import os
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from google import genai
from chatbot_config import MODEL_NAME, SYSTEM_PROMPT

load_dotenv()

app = Flask(__name__)

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not set in the .env file.")

client = genai.Client(api_key=api_key)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()

    if not message:
        return jsonify({"error": "Please enter a question."}), 400

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=message,
            config={
                "system_instruction": SYSTEM_PROMPT,
                "thinking_config": {"thinking_level": "minimal"},
            },
        )
        answer = (response.text or "").strip()
        return jsonify({"answer": answer or "I could not generate a response. Please try again."})
    except Exception:
        return jsonify({
            "error": "Unable to connect to Gemini right now. Please check your API key and try again."
        }), 500

if __name__ == "__main__":
    app.run(debug=True)
