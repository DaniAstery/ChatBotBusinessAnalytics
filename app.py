from flask import request, jsonify
from services.leads import save_lead
from services.gemini import ask_gemini
from services.logger import log_message, track_event
from services.formatter import format_response
from router import route_message

user_sessions = {}

@app.route("/chat", methods=["POST"])
def chat():

    # 1️⃣ Request data
    data = request.json
    message = data.get("message")
    user = data.get("user", {})

    # 2️⃣ Session setup
    session_id = data.get("session_id", "default")

    if session_id not in user_sessions:
        user_sessions[session_id] = {}

    session = user_sessions[session_id]

    # ✅ Safe init
    session.setdefault("waiting_for_lead", False)
    session.setdefault("data", {})

    # 🧠 ROUTING
    route = route_message(message)

    # =========================
    # 🧑‍💼 LEAD FLOW
    # =========================
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

    # =========================
    # 💰 SALES
    # =========================
    if route == "sales":
        reply = "Great! What product are you interested in?"
        log_message(user, message, "sales")
        track_event("sales")
        return jsonify(format_response(reply, "sales"))

    # =========================
    # 🛠️ SUPPORT
    # =========================
    if route == "support":
        reply = "I understand your issue. Please explain more."
        log_message(user, message, "support")
        track_event("support")
        return jsonify(format_response(reply, "support"))

    # =========================
    # 🤖 AI FALLBACK
    # =========================
    ai_reply = ask_gemini(message)
    log_message(user, message, "ai")
    track_event("ai")

    return jsonify(format_response(ai_reply, "ai"))