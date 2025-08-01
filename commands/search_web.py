# file: commands/search_web.py

import webbrowser
from assistant.speak import speak

def handle(command):
    """
    Parses a search command, extracts the search query, and opens it in a web browser.
    """
    try:
        # First, remove the longer phrase "search for" to avoid conflicts.
        # Then, remove the shorter word "search".
        search_term = command.replace("search for", "").replace("search", "").strip()

        if search_term:
            speak(f"Searching the web for {search_term}")
            # Construct the Google search URL
            url = f"https://www.google.com/search?q={search_term}"
            webbrowser.open(url)
        else:
            # This handles cases where the user just says "search"
            speak("What would you like me to search for?")
            
    except Exception as e:
        print(f"An error occurred in search_web.handle: {e}")
        speak("Sorry, I couldn't perform the web search.")

