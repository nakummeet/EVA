from google import genai
from config import GEMINI_API_KEY

# Initialize the Gemini client
client = genai.Client(api_key="AIzaSyCYFikXsVpJUiyVw3yZutB5qG61XYIhNPs")
#client = genai.Client(api_key=GEMINI_API_KEY)
#model = genai.GenerativeModel("gemini-1.5-flash")  # or "gemini-1.5-pro" if available

def handle_gemini(prompt):
    """
    Sends the given prompt to Gemini and returns the response text.
    """
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=(prompt)
        )
        print(response)
        return reply # type: ignore
    except Exception as e:
        print("⚠️ Gemini API error:", e)
        return "Sorry, I couldn't generate a response right now."

