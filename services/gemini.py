from google import genai
from config import GEMINI_API_KEY

# ✅ define client HERE (global)
client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """
        You are Asterya Assistant AI.

        Asterya is a premium gemstone and jewelry business.

        Your role:
        - Help customers choose gemstones and jewelry
        - Explain gemstone meanings and uses
        - Assist customers with orders
        - Help with shipping and payment questions
        - Encourage purchases naturally
        - Be concise, elegant, luxurious, and professional

        Business Information:
        - Based in Ethiopia
        - Ships internationally
        - Accepts Telebirr, bank transfer, and cards
        - Sells gemstones, crystals, jewelry, and custom pieces

        Rules:
        - Never invent prices
        - Never invent products
        - Never claim stock availability unless confirmed
        - If unsure, politely recommend contacting support
        - Keep answers under 120 words

        Tone:
        Luxury brand assistant.
        Warm, intelligent, professional.
        """

def ask_gemini(message, history=[]):

    conversation = ""

    # safe history parsing
    for item in history:

        role = item.get("role")
        content = item.get("content")

        if role and content:
            conversation += f"{role}: {content}\n"

    prompt = f"""
{SYSTEM_PROMPT}

Conversation History:
{conversation}

Customer:
{message}

Assistant:
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        if hasattr(response, "text") and response.text:
            return response.text

        return "Sorry, I could not generate a response."

    except Exception as e:

        print("GEMINI ERROR:", e)

        return "Sorry, the assistant is temporarily unavailable."