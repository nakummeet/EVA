# file: assistant/listen.py

import speech_recognition as sr

# Initialize the recognizer. It can be reused.
recognizer = sr.Recognizer()

# --- You can fine-tune these settings ---
# `pause_threshold`: How long it waits for silence before considering a phrase complete.
recognizer.pause_threshold = 1.5 

# `energy_threshold`: How sensitive the microphone is to speech.
# Adjust this value based on your microphone and room noise.
recognizer.energy_threshold = 1500

def listen():
    """
    Listens for a single user command from the microphone.

    This function now re-initializes the microphone each time it's called
    to ensure the audio buffer is cleared, preventing recognition of old audio.

    Returns:
        str: The recognized text from the user's speech, or an empty string.
    """
    # By creating a new Microphone instance inside the function,
    # we ensure we get a fresh audio stream every time.
    with sr.Microphone() as source:
        
        print("\nListening...")
        
        try:
            # Listen for audio input.
            # `timeout=5`: How long to wait for speech to start.
            # `phrase_time_limit=10`: The maximum length of a phrase.
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            print("Recognizing...")
            # Use Google's online speech recognition service.
            command = recognizer.recognize_google(audio)
            
            # Return the command in lowercase for easier matching.
            return command.lower()

        except sr.WaitTimeoutError:
            # This is not an error, it just means the user was silent.
            return ""
            
        except sr.UnknownValueError:
            # This means the API couldn't understand the audio.
            print("Could not understand the audio.")
            return ""

        except sr.RequestError as e:
            # This means there's a problem with the API (e.g., no internet).
            print(f"API Error: Could not request results from Google; {e}")
            return ""
