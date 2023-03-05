"""
Config File
"""

from os import environ


PENGUIN_GIFS_CODE = [(1, 54796), (10, 1111955)]

DB_LOGIN_DATA = {
"host": 'ip' if environ.get("HOMEPATH") == "\\Users\\mintnt" else "localhost", 
"user": '',
"password": '', 
"db": ''}



BOT_TOKEN = ""

FILES = {"bak_124": "BQACAgIAAxkBAAMfYujleFr-xhGjNxd8jTjml3FsUXIAAlcdAAKIiBhLcnKKov7V8ZQpBA", 
"bak_113": "BQACAgIAAxkBAAMiYujqUXjQno6TaqrwDXRmSaUiJ_4AAlgdAAKIiBhLlzxbuEBVCp0pBA",
"bak_121": "BQACAgIAAxkBAAMvYujvvnV6UOsYE8aHE1F8H-K3cYgAAlkdAAKIiBhL3pS2bSBmVycpBA",
"bak_122": "BQACAgIAAxkBAAMyYujv5BLh0OuKcUZGYLpQ9d1CrxYAAlsdAAKIiBhL93ag1ZEMZOkpBA",
"chitalka": "AgACAgIAAxkBAAIBoGLu1p4HQiRJxe6q7yik4GhFZW2kAALrwjEb4uZ5SxYCtrWVz_81AQADAgADeQADKQQ"}

WAITING_TIME_BEFORE_BACKUP = 60*10
BACKUP_UPDATE_TIME = 60


AUTODELETE_TIME = 60*3

MONITORING_STATS = "stats.png"
SITE_MONITORING_LOCATION = "stats.html" if environ.get("HOMEPATH") == "\\Users\\mintnt" else "../templates/monitoring.html"

EMOJIES = {"🚾": "туалет", "🔒": "замок", "📆": "календар", "📱": "телефон", "🎹": "піаніно", "🌻": "соняшник", "🐧": "пінгвінчик", "🧶": "нитка", "⚽️": "мяч","🔦": "фонарик","🚬": "сигарета"}
EMOJIES_REV = {x:k for k,x in EMOJIES.items()}
EMOJIES_LIST = list(EMOJIES.values())