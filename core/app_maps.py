"""
Единый источник правды для маппингов "процесс → имя" и "имя → категория".
Раньше эти словари были продублированы в tracker.py и stats.py и постепенно
разъехались (в одном есть Firefox/Spotify, в другом — нет). Теперь оба
модуля импортируют отсюда.
"""

APP_NAMES = {
    "chrome.exe":         "Google Chrome",
    "firefox.exe":        "Firefox",
    "msedge.exe":         "Microsoft Edge",
    "opera.exe":          "Opera",
    "brave.exe":          "Brave",
    "vivaldi.exe":        "Vivaldi",
    "steam.exe":          "Steam",
    "steamwebhelper.exe": "Steam",
    "cs2.exe":            "CS2",
    "dota2.exe":          "Dota 2",
    "discord.exe":        "Discord",
    "telegram.exe":       "Telegram",
    "code.exe":           "VS Code",
    "pycharm64.exe":      "PyCharm",
    "spotify.exe":        "Spotify",
    "vlc.exe":            "VLC",
    "explorer.exe":       "Рабочий стол",
    "idea64.exe":         "IntelliJ IDEA",
    "figma.exe":          "Figma",
    "slack.exe":          "Slack",
    "zoom.exe":           "Zoom",
    "obs64.exe":          "OBS Studio",
    "photoshop.exe":      "Photoshop",
}

BROWSER_PROCESSES = {
    "chrome.exe", "firefox.exe", "msedge.exe",
    "opera.exe", "brave.exe", "vivaldi.exe",
}

# Единая карта "читаемое имя приложения → категория"
CATEGORIES = {
    # Браузеры
    "Google Chrome":    "browser",
    "Firefox":          "browser",
    "Microsoft Edge":   "browser",
    "Opera":            "browser",
    "Brave":            "browser",
    "Vivaldi":          "browser",

    # Общение
    "Discord":  "chat",
    "Telegram": "chat",
    "Slack":    "chat",
    "Zoom":     "chat",

    # Работа
    "VS Code":         "work",
    "PyCharm":         "work",
    "IntelliJ IDEA":   "work",
    "Figma":           "work",
    "Photoshop":       "work",
    "Wps":             "work",

    # Музыка / видео
    "Spotify":         "music",
    "Яндекс музыка":   "music",
    "VLC":             "video",

    # Игры
    "Steam":     "gaming",
    "CS2":       "gaming",
    "Dota 2":    "gaming",
    "Xr_3da":    "gaming",      # S.T.A.L.K.E.R.
    "Isaac-ng":  "gaming",
    "Java":      "tlauncher",
    "Javaw":     "tlauncher",

    # Стрим
    "OBS Studio": "streaming",

    # Торренты
    "Qbittorrent": "torrent",

    # Фото
    "Photos": "photo",

    # VPN
    "V2raytun": "vpn",

    # Архиваторы
    "7zfm":   "archive",
    "Winrar": "archive",

    # Мои приложения
    "Python3.12": "myapps",
    "Python":     "myapps",

    "Searchapp": "Paneltask",
}

# Категории которые считаются медиа (не AFK даже без ввода)
MEDIA_CATEGORIES = {"video", "music", "streaming"}

# Ключевые слова в заголовке браузера = медиа
MEDIA_TITLES = {
    "youtube", "ютуб", "twitch", "netflix", "кинопоиск",
    "okko", "иви", "premier", "vk видео", "vk video",
    "rutube", "яндекс видео",
}


def clean_process_name(name: str) -> str:
    return name.replace(".exe", "").replace(".EXE", "").capitalize() or "Неизвестно"


def app_name_for(proc_name: str) -> str:
    """proc_name уже в нижнем регистре, например 'chrome.exe'"""
    return APP_NAMES.get(proc_name, clean_process_name(proc_name))
