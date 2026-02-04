from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Placeholder for Groq AI API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@app.route('/')
def index():
    return "BizTone Converter Backend is running!"

@app.route('/api/convert', methods=['POST'])
def convert_text():
    if not GROQ_API_KEY:
        return jsonify({"error": "GROQ_API_KEY not set"}), 500

    data = request.get_json()
    original_text = data.get('text')
    target_persona = data.get('target_persona') # e.g., '상사', '동료', '고객'

    if not original_text or not target_persona:
        return jsonify({"error": "Missing 'text' or 'target_persona' in request"}), 400

    # TODO: Implement actual Groq AI API call here
    # For now, a dummy response
    if target_persona == "상사":
        converted_text = f"상사에게 보고하는 말투로 변환된 내용: {original_text}"
    elif target_persona == "동료":
        converted_text = f"동료에게 전달하는 말투로 변환된 내용: {original_text}"
    elif target_persona == "고객":
        converted_text = f"고객 응대 말투로 변환된 내용: {original_text}"
    else:
        converted_text = f"알 수 없는 대상입니다: {original_text}"


    return jsonify({"converted_text": converted_text})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
