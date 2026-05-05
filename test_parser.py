import asyncio
import httpx
import os
import json
from dotenv import load_dotenv
from bs4 import BeautifulSoup

# Подгружаем данные из .env
load_dotenv()
LOGIN = os.getenv("PLATONUS_LOGIN")
PASSWORD = os.getenv("PLATONUS_PASSWORD")

async def get_platonus_grades():
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json, text/plain, */*",
    }

    async with httpx.AsyncClient(headers=headers, follow_redirects=True) as client:
        login_url = "https://platonus.iitu.edu.kz/rest/api/login"
        
        try:
            print(f"🔑 Авторизация...")
            await client.post(login_url, json={"login": LOGIN, "password": PASSWORD})
            
            # Определение текущего семестра
            resp = await client.get("https://platonus.iitu.edu.kz/student_register")
            soup = BeautifulSoup(resp.text, "html.parser")
            sid = soup.find("input", {"name": "studentID"})["value"]
            year = soup.find("select", {"id": "year"}).find("option", selected=True)["value"]
            term = soup.find("select", {"name": "term"}).find("option", selected=True)["value"]
            
            print(f"📡 Получение оценок ({year}, семестр {term})...")
            grades_api_url = f"https://platonus.iitu.edu.kz/journal/{year}/{term}/{sid}"
            response = await client.get(grades_api_url)
            response.raise_for_status()
            
            data = response.json()
            
            print("\n" + "="*80)
            print(f"{'ДИСЦИПЛИНА':<45} | {'ОЦЕНКИ'}")
            print("="*80)

            for subject in data:
                full_name = subject.get("subjectName", "Неизвестно")
                name = full_name.split('(')[0].strip()
                
                marks_list = []
                exams = subject.get("exams", [])
                for ex in exams:
                    ex_name = ex.get("name")
                    ex_mark = ex.get("mark")
                    if ex_mark and ex_mark != "-":
                        marks_list.append(f"{ex_name}: {ex_mark}")
                
                marks_str = " | ".join(marks_list) if marks_list else "Нет оценок"
                print(f"📖 {name[:43]:<43} | {marks_str}")
                print("-" * 80)

        except Exception as e:
            print(f"❌ ОШИБКА: {e}")

if __name__ == "__main__":
    asyncio.run(get_platonus_grades())
