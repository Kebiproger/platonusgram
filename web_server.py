from aiohttp import web
import secrets
from crypto import encrypt_password
from db_api import save_user, init_db
import os
from bot_handler import get_main_kb
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
    try:
        with open('Platonus.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
    except FileNotFoundError:
        return web.Response(text="Ошибка: Файл формы не найден.", status=500)
    
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
    username = data.get('login')
    password = data.get('password')
    
    if not username or not password:
        return web.Response(text="Ошибка: Все поля должны быть заполнены.", status=400)
    
    password_enc = encrypt_password(password)
    save_user(user_id, username, password_enc)
    
    try:
        await bot.send_message(
            user_id, 
            "✅ **Авторизация прошла успешно!**\n\n"
            "Теперь ты можешь проверять свои оценки прямо в меню ниже.",
            reply_markup=get_main_kb(), # Та самая кнопка "Узнать оценки"
            parse_mode="Markdown"
        )
    except Exception as e:
        print(f"Ошибка отправки уведомления: {e}")

    # 3. Уничтожаем токен
    del active_tokens[token]
    
    return web.Response(text="Успешно! Возвращайтесь в Telegram.")
# --- ЗАПУСК СЕРВЕРА ---
def setup_web_app():
    init_db()  # Инициализируем базу данных при старте сервера
    app = web.Application()
    # Регистрируем маршруты
    app.router.add_get('/login', handle_login_get)
    app.router.add_post('/login', handle_login_post)

    if os.path.exists('Platonus_files'):
        app.router.add_static('/Platonus_files', 'Platonus_files')

    return app