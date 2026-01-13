from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    bot_token: str
    admin_id: str


@dataclass
class LogSettings:
    level: str
    format: str


@dataclass
class Config:
    tg_bot: TgBot
    log: LogSettings


def load_config(path: str | None = None) -> Config:

    env = Env()
    env.read_env(path)
    
    return Config(
        tg_bot=TgBot(
            bot_token=env('BOT_TOKEN'),
            admin_id=env('ADMIN_ID')
        ),
        log=LogSettings(
            level=env('LOG_LEVEL'),
            format=env('LOG_FORMAT')
        )
    )
