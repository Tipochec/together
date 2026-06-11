"""
Together - приложение для пар
"""
import threading
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.tracker import ActivityTracker
from core.network import NetworkManager
from core.autostart import setup_autostart
from core.tray import TrayApp
from core.stats import StatsTracker


def main():
    setup_autostart()

    tracker = ActivityTracker()
    network = NetworkManager(tracker)
    stats   = StatsTracker(tracker)

    app = TrayApp(tracker, network)
    threading.Thread(target=app.run,       daemon=True).start()
    threading.Thread(target=tracker.start, daemon=True).start()
    threading.Thread(target=network.start, daemon=True).start()
    threading.Thread(target=stats.start,   daemon=True).start()

    from ui.window import run_webview_loop
    run_webview_loop(tracker, network, stats)


if __name__ == "__main__":
    main()
