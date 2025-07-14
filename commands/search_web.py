# commands/search_web.py
import webbrowser
from speak import speak

def handle(query):
    query = query.replace("search", "").strip()
    if query:
        speak(f"Searching in web {query}")
        webbrowser.open(f"https://www.google.com/search?q={query}")

    else :
        speak("Please say ehat you want to search")
