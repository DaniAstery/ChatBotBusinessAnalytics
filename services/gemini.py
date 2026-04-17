from google import genai
from config import GEMINI_API_KEY

# ✅ define client HERE (global)
client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """
You are a business assistant AI for a company.
Your job:
- help customers clearly
- be short and professional
- if user shows buying intent, guide them to pricing or contact
- never give long unnecessary answers
"""

def ask_gemini(message):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=SYSTEM_PROMPT + "\n\nUser: " + message
    )

    return response.text