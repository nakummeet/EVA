# listen.py
import speech_recognition as sr

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("🔍 Recognizing...")
        command = r.recognize_google(audio, language='en-in')
        print(f"🗣 You said: {command}")
        return command.lower()
    except Exception as e:
        print("❌ Could not recognize:", e)
        return ""
