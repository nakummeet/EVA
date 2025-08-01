import pyautogui
import subprocess
import psutil
from assistant.speak import speak

def close_app_by_name(app_name):
    app_name = app_name.lower()
    closed = False

    for proc in psutil.process_iter(['name']):
        try:
            if app_name in proc.info['name'].lower():
                proc.terminate()
                closed = True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    if closed:
        speak(f"{app_name} closed successfully.")
    else:
        speak(f"Couldn't find or close {app_name}.")


def handle(command):
    command = command.lower()

    if "close" in command:
        pyautogui.hotkey("alt", "f4")
        speak("Closed the current window.")

    elif "select all" in command:
        pyautogui.hotkey("ctrl", "a")
        speak("Selected all.")

    elif "copy" in command:
        pyautogui.hotkey("ctrl", "c")
        speak("Copied.")

    elif "paste" in command:
        pyautogui.hotkey("ctrl", "v")
        speak("Pasted.")

    elif "cut" in command:
        pyautogui.hotkey("ctrl", "x")
        speak("Cut to clipboard.")

    elif "minimize" in command:
        pyautogui.hotkey("win", "down")
        speak("Window minimized.")

    elif "maximize" in command:
        pyautogui.hotkey("win", "up")
        speak("Window maximized.")

    elif "file explorer" in command:
        subprocess.Popen("explorer")
        speak("Opening File Explorer.")

    elif "screenshot" in command:
        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot.png")
        speak("Screenshot taken and saved.")

    else:
        speak("Sorry, I don't recognize that command.")