import asyncio
import os
import json
from datetime import datetime
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from fastapi import FastAPI, Request
import httpx

# Загрузка настроек
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
LOGIN = os.getenv("PLATONUS_LOGIN")
PASSWORD = os.getenv("PLATONUS_PASSWORD")
DB_FILE = "last_grades.json"

app = FastAPI()

# --- Ядро Платонуса ---
async def fetch_platonus():
    """Авторизуется и забирает свежие данные"""
    headers = {"User-Agent": "Mozilla/5.0"}
    async with httpx.AsyncClient(headers=headers, follow_redirects=True, timeout=30.0) as client:
        # 1. Вход
        await client.post("https://platonus.iitu.edu.kz/rest/api/login", 
                         json={"login": LOGIN, "password": PASSWORD})
        
        # 2. Определение контекста (семестр/ID)
        resp = await client.get("https://platonus.iitu.edu.kz/student_register")
        soup = BeautifulSoup(resp.text, "html.parser")
        
        sid = soup.find("input", {"name": "studentID"})["value"]
        year = soup.find("select", {"id": "year"}).find("option", selected=True)["value"]
        term = soup.find("select", {"name": "term"}).find("option", selected=True)["value"]
        
        # 3. Запрос JSON
        api_url = f"https://platonus.iitu.edu.kz/journal/{year}/{term}/{sid}"
        return (await client.get(api_url)).json()

def format_html_report(data, title="Ваши оценки"):
    """Создает красивый HTML для Telegram"""
    msg = f"📊 <b>{title}</b>\n<i>Обновлено: {datetime.now().strftime('%d.%m %H:%M')}</i>\n\n"
    for s in data:
        name = s.get("subjectName").split('(')[0].strip()
        marks = [f"{e['name']}: {e['mark']}" for e in s.get("exams", []) if e['mark'] != "-"]
        msg += f"📖 <b>{name}</b>\n<code>{ ' | '.join(marks) if marks else '...' }</code>\n\n"
    return msg

async def send_tg(text: str):
    """Отправка сообщения через API Telegram"""
    async with httpx.AsyncClient() as client:
        await client.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                         json={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"})

# --- Фоновый мониторинг ---
async def monitoring_loop():
    """Проверка изменений каждые 30 минут"""
    while True:
        try:
            new_data = await fetch_platonus()
            if os.path.exists(DB_FILE):
                with open(DB_FILE, "r") as f: old_data = json.load(f)
                # Простое сравнение JSON (можно усложнить для детального отчета)
                if json.dumps(old_data) != json.dumps(new_data):
                    await send_tg("🔔 <b>Обнаружены изменения в оценках!</b>\n\n" + format_html_report(new_data))
            
            with open(DB_FILE, "w") as f: json.dump(new_data, f)
        except Exception as e:
            print(f"Ошибка мониторинга: {e}")
        await asyncio.sleep(1800)

@app.on_event("startup")
async def on_startup():
    # Запускаем мониторинг как фоновую задачу
    asyncio.create_task(monitoring_loop())

# --- Обработка Webhook ---
@app.post("/webhook")
async def handle_webhook(request: Request):
    update = await request.json()
    if "message" in update:
        msg = update["message"]
        text = msg.get("text", "")
        uid = msg["from"]["id"]

        # Проверяем, что пишет именно владелец (вы)
        if str(uid) != str(CHAT_ID):
            return {"ok": True}

        if text in ["/grades", "/start"]:
            asyncio.create_task(process_user_request())

    return {"ok": True}

async def process_user_request():
    """Отдельная задача для ответа пользователю, чтобы не блокировать webhook"""
    try:
        data = await fetch_platonus()
        await send_tg(format_html_report(data))
    except Exception as e:
        await send_tg(f"❌ Ошибка при запросе к Платонусу: {e}")
