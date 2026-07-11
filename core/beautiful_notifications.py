"""
Красивые всплывающие уведомления вместо системных toast.
Работает через tkinter — лёгкий, кастомный, без системных звуков.
"""
import threading
import tkinter as tk
from tkinter import font

# Очередь уведомлений (чтобы не накладывались)
_notification_queue = []
_queue_lock = threading.Lock()
_is_showing = False


def show_beautiful_notification(text, duration=3000):
    """
    Показать красивое уведомление в правом нижнем углу.
    text — текст уведомления.
    duration — мс, сколько показывать.
    """
    with _queue_lock:
        _notification_queue.append((text, duration))
    
    if not _is_showing:
        _process_queue()


def _process_queue():
    global _is_showing
    with _queue_lock:
        if not _notification_queue:
            _is_showing = False
            return
        text, duration = _notification_queue.pop(0)
        _is_showing = True
    
    # Показываем в отдельном потоке
    threading.Thread(target=_show_window, args=(text, duration), daemon=True).start()


def _show_window(text, duration):
    """Создать окно-уведомление"""
    root = tk.Tk()
    root.overrideredirect(True)  # Без рамки
    root.attributes("-topmost", True)  # Поверх всех окон
    
    # Прозрачный фон
    root.configure(bg="white")
    root.attributes("-transparentcolor", "white")
    
    # Размер и позиция (правый нижний угол)
    width, height = 360, 70
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = screen_width - width - 30
    y = screen_height - height - 30
    root.geometry(f"{width}x{height}+{x}+{y}")
    
    # Основной фрейм с закруглениями
    frame = tk.Frame(
        root,
        bg="#1a1820",
        highlightthickness=1,
        highlightcolor="rgba(255,255,255,0.1)",
        highlightbackground="rgba(255,255,255,0.1)",
    )
    frame.pack(fill="both", expand=True, padx=2, pady=2)
    
    # Текст сообщения
    label = tk.Label(
        frame,
        text=text,
        bg="#1a1820",
        fg="#e8e6f0",
        font=("Segoe UI", 11),
        wraplength=320,
        justify="left",
        padx=16,
        pady=16,
    )
    label.pack(fill="both", expand=True)
    
    # Анимация появления (плавное затухание)
    root.attributes("-alpha", 0.0)
    
    def fade_in():
        alpha = 0.0
        while alpha < 1.0:
            alpha += 0.05
            root.attributes("-alpha", alpha)
            root.update()
            root.after(20)
    
    def fade_out():
        alpha = 1.0
        while alpha > 0.0:
            alpha -= 0.05
            root.attributes("-alpha", alpha)
            root.update()
            root.after(20)
        root.destroy()
        # Показать следующее уведомление
        _process_queue()
    
    # Сначала плавно появляемся
    fade_in()
    
    # Через duration мс плавно исчезаем
    root.after(duration, fade_out)
    
    # Клик по уведомлению закрывает его сразу
    root.bind("<Button-1>", lambda e: fade_out())
    
    root.mainloop()