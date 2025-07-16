import time
import re
from threading import Thread

from assistant.listen import listen
from assistant.speak import speak
from assistant.gemini_chat import handle_gemini
from assistant.chat_ui import ChatWindow

import commands.open_app as open_app
import commands.search_web as search_web
import commands.tell_time as tell_time
import commands.wikipedia_lookup as wiki

from config import ACTIVATION_PHRASE, INACTIVITY_TIMEOUT


def assistant_main(chat_ui):
    speak("EVA is ready. Say 'Hey Eva' to begin.")
    chat_ui.add_message("🤖 EVA", "EVA is ready. Say 'Hey Eva' to begin.")

    while True:
        # Wait for activation phrase
        command = listen()
        print("Heard:", command)
        command_cleaned = re.sub(r"[^\w\s]", "", command.lower())

        if ACTIVATION_PHRASE in command_cleaned:
            speak("Eva here. How can I help?")
            chat_ui.add_message("🤖 EVA", "Eva here. How can I help?")
            time.sleep(0.5)

            last_active_time = time.time()

            while True:
                # Timeout if user is inactive
                if time.time() - last_active_time > INACTIVITY_TIMEOUT:
                    speak("No commands received. Going back to sleep.")
                    chat_ui.add_message("🤖 EVA", "No commands received. Going back to sleep.")
                    break

                # Listen for user command
                command = listen()
                print("Command received:", command)

                if not command:
                    continue

                chat_ui.add_message("🧑 You", command)
                last_active_time = time.time()
                command_lower = command.lower()

                # Handle predefined commands
                if "open" in command_lower:
                    open_app.handle(command)
                elif "search" in command_lower:
                    search_web.handle(command)
                elif "time" in command_lower:
                    tell_time.handle()
                elif "who is" in command_lower or "what is" in command_lower:
                    wiki.handle(command)
                elif "go to sleep" in command_lower:
                    speak("Going to sleep.")
                    chat_ui.add_message("🤖 EVA", "Going to sleep.")
                    break
                elif "exit" in command_lower or "bye" in command_lower:
                    speak("Goodbye!")
                    chat_ui.add_message("🤖 EVA", "Goodbye!")
                    return
                else:
                    # Fallback to Gemini for general queries
                    speak("Let me check that for you.")
                    try:
                        gemini_response = handle_gemini(command)
                        chat_ui.add_message("🤖 EVA (Gemini)", gemini_response)
                        speak("Here’s what I found.", gemini_response)
                    except Exception as e:
                        error_msg = f"Something went wrong with Gemini: {e}"
                        print(error_msg)
                        chat_ui.add_message("🤖 EVA", error_msg)
                        speak("Sorry, I encountered an error.")

# Entry point
if __name__ == "__main__":
    chat_ui = ChatWindow()
    chat_ui.show()  # Show window before starting assistant

    # Run assistant in a background thread
    Thread(target=assistant_main, args=(chat_ui,), daemon=True).start()

    # Keep the GUI running
    chat_ui.run()
