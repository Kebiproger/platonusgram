# Файл: db_config.py
from backend.config import DB_URL

TORTOISE_ORM = {
    "connections": {
        # ВАЖНО: Указал твою базу database.db, а не db.sqlite3!
        "default": DB_URL
    }, 
    "apps": {
        "models": {
            # Указываем твой файл models.py и служебный файл aerich
            "models": ["backend.db.models", "aerich.models"], 
            "default_connection": "default",
        },
    },
}