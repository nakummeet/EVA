import os
import subprocess
import winshell
from assistant.speak import speak 

def handle(command):
    command = command.lower()

    if "open notepad" in command:
        speak("Opening Notepad")
        os.system("notepad")

    elif "open chrome" in command:
        speak("Opening Google Chrome")
        os.system("start chrome")

    elif "open recycle bin" in command:
        speak("Opening Recycle Bin")
        subprocess.Popen('explorer.exe shell:RecycleBinFolder')

    elif "empty recycle bin" in command or "delete recycle bin" in command:
        speak("Emptying Recycle Bin")
        try:
            winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=True)
            speak("Recycle Bin emptied successfully")
        except Exception as e:
            speak("Failed to empty Recycle Bin")
            print(str(e))

    elif "open command prompt" in command:
        speak("Opening Command Prompt")
        os.system("start cmd")

    elif "open calculator" in command:
        speak("Opening Calculator")
        os.system("calc")

    elif "shutdown" in command:
        speak("Shutting down the system")
        os.system("shutdown /s /t 5")

    elif "restart" in command:
        speak("Restarting the system")
        os.system("shutdown /r /t 5")

    elif "log off" in command:
        speak("Logging off")
        os.system("shutdown /l")

    elif "open vscode" in command:
        speak("Opening Visual Studio Code")
        os.system("code")  # Assumes VS Code is in PATH

    else:
        speak("Sorry, I don't understand the command.")
