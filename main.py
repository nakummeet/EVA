import time
import re

# --- Local Imports ---
# Make sure your project structure has these files and functions.
from assistant.listen import listen
from assistant.speak import speak

# Import all your command handlers
import commands.open_app as open_app
import commands.search_web as search_web
import commands.tell_time as tell_time
import commands.wikipedia_lookup as wiki

# --- Configuration ---
# Import configuration variables from the config.py file.
from config import ACTIVATION_PHRASES, INACTIVITY_TIMEOUT


# --- Command Routing Dictionary ---
# Maps keywords to the function that should handle them.
# This avoids a long if/elif/else chain.
COMMANDS = {
    "open": open_app.handle,
    "search": search_web.handle,
    "who is": wiki.handle,
    "what is": wiki.handle,
    # Use a lambda for commands that don't need the 'command' text as input.
    "time": lambda command: tell_time.handle(),
}

def handle_command(command):
    """
    Parses a command and calls the appropriate handler function.

    Args:
        command (str): The user's command after the activation phrase.

    Returns:
        str or bool: "exit" to terminate, True if handled, False if not recognized.
    """
    # --- FIXED EXIT LOGIC ---
    # We split the command into words to check for exact matches.
    # This prevents parts of other words from accidentally triggering an exit.
    # For example, "explain the word exit" will no longer cause a shutdown.
    command_words = command.split()
    if "exit" in command_words or "bye" in command_words or "goodbye" in command_words:
        speak("Goodbye!")
        print("Exiting program.")
        return "exit"

    for keyword, handler_function in COMMANDS.items():
        if keyword in command:
            handler_function(command)
            return True  # Command was successfully handled

    return False  # No matching command keyword was found

def start_conversational_mode():
    """
    Enters a loop to listen for multiple commands until timeout or sleep command.
    """
    speak("Eva here. How can I help?")
    print("\n--- Conversational Mode Activated ---")
    last_active_time = time.time()

    while True:
        if time.time() - last_active_time > INACTIVITY_TIMEOUT:
            speak("No commands received. Going back to sleep.")
            print("Inactivity timeout. Returning to one-shot mode.")
            break

        command = listen()
        if not command:
            continue

        print(f"Command received: '{command}'")
        last_active_time = time.time()

        if "go to sleep" in command:
            speak("Going to sleep.")
            print("Going to sleep. Returning to one-shot mode.")
            break

        if not handle_command(command):
            speak("Sorry, I don't understand that command.")
            print("Command not recognized in conversational mode.")
    
    print("--- Conversational Mode Deactivated ---\n")

def assistant_main():
    """
    The main loop. Listens for an activation phrase and then delegates the command.
    """
    speak("EVA is ready.")
    print("EVA is ready. Listening for activation phrase...")

    while True:
        full_command = listen()
        if not full_command:
            continue

        triggered_phrase = None
        for phrase in ACTIVATION_PHRASES:
            if phrase in full_command:
                triggered_phrase = phrase
                break
        
        if triggered_phrase:
            print(f"Activation detected: '{full_command}'")
            
            try:
                # Extract the command part after the activation phrase
                actual_command = full_command.split(triggered_phrase, 1)[1].strip()
            except IndexError:
                actual_command = ""

            if not actual_command:
                speak("Hmm")
                continue

            # Check for the command to start the conversational mode
            if actual_command in ("start", "start listening", "let's chat"):
                start_conversational_mode()
                continue

            # Default to one-shot command handling
            result = handle_command(actual_command)
            if result == "exit":
                break
            
            if result is False:
                speak("I'm not sure how to help with that.")
                print(f"Unrecognized one-shot command: '{actual_command}'")

# --- Program Entry Point ---
if __name__ == "__main__":
    try:
        assistant_main()
    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting.")
    except Exception as e:
        print(f"A fatal error occurred: {e}")
