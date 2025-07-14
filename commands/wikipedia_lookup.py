import wikipedia
from assistant.speak import speak

def handle(command):
    query = command.replace("who is", "").replace("what is", "")
    try:
        result = wikipedia.summary(query, sentences=2)
        speak(result)
    except:
        speak("Sorry, I couldn't find information.")
