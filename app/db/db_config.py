# Файл: db_config.py
from app.core.config import DB_URL
from tortoise import Tortoise
from app.core.config import logger

TORTOISE_ORM = {
    "connections": {
        # ВАЖНО: Указал твою базу database.db, а не db.sqlite3!
        "default": DB_URL
    }, 
    "apps": {
        "models": {
            # Указываем твой файл models.py и служебный файл aerich
            "models": ["app.db.models", "aerich.models"], 
            "default_connection": "default",
        },
    },
}
async def init_db(generate_schemas: bool = False):
    await Tortoise.init(
        db_url=DB_URL,
        modules={'models' : ["app.db.models"]}
    )
    if generate_schemas:
        await Tortoise.generate_schemas()
    
    conn = Tortoise.get_connection("default")
    
    logger.info("База данных Tortoise инициализирована!")