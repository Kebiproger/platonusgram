from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "telegram_id" BIGINT NOT NULL UNIQUE,
    "login" VARCHAR(100),
    "platonus_sid" INT,
    "password_enc" TEXT,
    "session_cookie" TEXT,
    "cached_grades" JSONB,
    "cached_schedule" JSONB,
    "grades_updated_at" TIMESTAMPTZ,
    "schedule_updated_at" TIMESTAMPTZ,
    "error_count" INT NOT NULL DEFAULT 0,
    "is_active" BOOL NOT NULL DEFAULT True,
    "get_grades_updates" BOOL NOT NULL DEFAULT True
);
CREATE INDEX IF NOT EXISTS "idx_users_telegra_ab91e9" ON "users" ("telegram_id");
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "eJztmFtPIjEUgP8K4clNXIMDCLtvoKyyUdjouGs0ZlJmytDQaXHa8RLDf9+2c78huLhIwg"
    "uBc+mc8/WUzjmvVYdaELODawbd6vfKa5UAB4ovKfl+pQpms1gqBRyMsDL0hIWSgBHjLjC5"
    "EI4BZlCILMhMF804okRIiYexFFJTGCJixyKPoAcPGpzakE9UIHf3QoyIBZ8hC3/OpsYYQW"
    "yl4kSWfLaSG/xlpmR9wn8oQ/m0kWFS7DkkNp698AklkTUiXEptSKALOJTLc9eT4cvogjTD"
    "jPxIYxM/xISPBcfAwzyR7pIMTEokPxENUwna8ilftcNGq9GuHzXawkRFEklacz+9OHffUR"
    "EY6NW50gMOfAuFMebGIYa2CxyjCGAX2aUMM45vwwzRfQKa3zStXm9ptfpRu9lotZrtWoQ1"
    "r1rEt9s/lYiFARUl7x+EkHnMGFMbkTzd4wlwi9lGDhmqIpUlqAbMIqihSUw1PpdrwuqAZw"
    "NDYvOJ+HlYqy1A9rtzeXzWudwTVl/S4AaBSvN1aYYzDDglHjPYSic96/auMt0A0LWc+gQ9"
    "wNgTdS0DEjNPT4fPZfgyfltSjwvY6L0bdV4dxh5wsur2Ljo3qiCdl0BzPhychuaJKj0+H3"
    "YzeBlkTIQowNEpgqsAznvuEBciNoE5gZYhbhwRcJ7wz6vhoJhwzjED+JqIzO8sZPL9CkaM"
    "328bbpn6YtxZshICZdx21SpqgRLcTH56uKCk3wSedN0hXwK5X6GGN7MkBQPwPPQToeHIgc"
    "XgCxfIoLeCFQ7CL9uGXu9f9K70zsWvFP+Tjt6TGi317xJK944yexItUvnT188q8mfldjjo"
    "ZbcpstNvqzIm4HFqEPpkACuZdigORem7ITgH/7CxJUvstnbDWwtdl7pinzxSsKWlr6QZr/"
    "U0TstsXO3zvI8iZgCTo8eCi6VLKYaAlDTuSb8MuZFw/Ch0URu67prvDofnqXLv9rMvQ9cX"
    "3Z5ol1SdCyPES7pMG3IjdQUUvCYthFu8wI7yXA6dxtPE+EQKRsCcPgHRGuU0VKNltnmVoz"
    "lZCSDAVoRknjKrYAbXgS4yJ9WC6Vyg2V80nwOxzW5At8YL7aMHdI/QlR3iKuOjhMu7usl3"
    "Hd51TpC0ZnOJCZKwKp0gKV36/1EejRUgBubbCfBDRnDiiRwWveos6AVjlzX0gBvA+j+awI"
    "1eL/O/wcRJZQ=="
)
