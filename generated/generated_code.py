# commands/generate_code.py

from assistant.gemini_chat import handle_gemini
from assistant.speak import speak

def handle(command):
    """
    Handle code generation requests using Gemini.
    """
    speak("Generating code, please wait...")
    response = handle_gemini(command)

    # Speak only summary, not the whole code
    speak("Here is the generated code. I've displayed it on your screen.")

    # Show the generated code in console or GUI
    print("\n🔧 Generated Code:\n")
    print(response)

    # Optional: Save to a file or show in popup
    with open("generated_code.py", "w", encoding="utf-8") as file:
        file.write(response)

    return response
