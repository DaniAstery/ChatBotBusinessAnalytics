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
session= {};
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
    

    if route == "lead":

    # initialize session if needed
        if session["waiting_for_lead"] is False:
            session["waiting_for_lead"] = True
            session["data"] = {}

            return jsonify(format_response(
                "Great! What is your name?",
                "lead"
            ))

        # step 1 → collect name
        if "name" not in session["data"]:
            session["data"]["name"] = message

            return jsonify(format_response(
                "Please provide your phone number or email.",
                "lead"
            ))

        # step 2 → collect contact + SAVE
        if "contact" not in session["data"]:
            session["data"]["phone"] = message
            save_lead(session["data"])  
            # reset session
            session["waiting_for_lead"] = False
            session["data"] = {}

            return jsonify(format_response(
                "Thanks! Our team will contact you soon.",
                "lead"
            ))
    
    
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




    