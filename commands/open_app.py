# file: commands/open_app.py

import pyautogui
import time
from assistant.speak import speak

def _execute_open(app_name):
    """The core logic to open an application."""
    try:
        # Press Windows key to open the Start Menu/Search
        pyautogui.press('win')
        time.sleep(1)

        # Type the app name
        pyautogui.write(app_name, interval=0.1)
        time.sleep(1)

        # Press Enter to open the app
        pyautogui.press('enter')

        speak(f"Opening {app_name}")
    except Exception as e:
        error_msg = f"Sorry, I encountered an error trying to open {app_name}."
        print(f"Error: {e}")
        speak(error_msg)

def handle(command):
    """
    Parses the command to extract the application name and then opens it.
    Example: "open notepad" -> "notepad"
    """
    try:
        # Splits the command string by "open " and takes the second part [1]
        # .strip() removes any leading/trailing whitespace
        app_name = command.lower().split("open", 1)[1].strip()
        
        if app_name:
            _execute_open(app_name)
        else:
            speak("You said 'open', but didn't specify which application.")
    except IndexError:
        speak("I didn't catch which application you want to open.")