from flask import Flask, request, jsonify
from services.router import route_message
from services.gemini import ask_gemini
from services.leads import save_lead
from services.formatter import format_response
from services.logger import log_message
from services.analytics import track_event, get_stats
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
user_sessions = {}
@app.route("/stats", methods=["GET"])
def stats():
    return get_stats()
    

@app.route("/chat", methods=["POST"])
def chat():

    data = request.json
    message = data.get("message")
    user = data.get("user", {})

    route = route_message(message)

    # 💰 SALES
    if route == "sales":
        
        reply = "Great! What product are you interested in?"
        log_message(user, message, "sales")
        track_event("sales")
        return jsonify(format_response(reply, "sales"))
    

    # 🧑‍💼 LEAD
    if route == "lead":

        name = user.get("name")
        contact = user.get("phone") or user.get("email")

        # ✅ If user info already exists → SAVE
        if name and contact:
            save_lead(user)

            reply = "Thanks! Our team will contact you soon."
            log_message(user, message, "lead")
            track_event("lead")

            return jsonify(format_response(reply, "lead"))

        # ❗ If info missing → ASK for it
        else:
            missing = []

            if not name:
                missing.append("name")

            if not contact:
                missing.append("phone number or email")

            ask_text = "Please provide your " + " and ".join(missing) + " so we can assist you."

            return jsonify(format_response(ask_text, "lead"))
        
       
    # 🛠️ SUPPORT
    if route == "support":
        reply = "I understand your issue. Please explain more."
        log_message(user, message, "support")
        track_event("support")      
        return jsonify(format_response(reply, "support"))
       
    # 🤖 AI
    ai_reply = ask_gemini(message)
    log_message(user, message, "ai")
    track_event("ai")
    return jsonify(format_response(ai_reply, "ai"))

if __name__ == "__main__":
    app.run(debug=True)




    