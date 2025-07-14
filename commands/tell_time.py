from datetime import datetime
from speak import speak

def handle():
    time = datetime.now().strftime("%I:%m %p")
    speak("Current time is " + time)