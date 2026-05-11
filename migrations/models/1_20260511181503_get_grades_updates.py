from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" ADD "get_grades_updates" INT NOT NULL DEFAULT 1;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" DROP COLUMN "get_grades_updates";"""


MODELS_STATE = (
    "eJztl21P2zAQx79KlVdMYqikLe32roEOOtF2grAhpilyEze1mtghdngQ63ef7Tw/rrAyQO"
    "Jdc/c/5+5nx717UFxiQYfuXVDoK59bDwoGLuQ/cvbdlgI8L7UKAwNzRwoDrpAWMKfMBybj"
    "xgVwKOQmC1LTRx5DBHMrDhxHGInJhQjbqSnA6DqABiM2ZEuZyM9f3IywBe8gjR+9lbFA0L"
    "FyeSJLvFvaDXbvSdsYsy9SKN42N0ziBC5Oxd49WxKcqBFmwmpDDH3AoFie+YFIX2QXlRlX"
    "FGaaSsIUMzEWXIDAYZlyN2RgEiz48WyoLNAWb/mo7nf73UHnoDvgEplJYumvw/LS2sNASW"
    "CqK2vpBwyECokx5cagA20fuEYVQA3ZtQwLgX+HGaN7BTQ/qWqn01fbnYNBr9vv9wbtBGvZ"
    "1cRXGx8LxFxA+JEPP4SYecrYITbCZbqHS+BXs00CClR5KRtQjZglUGNJSjX9LreE1QV3hg"
    "OxzZb8cb/dbkD2fXh2eDI82+GqD3lw08ilhr48Qw9Qekt8y4DYLKPU4V3NMS3GvRGiDQD1"
    "0aU8cS6l106W285keCmRuveR53Q2PY7lGc6HpzOtgJdCSnmKHBxZIfgYwOXId8SViE1gLq"
    "Fl8DuTJ1wm/PV8Nq0mXAosALaQyVq/Ww6im9y5rwq0KLoZdJGpKJ9QZvtyFblAEXQIygg8"
    "S1AwACvDPuIehlxYDbxygSL0aIW9+MdbQ6+PJ6NzfTj5luN/NNRHwqPmDnls3Tko7EmySO"
    "vHWD9picfW1Ww6Km5TotOvFJETCBgxMLk1gJUtOzbHpty2Qt8nPt+lAFdsaG2bUojaTpuy"
    "yca1X7rny/TG1OD9OLqpuNc1QhwIcE2bnI0rkJvzwOdClzR92z7z2mx2mjvu2rh4cV9MtB"
    "FvTuQ55yLEano6PqEYuXui4kpvhFu9wDvltRjxFqvMsCIMc2CubgFv40oeopI6bdnlqm7R"
    "AjCwJSFRp6gqmniH0EfmUqmYhSPPbtM0DFLN+zi8xT+05x6Hb6AvutnHDGuZkCd1vk/6eL"
    "c5r6m93gbzGlfVzmvSl78fxafxCIiR/G0CfJaBl7+RwapWp2FQSEP+aUR4AaD/Y0Z40T+W"
    "9R8pds8c"
)
