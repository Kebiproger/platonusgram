from aiohttp import web
import secrets
from crypto import encrypt_password
from db_api import save_user, init_db
# Временное хранилище токенов (в идеале использовать Redis, но для начала хватит словаря)
# Формат: { "token_string": telegram_id }
active_tokens = {}

# --- СТРАНИЦА ФОРМЫ (GET-запрос) ---
async def handle_login_get(request):
    # 1. Извлекаем токен из ссылки: http://.../login?token=123
    token = request.query.get('token')
    
    # 2. Проверяем, существует ли такой токен в нашем словаре
    if not token or token not in active_tokens:
        return web.Response(text="Ошибка: Ссылка недействительна или устарела.", status=403)
    
    # 3. Если всё ок, отдаем HTML-форму (строкой)
    html_content = f"""
    <html>
        <body>
            <h2>Авторизация в Platonus</h2>
            <form action="/login?token={token}" method="post">
                <input type="text" name="username" placeholder="Логин" required><br>
                <input type="password" name="password" placeholder="Пароль" required><br>
                <button type="submit">Войти</button>
            </form>
        </body>
    </html>
    """
    return web.Response(text=html_content, content_type='text/html')

# --- ПРИЕМ ДАННЫХ ОТ ПОЛЬЗОВАТЕЛЯ (POST-запрос) ---
async def handle_login_post(request):
    token = request.query.get('token')
    
    if not token or token not in active_tokens:
         return web.Response(text="Ошибка: Ссылка устарела.", status=403)
    
    # 1. Достаем Telegram ID по токену
    user_id = active_tokens[token]
    
    # 2. Получаем данные из HTML-формы
    data = await request.post()
    username = data.get('username')
    password = data.get('password')
    
    # ТУТ БУДЕТ МАГИЯ:
    password_enc = encrypt_password(password)
    save_user(user_id, username, password_enc)
    
    # 3. Уничтожаем токен, чтобы ссылка стала недействительной
    del active_tokens[token]
    
    return web.Response(text="Успешно! Данные зашифрованы. Можете закрыть страницу и вернуться в Telegram.")

# --- ЗАПУСК СЕРВЕРА ---
def setup_web_app():
    init_db()  # Инициализируем базу данных при старте сервера
    app = web.Application()
    # Регистрируем маршруты
    app.router.add_get('/login', handle_login_get)
    app.router.add_post('/login', handle_login_post)
    return app