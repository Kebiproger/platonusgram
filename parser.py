import httpx
from bs4 import BeautifulSoup
import html
import fake_useragent
import logging
import json
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



async def get_platonus_grades(login, password):
    ua=fake_useragent.UserAgent()
    headers = {
        "User-Agent": ua.random,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive"
    }

    async with httpx.AsyncClient(headers=headers, follow_redirects=True) as client:
        login_url = "https://platonus.iitu.edu.kz/rest/api/login"
        
        try:
            logger.info(f"🔑 Авторизация...")
            login_resp = await client.post(login_url, json={"login": login, "password": password})
            logger.info(f"DEBUG: login status = {login_resp.status_code}")
            
            # Определение текущего семестра
            resp = await client.get("https://platonus.iitu.edu.kz/student_register")
            logger.info(f"DEBUG: register status = {resp.status_code}, url = {resp.url}")
            
            soup = BeautifulSoup(resp.text, "html.parser")
            student_id_input = soup.find("input", {"name": "studentID"})
            
            if not student_id_input:
                logger.info(f"DEBUG: Part of HTML: {resp.text[:500]}")
                return "❌ Ошибка авторизации: неверный логин/пароль или сессия не сохранилась."
            if student_id_input: # Замени на свою проверку
            # 3. ВЫТАСКИВАЕМ КУКИ! 
                cookies_dict = dict(client.cookies)
                # Превращаем словарь в строку, чтобы сохранить в БД
                cookie_string = json.dumps(cookies_dict)
                 

            sid = student_id_input["value"]
            year_option = soup.find("select", {"id": "year"}).find("option", selected=True)
            term_option = soup.find("select", {"name": "term"}).find("option", selected=True)
            
            if not year_option or not term_option:
                return "❌ Ошибка: Не удалось определить текущий год или семестр."

            year = year_option["value"]
            term = term_option["value"]
            
            logger.info(f"📡 Получение оценок ({year}, семестр {term})...")
            grades_api_url = f"https://platonus.iitu.edu.kz/journal/{year}/{term}/{sid}"
            response = await client.get(grades_api_url)
            response.raise_for_status()
            
            data = response.json()

            result_text = "📊 <b>Ваши текущие оценки:</b>\n\n"
            for subject in data:
                full_name = subject.get("subjectName", "Неизвестно")
                name = html.escape(full_name.split('(')[0].strip())
                
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
                if len(result_text) + len(subject_text) > 4000:
                    result_text += "⚠️ <i>...и другие (слишком много оценок)</i>"
                    break
                
                result_text += subject_text

            # Возвращаем накопленный текст боту
            return result_text

        except httpx.HTTPStatusError as e:
            return f"❌ Ошибка сервера Platonus:\nСтатус-код: {e.response.status_code}\nURL: {e.request.url}"
        except AttributeError as e:
            return f"❌ Ошибка парсинга HTML (возможно, сайт изменился):\nПодробности: {html.escape(str(e))}"
        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            logger.error(f"ПОЛНАЯ ОШИБКА:\n{error_trace}", exc_info=True)
            return f"❌ Неизвестная ошибка: {type(e).__name__}\n{html.escape(str(e)) or 'Нет описания.'}"