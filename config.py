from loguru import logger
import sys

logger_config = {
    "handlers": [
        {"sink": sys.stderr, 'colorize': True, 'level': 'INFO'},
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