import asyncio
import html
import json
import logging
import random
import traceback
from datetime import datetime, timedelta, timezone
import httpx
from bs4 import BeautifulSoup
from crypto import fernet_decrypt_password
from models import User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

platonus_semaphore = None # Глобальный семафор для ограничения одновременных запросов к Платонусу

MAX_MESSAGE_LENGTH = 4000
HTTP_OK = 200

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
]

def get_semaphore():
    global platonus_semaphore
    # Если семафора еще нет, создаем его (это произойдет только 1 раз!)
    if platonus_semaphore is None:
        platonus_semaphore = asyncio.Semaphore(5)
        logger.info("Семафор для Платонуса успешно инициализирован!")
    
    return platonus_semaphore

def get_stealth_headers() -> dict:
    """Генерирует заголовки, чтобы выглядеть как настоящий браузер из СНГ."""
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
    }


async def get_platonus_grades(user: User) -> tuple[str, bool]:
    """
    Парсит оценки.
    Возвращает кортеж: (Текст_с_оценками, Актуальные_Cookies_словарем)
    """
    sem=get_semaphore() # Получаем глобальный семафор
    cookies = user.session_cookie
    if cookies:
        cookies = json.loads(cookies)
    else:
        cookies = None
    now = datetime.now(timezone.utc)

    if user.grades_updated_at:
        # Вычисляем разницу во времени
        time_diff = now - user.grades_updated_at
        
        # Если прошло меньше 1 часа (timedelta(hours=1)) И оценки есть в базе
        if time_diff < timedelta(hours=1) and user.cached_grades:
            logger.info(f"Студент {user.login} получил оценки из кэша.")
            # Возвращаем данные и флаг is_cached = True
            return user.cached_grades, True 
        
    async with sem: # Входим в контекст семафора (гарантирует, что одновременно будет не больше 5 таких блоков)
        logger.info(f"Студент {user.login} встал в очередь на парсинг.")
        
        async with httpx.AsyncClient(
            cookies=cookies,
            headers=get_stealth_headers(),
            follow_redirects=True,
            timeout=httpx.Timeout(20.0),
            http2=True,
            limits=httpx.Limits(max_connections=20, max_keepalive_connections=10),
        ) as client:
            try:
                logger.info("📡 Проверяем актуальность сессии (Cookies)...")
                resp = await client.get("https://platonus.iitu.edu.kz/student_register")
                logger.info(f"DEBUG: register status = {resp.status_code}, url = {resp.url}")
                await asyncio.sleep(
                    random.uniform(1.2, 2.5)
                )  # Jitter имитация реального человека

                if "AccessDenied" in str(resp.url):
                    logger.info(
                        "🔑 Сессия устарела или отсутствует. Имитируем ввод логина..."
                    )
                    # Человек вводит логин/пароль не моментально. Ждем 2-4 секунды.
                    await asyncio.sleep(random.uniform(2.0, 4.5))

                    # Добавляем Referer, как будто мы реально нажали кнопку на главной странице
                    client.headers.update({"Referer": "https://platonus.iitu.edu.kz/"})

                    login_url = "https://platonus.iitu.edu.kz/rest/api/login"
                    logger.info("🔑 Авторизация...")
                    login_resp = await client.post(
                        login_url, json={"login": user.login, "password": fernet_decrypt_password(user.password_enc)}
                    )

                    if login_resp.status_code != HTTP_OK:
                        return (
                            f"❌ Ошибка авторизации (Код: {login_resp.status_code}). Проверьте пароль.",
                            cookies,
                        )
                    logger.info("✅ Успешный вход! Сохраняем новые куки.")

                    # Имитация паузы после логина (пока грузится дашборд)
                    await asyncio.sleep(random.uniform(1.0, 2.0))

                    # Запрашиваем страницу еще раз, уже с новыми куками
                    resp = await client.get("https://platonus.iitu.edu.kz/student_register")
                else:
                    logger.info(
                        "🚀 Сессия (Cookies) жива! Логин не потребовался. Экономим время."
                    )

                soup = BeautifulSoup(resp.text, "lxml")
                student_id_input = soup.find("input", {"name": "studentID"})

                if not student_id_input:
                    logger.info(f"DEBUG: Part of HTML: {resp.text[:500]}")
                    return (
                        "❌ Ошибка авторизации: неверный логин/пароль или сессия не сохранилась.",
                        cookies,
                    )

                sid = student_id_input.get("value")

                year_select = soup.find("select", {"id": "year"})
                term_select = soup.find("select", {"name": "term"})

                if not year_select or not term_select:
                    return "❌ Не удалось найти селекторы года или семестра.", cookies

                # Ищем выбранные опции внутри найденных селекторов
                year_option = year_select.find("option", selected=True)
                term_option = term_select.find("option", selected=True)

                if not year_option or not term_option:
                    return "❌ Не удалось определить текущий год или семестр.", cookies

                # Безопасно достаем value
                year = year_option.get("value")
                term = term_option.get("value")

                client.headers.update(
                    {
                        "Referer": "https://platonus.iitu.edu.kz/student_register",
                        "Accept": "application/json, text/plain, */*",
                    }
                )

                await asyncio.sleep(random.uniform(0.5, 1.2))

                logger.info(f"📡 Получение оценок ({year}, семестр {term})...")
                grades_api_url = f"https://platonus.iitu.edu.kz/journal/{year}/{term}/{sid}"
                response = await client.get(grades_api_url)
                response.raise_for_status()

                data = response.json()

                result_text = "📊 <b>Ваши текущие оценки:</b>\n\n"
                for subject in data:
                    full_name = subject.get("subjectName", "Неизвестно")
                    name = html.escape(full_name.split("(")[0].strip())

                    marks_list = []
                    exams = subject.get("exams", [])
                    for ex in exams:
                        ex_name = html.escape(ex.get("name", "Элемент"))
                        ex_mark = html.escape(str(ex.get("mark", "")))
                        if ex_mark and ex_mark != "-":
                            marks_list.append(f"  ▫️ <i>{ex_name}</i>: <b>{ex_mark}</b>")

                    subject_text = f"📚 <b>{name}</b>\n"
                    if marks_list:
                        subject_text += "\n".join(marks_list)
                    else:
                        subject_text += "  ▫️ <i>Нет оценок</i>"
                    subject_text += "\n\n"

                    # Проверка на лимит сообщения (4096 символов)
                    if len(result_text) + len(subject_text) > MAX_MESSAGE_LENGTH:
                        result_text += "⚠️ <i>...и другие (слишком много оценок)</i>"
                        break

                    result_text += subject_text

                # Возвращаем накопленный текст боту
                current_cookies = dict(client.cookies)
                user.cached_grades = result_text
                user.grades_updated_at = now
                if current_cookies:
                    user.session_cookie = json.dumps(current_cookies)
                await user.save()

                return result_text, False  # is_cached = False, т.к. мы только что получили свежие данные с сайта

            except httpx.HTTPStatusError as e:
                if e.response.status_code in (429, 403):
                    logger.warning(f"🚨 WAF БЛОКИРОВКА! Код: {e.response.status_code}")
                    # Здесь в будущем можно включать глобальный "Circuit Breaker"
                return (
                    f"❌ Сервер Platonus временно недоступен (Код: {e.response.status_code}). Попробуйте позже.",
                    cookies,
                )
            except AttributeError as e:
                return (
                    f"❌ Ошибка парсинга HTML (возможно, сайт изменился):\nПодробности: {html.escape(str(e))}",
                    cookies,
                )
            except Exception as e:
                error_trace = traceback.format_exc()
                logger.error(f"ПОЛНАЯ ОШИБКА:\n{error_trace}", exc_info=True)
                return (
                    f"❌ Неизвестная ошибка: {type(e).__name__}\n{html.escape(str(e)) or 'Нет описания.'}",
                    cookies,
                )
