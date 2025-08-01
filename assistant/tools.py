# assistant/tools.py
import webbrowser
import pyautogui
import time
from datetime import datetime
import wikipedia

# IMPORTANT: This function helps the main script call the right tool
def get_available_tools():
    """Returns a dictionary mapping tool names to their functions."""
    return {
        "tell_time": tell_time,
        "search_web": search_web,
        "open_app": open_app,
        "wikipedia_lookup": wikipedia_lookup,
    }

# --- Tool Definitions ---

def tell_time(query: str = ""):
    """
    Tells the current time.
    Returns: A string with the current time.
    """
    now = datetime.now()
    current_time = now.strftime("%I:%M %p")
    return f"The current time is {current_time}."

def search_web(query: str):
    """
    Searches the web using Google.
    Args:
        query (str): The search term.
    Returns: A string confirming the search has started.
    """
    search_url = f"https://www.google.com/search?q={query}"
    webbrowser.open(search_url)
    return f"I have started a search for '{query}' in your browser."

def open_app(app_name: str):
    """
    Opens an application on the computer by typing its name in the search bar.
    Args:
        app_name (str): The name of the application to open (e.g., 'notepad', 'chrome').
    Returns: A string confirming the action.
    """
    try:
        pyautogui.press('win')
        time.sleep(1)
        pyautogui.write(app_name)
        time.sleep(1)
        pyautogui.press('enter')
        return f"I am opening {app_name}."
    except Exception as e:
        print(f"Error opening app: {e}")
        return "Sorry, I couldn't open that application."

def wikipedia_lookup(query: str):
    """
    Looks up a topic on Wikipedia.
    Args:
        query (str): The topic to look up.
    Returns: A summary of the Wikipedia page or an error message.
    """
    try:
        # Clean the query for better search results
        cleaned_query = query.replace("who is", "").replace("what is", "").replace("look up", "").strip()
        summary = wikipedia.summary(cleaned_query, sentences=2)
        return summary
    except wikipedia.exceptions.PageError:
        return f"Sorry, I could not find a Wikipedia page for '{cleaned_query}'."
    except wikipedia.exceptions.DisambiguationError as e:
        return f"That query is ambiguous. It could refer to: {e.options[:3]}. Please be more specific."
    except Exception as e:
        print(f"Error with Wikipedia lookup: {e}")
        return "Sorry, I encountered an error while looking that up."