import time
import re
from listen import listen
from speak import speak
import commands.open_app as open_app
import commands.search_web as search_web
import commands.tell_time as tell_time
import commands.wikipedia_lookup as wiki

# --- Configuration ---
ACTIVATION_PHRASE = "hey eva"
INACTIVITY_TIMEOUT = 15  # Seconds to wait for a command before sleeping

def main():
    """
    Main function to run the EVA assistant.
    The assistant waits for an activation phrase ("Hey Eva"), then listens for commands.
    If no command is given within the timeout period, it goes back to sleep.
    """
    speak("EVA is ready. Say 'Hey Eva' to begin.")

    while True:
        # Step 1: Listen for the activation phrase in a low-power mode
        command = listen()
        print("Heard:", command)  # Debug output

        # Normalize and clean the command text
        command_cleaned = re.sub(r'[^\w\s]', '', command.lower())

        if ACTIVATION_PHRASE in command_cleaned:
            speak("Eva here. How can I help?")
            time.sleep(1)  # Optional delay
            last_active_time = time.time()

            # Step 2: Enter the active listening loop
            while True:
                # Check if the inactivity timeout has been reached
                if time.time() - last_active_time > INACTIVITY_TIMEOUT:
                    speak("No commands received. Going back to sleep.")
                    break

                command = listen()
                print("Command received:", command)  # Debug output

                if not command:
                    continue

                # Reset inactivity timer
                last_active_time = time.time()

                command_lower = command.lower()

                # Step 3: Handle the received command
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
                    break
                elif "exit" in command_lower or "bye" in command_lower:
                    speak("Goodbye, Meet!")
                    return
                else:
                    speak("Sorry, I didn't catch that. Could you please repeat?")

if __name__ == "__main__":
    main()
