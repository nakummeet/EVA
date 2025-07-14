import pyttsx3

def speak(text):
    print("🤖 EVA:", text)
    engine = pyttsx3.init()  # Re-initialize every time
    engine.say(text)
    engine.runAndWait()
    engine.stop()  # Cleanly stop the engine
