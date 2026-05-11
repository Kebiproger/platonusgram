from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "telegram_id" BIGINT NOT NULL UNIQUE,
    "login" VARCHAR(100),
    "password_enc" TEXT,
    "session_cookie" TEXT,
    "cached_grades" JSON,
    "grades_updated_at" TIMESTAMP,
    "error_count" INT NOT NULL DEFAULT 0,
    "is_active" INT NOT NULL DEFAULT 1
);
CREATE INDEX IF NOT EXISTS "idx_users_telegra_ab91e9" ON "users" ("telegram_id");
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "eJztl21P2zAQx79KlFdMYqikLe32roEOOtF2grAhpilyEze1mtghdiiI8d1nO89PXWFlgM"
    "S75u5/zt3Pjnt3r3rEhi7du6AwUD8r9yoGHuQ/CvZdRQW+n1mFgYGZK4UhV0gLmFEWAItx"
    "4xy4FHKTDakVIJ8hgrkVh64rjMTiQoSdzBRidB1CkxEHsoVM5OcvbkbYhreQJo/+0pwj6N"
    "qFPJEt3i3tJrvzpW2E2RcpFG+bmRZxQw9nYv+OLQhO1QgzYXUghgFgUCzPglCkL7KLy0wq"
    "ijLNJFGKuRgbzkHosly5GzKwCBb8eDZUFuiIt3zU9ju9Tr990OlzicwktfQeovKy2qNASW"
    "BiqA/SDxiIFBJjxo1BFzoB8Mw6gDpyGhmWAv8OM0H3Cmh+0rR2u6e12gf9bqfX6/ZbKdaq"
    "ax1ffXQsEHMB4Uc++hAS5hljlzgIV+keLkBQzzYNKFHlpWxANWaWQk0kGdXsu9wSVg/cmi"
    "7EDlvwx/1Waw2y74Ozw5PB2Q5XfSiCm8QuLfIVGfqA0hUJbBNiq4rSgLcNx7Qc90aIrgFo"
    "DC/lifMovXbz3HbGg0uJ1LuLPafTyXEiz3E+PJ3qJbwUUspT5ODIEsHHAK5GviOuRWwBaw"
    "Ftk9+ZPOEq4a/n00k94UpgCbCNLKb8VlxEN7lzXxVoUfR60GWmonxCmRPIVeQCZdARKDP0"
    "bUHBBKwK+4h7GPJgPfDaBcrQ4xX2kh9vDb0xGg/PjcH4W4H/0cAYCo9WOOSJdeegtCfpIs"
    "qPkXGiiEflajoZlrcp1RlXqsgJhIyYmKxMYOfLTsyJqbCtMAhIwHcpxDUb2timlKK206Zs"
    "snGtl+75cr0xNXk/jm5q7nWdEBcC3NAm5+NK5GY88LnQpU3fts+8Pp2eFo67Pipf3Bdjfc"
    "ibE3nOuQixXE8nho/5MtdGC8MMWMsV4A1GxUM00qStujzNK1sABo4kJOoUVcWz2AAGyFqo"
    "NVNa7NldN6eBTPM+qG2zB37mQe2Gj9cipQq85jEiF/KknuxJH+82Jwmt291gkuCqxklC+o"
    "q3ofg0HgExlr9NgM8yivE3Mlj3J7ymhc1C/ql5fQGg/6N7fdE/loc/COpbWg=="
)
