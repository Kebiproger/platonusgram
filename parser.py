import httpx
from bs4 import BeautifulSoup
from config import LOGIN, PASSWORD 


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

            result_text = "📊 <b>Ваши текущие оценки:</b>\n\n"
            for subject in data:
                full_name = subject.get("subjectName", "Неизвестно")
                name = full_name.split('(')[0].strip()
                
                marks_list = []
                exams = subject.get("exams", [])
                for ex in exams:
                    ex_name = ex.get("name")
                    ex_mark = ex.get("mark")
                    if ex_mark and ex_mark != "-":
                        marks_list.append(f"  ▫️ <i>{ex_name}</i>: <b>{ex_mark}</b>")
                
                if marks_list:
                    marks_str = "\n".join(marks_list)
                else:
                    marks_str = "  ▫️ <i>Нет оценок</i>"
                
                result_text += f"📚 <b>{name}</b>\n{marks_str}\n\n"

            # Возвращаем накопленный текст боту
            return result_text

        except httpx.HTTPStatusError as e:
            return f"❌ Ошибка сервера Platonus:\nСтатус-код: {e.response.status_code}\nURL: {e.request.url}"
        except AttributeError as e:
            return f"❌ Ошибка парсинга HTML (возможно, неверный логин/пароль или сайт изменился):\nПодробности: Не удалось найти элемент на странице. {e}"
        except Exception as e:
            import traceback
            # Получаем детальный лог ошибки с указанием строки
            error_trace = traceback.format_exc()
            print("ПОЛНАЯ ОШИБКА:\n", error_trace) # Выведет в терминал
            return f"❌ Неизвестная ошибка: {type(e).__name__}\n{str(e) or 'Нет описания ошибки. Смотри терминал.'}"