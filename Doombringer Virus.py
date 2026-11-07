
import tkinter as tk
import random
import platform
import webbrowser
import datetime

MAX_WINDOWS = 15
SPAWN_MS = 350
BLINK_MS = 300

windows = []
stopped = False
chaos = False
bsod_active = False
browser_count = 0
blink_state = False

root = tk.Tk()
root.withdraw()

def stop_all(event=None):
    global stopped
    stopped = True
    for win in windows[:]:
        try:
            win.destroy()
        except tk.TclError:
            pass
    windows.clear()
    try:
        root.destroy()
    except tk.TclError:
        pass

def close_window(win):
    if win in windows:
        windows.remove(win)
    try:
        win.destroy()
    except tk.TclError:
        pass

def register(win):
    windows.append(win)
    win.protocol("WM_DELETE_WINDOW", lambda w=win: close_window(w))

def idiot_window():
    if stopped or bsod_active or len(windows) >= MAX_WINDOWS:
        return

    win = tk.Toplevel(root)
    register(win)
    win.title("You are an idiot")
    win.geometry("480x380")
    win.configure(bg="black")

    title = tk.Label(
        win, text="You are an idiot",
        font=("Arial", 27, "bold"),
        fg="white", bg="black"
    )
    title.pack(pady=15)

    smile = tk.Label(
        win, text="☺",
        font=("Arial", 180, "bold"),
        fg="white", bg="black"
    )
    smile.pack(expand=True)

    win._flash_widgets = [title, smile]
    win._flash = True

def info_window():
    if stopped or bsod_active or len(windows) >= MAX_WINDOWS:
        return

    win = tk.Toplevel(root)
    register(win)
    win.title("DOOMBRINGER SYSTEM")
    win.geometry("650x400")
    win.configure(bg="black")

    label = tk.Label(
        win, text="",
        font=("Consolas", 15),
        fg="red", bg="black",
        justify="left"
    )
    label.pack(expand=True)

    def update():
        if stopped or bsod_active or not win.winfo_exists():
            return
        now = datetime.datetime.now()
        label.config(text=(
            "DOOMBRINGER // SYSTEM REPORT\n\n"
            f"TIME: {now:%H:%M:%S}\n"
            f"DATE: {now:%Y-%m-%d}\n"
            f"OS: {platform.system()}\n"
            f"VERSION: {platform.release()}\n"
            "DISK SCAN: SIMULATED\n"
            "PERSONAL DATA: NOT COLLECTED"
        ))
        win.after(1000, update)

    update()

def spawn_loop():
    if stopped or bsod_active or not chaos:
        return
    if len(windows) < MAX_WINDOWS:
        idiot_window()
    root.after(SPAWN_MS, spawn_loop)

def blink_loop():
    global blink_state

    if stopped or bsod_active:
        return

    blink_state = not blink_state

    for win in windows[:]:
        try:
            if not win.winfo_exists():
                continue
            if hasattr(win, "_flash_widgets"):
                win._flash = not win._flash
                bg = "#b00000" if win._flash else "black"
                fg = "black" if win._flash else "white"
                win.configure(bg=bg)
                for widget in win._flash_widgets:
                    widget.configure(bg=bg, fg=fg)
        except tk.TclError:
            pass

    root.after(BLINK_MS, blink_loop)

def start_chaos():
    global chaos
    if chaos or stopped:
        return
    chaos = True
    idiot_window()
    idiot_window()
    info_window()
    spawn_loop()
    blink_loop()

