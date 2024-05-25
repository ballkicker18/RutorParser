from loguru import logger
import sys

logger_config = {
    "handlers": [
        {"sink": sys.stderr, 'colorize': True, 'level': 'DEBUG'},
        # {"sink": "log/debug.log", "serialize": False, 'level': 'DEBUG'},
        {"sink": "log/info.log", "serialize": False, 'level': 'INFO'}
    ]
}
logger.configure(**logger_config)

RUTOR_LINK = 'https://rutor.org'
USE_TOR = False
TOR_PORT = 9050
USE_PROXY = False
PROXIES = {
    'http': 'http://ip:port',
    'https': 'http://ip:port',
}
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; rv:125.0) Gecko/20100101 Firefox/125.0'

CATEGORIES = {
    "Любая категория": 0,
    "Зарубежные фильмы": 1,
    "Наши фильмы": 5,
    "Научно-популярные фильмы": 12,
    "Зарубежные сериалы": 4,
    "Наши сериалы": 16,
    "Телевизор": 6,
    "Мультипликация": 7,
    "Аниме": 10,
    "Музыка": 2,
    "Игры": 8,
    "Софт": 9,
    "Спорт и здоровье": 13,
    "Юмор": 15,
    "Хозяйство и быт": 14,
    "Книги": 11,
    "Другое": 3,
    "Иностранные релизы": 17 
}