from datetime import datetime
from assistant.speak import speak

def handle():
    time = datetime.now().strftime("%I:%m %p")
    speak("Current time is " + time)