def show_bsod():
    global bsod_active

    if stopped or bsod_active:
        return

    bsod_active = True

    # Pause all existing windows without destroying them.
    for win in windows:
        try:
            win.withdraw()
        except tk.TclError:
            pass

    bsod = tk.Toplevel(root)
    bsod.title("Windows")
    bsod.configure(bg="#0078D7")
    bsod.attributes("-fullscreen", True)
    bsod.attributes("-topmost", True)

    blue = "#0078D7"
    white = "white"

    frame = tk.Frame(bsod, bg=blue)
    frame.place(relx=0.17, rely=0.13, relwidth=0.68, relheight=0.78)

    tk.Label(
        frame, text=":(",
        font=("Segoe UI", 105),
        fg=white, bg=blue
    ).pack(anchor="w")

    tk.Label(
        frame,
        text="Your device ran into a problem and needs to restart.",
        font=("Segoe UI", 25),
        fg=white, bg=blue
    ).pack(anchor="w", pady=(5, 15))

    tk.Label(
        frame,
        text="We're just collecting some error info, and then we'll restart for you.",
        font=("Segoe UI", 15),
        fg=white, bg=blue
    ).pack(anchor="w")

    percent = tk.Label(
        frame, text="0% complete",
        font=("Segoe UI", 15),
        fg=white, bg=blue
    )
    percent.pack(anchor="w", pady=20)

    tk.Label(
        frame,
        text=(
            "For more information about this issue and possible fixes, visit:\n"
            "https://www.windows.com/stopcode\n\n"
            "Stop code: CRITICAL_PROCESS_DIED"
        ),
        font=("Segoe UI", 11),
        fg=white, bg=blue,
        justify="left"
    ).pack(anchor="w", pady=10)

    progress = 0

    def update_percent():
        nonlocal progress
        if stopped or not bsod.winfo_exists():
            return

        progress = min(100, progress + random.randint(1, 4))
        percent.config(text=f"{progress}% complete")

        if progress < 100:
            bsod.after(1200, update_percent)

    update_percent()

    def resume():
        global bsod_active
        bsod_active = False
        try:
            bsod.destroy()
        except tk.TclError:
            pass

        for win in windows[:]:
            try:
                if win.winfo_exists():
                    win.deiconify()
            except tk.TclError:
                pass

        if chaos:
            spawn_loop()
            blink_loop()

    bsod.bind("<Escape>", lambda event: resume())
    bsod.protocol("WM_DELETE_WINDOW", resume)

def warning_window():
    if stopped or bsod_active:
        return

    if len(windows) < MAX_WINDOWS:
        win = tk.Toplevel(root)
        register(win)
        win.title("CRITICAL SYSTEM WARNING")
        win.geometry("500x220")
        win.configure(bg="black")

        tk.Label(
            win,
            text=random.choice([
                "CRITICAL ERROR",
                "SYSTEM FAILURE",
                "ACCESS DENIED",
                "UNKNOWN PROCESS",
                "SECURITY WARNING"
            ]),
            font=("Consolas", 23, "bold"),
            fg="red", bg="black"
        ).pack(expand=True)

    root.after(random.randint(8000, 16000), warning_window)

def browser_random():
    global browser_count

    if stopped or bsod_active or browser_count >= 5:
        return

    browser_count += 1
    query = random.choice([
        "funny cat videos",
        "Windows error sounds",
        "computer memes",
        "You are an idiot meme"
    ])

    try:
        webbrowser.open(
            "https://www.google.com/search?q=" +
            query.replace(" ", "+")
        )
    except Exception:
        pass

    root.after(random.randint(18000, 35000), browser_random)

def initial_window():
    win = tk.Toplevel(root)
    register(win)
    win.title("DOOMBRINGER")
    win.geometry("800x500")
    win.configure(bg="#cc0000")

    tk.Label(
        win,
        text="DOOMBRINGER",
        font=("Arial", 44, "bold"),
        fg="black", bg="#cc0000"
    ).pack(pady=75)

    tk.Label(
        win,
        text="CRITICAL SYSTEM WARNING",
        font=("Arial", 23, "bold"),
        fg="black", bg="#cc0000"
    ).pack()

    def begin():
        close_window(win)
        start_chaos()

    win.protocol("WM_DELETE_WINDOW", begin)

root.bind_all("<Alt-Shift-Return>", stop_all)
root.bind_all("<Alt-Shift-KP_Enter>", stop_all)

initial_window()

root.after(12000, warning_window)
root.after(25000, show_bsod)
root.after(5000, browser_random)

root.mainloop()
