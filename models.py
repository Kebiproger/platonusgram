from tortoise import fields
from tortoise.models import Model


class User(Model):
    # Tortoise сам создаст поле id (Primary Key), но мы можем указать его явно
    id = fields.IntField(pk=True)

    # Главный идентификатор
    telegram_id = fields.BigIntField(unique=True, index=True)
    login = fields.CharField(max_length=100, null=True)

    # Данные для Платонуса
    password_enc = fields.TextField(null=True) # Для зашифрованного пароля
    session_cookie = fields.TextField(null=True) # Сюда будем класть JSON куки

    # Система кэширования
    cached_grades = fields.JSONField(null=True)
    grades_updated_at = fields.DatetimeField(null=True) 

    # Защита от банов
    error_count = fields.IntField(default=0)

    is_active = fields.BooleanField(default=True)
    get_grades_updates= fields.BooleanField(default=True)

    class Meta:
        table = "users" # Как таблица будет называться внутри файла database.db
