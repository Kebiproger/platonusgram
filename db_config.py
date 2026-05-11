# Файл: db_config.py

TORTOISE_ORM = {
    "connections": {
        # ВАЖНО: Указал твою базу database.db, а не db.sqlite3!
        "default": "sqlite://database.db" 
    }, 
    "apps": {
        "models": {
            # Указываем твой файл models.py и служебный файл aerich
            "models": ["models", "aerich.models"], 
            "default_connection": "default",
        },
    },
}