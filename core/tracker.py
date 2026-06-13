"""
Трекер активности - читает активное окно каждую секунду.
Три состояния: active / watching / afk
"""
import time
import threading
import ctypes
import ctypes.wintypes
import os
import json
from datetime import datetime
from collections import deque

user32   = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

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

CATEGORIES = {
    # Браузеры
    "Google Chrome": "browser",
    "Firefox": "browser",
    "Microsoft Edge": "browser",
    "Opera": "browser",
    "Brave": "browser",
    "Vivaldi": "browser",

    # Общение
    "Discord": "chat",
    "Telegram": "chat",
    "Slack": "chat",
    "Zoom": "chat",

    # Работа
    "VS Code": "work",
    "PyCharm": "work",
    "IntelliJ IDEA": "work",
    "Figma": "work",
    "Photoshop": "work",
    "Wps": "work",

    # Музыка / Видео
    "Spotify": "music",
    "VLC": "video",
    "Яндекс музыка": "music",

    # Игры
    "Steam": "gaming",
    "CS2": "gaming",
    "Dota 2": "gaming",
    "Xr_3da": "gaming",
    "Isaac-ng": "gaming",
    "Java": "tlauncher",
    "Javaw": "tlauncher",

    # Прочее
    "Qbittorrent": "torrent",
    "Photos": "photo",
    "V2raytun": "vpn",
    "7zfm": "archive",
    "Winrar": "archive",
    "OBS Studio": "streaming",
    "Python3.12": "myapps",
    "Python": "myapps",
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

AFK_TIMEOUT  = 300   # 5 минут без ввода → проверяем медиа
AFK_HARD     = 1800  # 30 минут без ввода → AFK в любом случае


def _settings_path():
    return os.path.join(os.path.dirname(__file__), "..", "settings.json")


def load_settings():
    try:
        with open(_settings_path(), "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


class ActivityTracker:
    def __init__(self):
        self.current = {
            "app": "—", "title": "", "category": "idle",
            "since": datetime.now(),
            "status": "active",   # active | watching | afk
        }
        self.history  = deque(maxlen=100)
        self._lock    = threading.Lock()
        self._running = False
        self._on_change_callbacks = []

        # Счётчики времени за сессию
        self._time_active   = 0   # секунд активно
        self._time_watching = 0   # секунд смотрит медиа
        self._time_afk      = 0   # секунд AFK
        self._session_start = datetime.now()

    def on_change(self, cb):
        self._on_change_callbacks.append(cb)

    def get_current(self):
        with self._lock:
            return dict(self.current)

    def get_history(self):
        with self._lock:
            return list(self.history)

    def get_time_stats(self):
        """Время за текущую сессию (с момента запуска приложения)"""
        with self._lock:
            return {
                "active":   self._time_active,
                "watching": self._time_watching,
                "afk":      self._time_afk,
                "total":    self._time_active + self._time_watching,
                "session_start": self._session_start.isoformat(),
            }

    def start(self):
        self._running  = True
        prev_app   = None
        prev_title = None

        while self._running:
            try:
                proc_name, app, title = self._get_active_window()
                idle_secs = self._get_idle_seconds()
                status    = self._calc_status(idle_secs, app, title)

                # Приватный режим
                settings = load_settings()
                if settings.get("private_mode") and proc_name.lower() in BROWSER_PROCESSES:
                    title = ""

                changed = (app != prev_app or title != prev_title)

                if changed:
                    now = datetime.now()
                    with self._lock:
                        if prev_app and prev_app != "—":
                            self.history.appendleft({
                                "app":       prev_app,
                                "title":     prev_title,
                                "category":  CATEGORIES.get(prev_app, "other"),
                                "timestamp": self.current["since"],
                            })
                        self.current = {
                            "app":      app,
                            "title":    title,
                            "category": CATEGORIES.get(app, "other"),
                            "since":    now,
                            "status":   status,
                            # для обратной совместимости с сетью
                            "afk":      status == "afk",
                        }
                    prev_app   = app
                    prev_title = title
                    for cb in self._on_change_callbacks:
                        try: cb(self.current)
                        except Exception: pass
                else:
                    with self._lock:
                        self.current["status"] = status
                        self.current["afk"]    = status == "afk"

                # Считаем время по статусу
                with self._lock:
                    if status == "active":
                        self._time_active   += 1
                    elif status == "watching":
                        self._time_watching += 1
                    else:
                        self._time_afk      += 1

            except Exception:
                pass

            time.sleep(1)

    def stop(self):
        self._running = False

    def _calc_status(self, idle_secs, app, title):
        """Определяем статус: active / watching / afk"""
        if idle_secs < AFK_TIMEOUT:
            return "active"

        # Жёсткий AFK — 30 минут без ввода, без вариантов
        if idle_secs >= AFK_HARD:
            return "afk"

        # Проверяем медиа по категории
        category = CATEGORIES.get(app, "other")
        if category in MEDIA_CATEGORIES:
            return "watching"

        # Проверяем браузер — смотрит ли медиа по заголовку
        if category == "browser" and title:
            title_lower = title.lower()
            if any(kw in title_lower for kw in MEDIA_TITLES):
                return "watching"

        return "afk"

    def _get_idle_seconds(self):
        """Сколько секунд прошло с последнего ввода мыши/клавы"""
        try:
            li = ctypes.wintypes.LASTINPUTINFO()
            li.cbSize = ctypes.sizeof(li)
            user32.GetLastInputInfo(ctypes.byref(li))
            return (kernel32.GetTickCount() - li.dwTime) / 1000.0
        except Exception:
            return 0

    def _get_active_window(self):
        try:
            hwnd = user32.GetForegroundWindow()
            if not hwnd:
                return "explorer.exe", "Рабочий стол", ""

            length = user32.GetWindowTextLengthW(hwnd)
            title  = ""
            if length > 0:
                buf = ctypes.create_unicode_buffer(length + 1)
                user32.GetWindowTextW(hwnd, buf, length + 1)
                title = buf.value

            pid = ctypes.wintypes.DWORD()
            user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
            proc_name = self._get_process_name(pid.value)
            app_name  = APP_NAMES.get(proc_name.lower(), self._clean_process_name(proc_name))
            clean_title = self._clean_title(title, app_name)
            return proc_name, app_name, clean_title
        except Exception:
            return "explorer.exe", "Рабочий стол", ""

    def _get_process_name(self, pid):
        try:
            handle = kernel32.OpenProcess(0x0400 | 0x0010, False, pid)
            if not handle:
                return "unknown.exe"
            buf  = ctypes.create_unicode_buffer(260)
            size = ctypes.wintypes.DWORD(260)
            ctypes.windll.psapi.GetModuleFileNameExW(handle, None, buf, size)
            kernel32.CloseHandle(handle)
            return os.path.basename(buf.value) if buf.value else "unknown.exe"
        except Exception:
            return "unknown.exe"

    def _clean_title(self, title, app_name):
        if not title:
            return ""
        for suffix in [" \u2014 Google Chrome", " - Google Chrome",
                       " \u2014 Mozilla Firefox", " - Mozilla Firefox",
                       " \u2014 Microsoft Edge", " - Microsoft Edge",
                       " \u2014 Opera", " - Opera", " - Brave"]:
            if title.endswith(suffix):
                title = title[:-len(suffix)]
                break
        return title[:120]

    def _clean_process_name(self, name):
        return name.replace(".exe", "").replace(".EXE", "").capitalize() or "Неизвестно"
