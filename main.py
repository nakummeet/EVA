import time
import re
from assistant.listen import listen
from assistant.speak import speak
from assistant.gemini_chat import handle_gemini
from assistant.chat_ui import ChatWindow

# Command modules
import commands.open_app as open_app
import commands.search_web as search_web
import commands.tell_time as tell_time
import commands.wikipedia_lookup as wiki

# Configuration
from config import ACTIVATION_PHRASE, INACTIVITY_TIMEOUT


def main():
    """
    Main loop for the EVA AI assistant.
    Listens for the activation phrase and handles user commands via speech.
    Outputs responses via both voice and desktop popup.
    """
    # Create chat UI instance
    chat_ui = ChatWindow()
    chat_ui.show()

    # Initial welcome
    speak("EVA is ready. Say 'Hey Eva' to begin.")
    chat_ui.add_message("🤖 EVA", "EVA is ready. Say 'Hey Eva' to begin.")

    while True:
        # Step 1: Passive listening
        command = listen()
        print("Heard:", command)
        command_cleaned = re.sub(r"[^\w\s]", "", command.lower())

        if ACTIVATION_PHRASE in command_cleaned:
            speak("Eva here. How can I help?")
            chat_ui.add_message("🤖 EVA", "Eva here. How can I help?")
            time.sleep(0.5)

            last_active_time = time.time()

            # Step 2: Active command loop
            while True:
                # Check for inactivity
                if time.time() - last_active_time > INACTIVITY_TIMEOUT:
                    speak("No commands received. Going back to sleep.")
                    chat_ui.add_message("🤖 EVA", "No commands received. Going back to sleep.")
                    break

                command = listen()
                print("Command received:", command)

                if not command:
                    continue

                chat_ui.add_message("🧑 You", command)
                last_active_time = time.time()
                command_lower = command.lower()

                # Step 3: Handle commands
                if "open" in command_lower:
                    open_app.handle(command)
                elif "search" in command_lower:
                    search_web.handle(command)
                elif "time" in command_lower:
                    tell_time.handle()
                elif "who is" in command_lower or "what is" in command_lower:
                    wiki.handle(command)
                elif "code" in command_lower or "generate" in command_lower or "write code" in command_lower:
                    speak("Let me write the code for you.")
                    gemini_response = handle_gemini(command)
                    chat_ui.add_message("🤖 EVA (Gemini)", gemini_response)
                    speak("Here's the generated code.")
                elif "go to sleep" in command_lower:
                    speak("Going to sleep.")
                    chat_ui.add_message("🤖 EVA", "Going to sleep.")
                    break
                elif "exit" in command_lower or "bye" in command_lower:
                    speak("Goodbye, Meet!")
                    chat_ui.add_message("🤖 EVA", "Goodbye, Meet!")
                    return
                else:
                    speak("Sorry, I didn't catch that.")
                    chat_ui.add_message("🤖 EVA", "Sorry, I didn't catch that.")


if __name__ == "__main__":
    main()
