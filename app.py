from flask import Flask, render_template, request, jsonify
from spam_detector import check_spam_message
from scam_checker import check_phone_number, check_high_risk_links
from firebase_utils import add_scam_message
from emotional_support import get_emotional_support

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/check_phone", methods=["POST"])
def check_phone():
    phone_number = request.form.get("phone_number")
    result = check_phone_number(phone_number)
    return jsonify({"result": result})

@app.route("/check_url", methods=["POST"])
def check_url():
    url = request.form.get("url")
    result = check_high_risk_links(url)
    return jsonify(result)

@app.route("/check_spam_message", methods=["POST"])
def check_spam_message_api():
    message = request.form.get("message")
    result = check_spam_message(message)
    return jsonify({"result": result})

@app.route("/add_spam_message", methods=["POST"])
def add_spam_message_api():
    message = request.form.get("message")
    label = request.form.get("label", "spam")

    if not message:
        return jsonify({"error": "Message is required"}), 400

    add_scam_message(message, label)
    return jsonify({"success": "Message added successfully"}), 200

@app.route("/emotional_support", methods=["POST"])
def emotional_support():
    user_input = request.form.get("user_input")
    response = get_emotional_support(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
