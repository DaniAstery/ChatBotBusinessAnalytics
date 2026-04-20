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
user_sessions= {};
@app.route("/stats", methods=["GET"])
def stats():
    return get_stats()
    

@app.route("/chat", methods=["POST"])
def chat():

    data = request.json
    message = data.get("message")
    user = data.get("user", {})

     # 2️⃣ session id
    session_id = data.get("session_id", "default")

    # 3️⃣ create session if not exists
    if session_id not in user_sessions:
        user_sessions[session_id] = {}

    # 4️⃣ NOW define session ✅
    session = user_sessions[session_id]

    # 5️⃣ NOW safe to use setdefault ✅
    session.setdefault("waiting_for_lead", False)
    session.setdefault("data", {})


    route = route_message(message)

    # 💰 SALES
    if route == "sales":
        
        reply = "Great! What product are you interested in?"
        log_message(user, message, "sales")
        track_event("sales")
        return jsonify(format_response(reply, "sales"))
    

       if route == "lead":

        # 🔹 START FLOW
        if session["waiting_for_lead"] is False:
            session["waiting_for_lead"] = True
            session["data"] = {}

            return jsonify(format_response(
                "Great! What is your name?",
                "lead"
            ))

        # 🔹 STEP 1: NAME
        if "name" not in session["data"]:
            session["data"]["name"] = message

            return jsonify(format_response(
                "Please provide your phone number or email.",
                "lead"
            ))

        # 🔹 STEP 2: CONTACT + SAVE
        if "contact" not in session["data"]:
            session["data"]["contact"] = message

            # ✅ FIX: map fields for sheet
            session["data"]["phone"] = session["data"]["contact"]
            session["data"]["interest"] = "gemstone"

            print("ABOUT TO SAVE:", session["data"])

            try:
                save_lead(session["data"])
                print("SAVED SUCCESSFULLY")
            except Exception as e:
                print("SAVE ERROR:", e)

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




    