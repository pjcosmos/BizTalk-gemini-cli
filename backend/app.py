from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from groq import Groq

# Load environment variables from .env file
load_dotenv()

# Configure Flask to serve static files from the 'frontend' directory
app = Flask(__name__, static_folder='../frontend', static_url_path='/')
CORS(app)  # Enable CORS for all routes

# Placeholder for Groq AI API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = Groq(
    api_key=GROQ_API_KEY,
)

# Route to serve the main HTML file
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# Route to serve other static files (CSS, JS, etc.)
@app.route('/<path:path>')
def serve_static(path):
    # Prevent serving backend files or sensitive files
    if '..' in path or path.startswith('.'):
        return "Access denied", 403
    return send_from_directory(app.static_folder, path)

@app.route('/api/convert', methods=['POST'])
def convert_text():
    if not GROQ_API_KEY:
        return jsonify({"error": "GROQ_API_KEY not set in environment variables"}), 500

    data = request.get_json()
    original_text = data.get('originalText')
    target_persona = data.get('targetAudience')

    if not original_text or not target_persona:
        return jsonify({"error": "Missing 'originalText' or 'targetAudience' in request"}), 400

    system_message = "당신은 비즈니스 커뮤니케이션 전문가입니다. 사용자가 제공하는 텍스트를 특정 대상에 맞는 적절한 비즈니스 말투로 변환해주세요. 원문의 의미를 유지하되, 대상에게 가장 효과적인 톤앤매너와 어휘를 사용하여 변환해야 합니다."

    if target_persona == "상사":
        system_message += " 변환된 내용은 정중한 격식체로, 결론부터 명확하게 제시하는 보고 형식이어야 합니다."
        model_to_use = "llama3-8b-8192" # Example model, can be configured
    elif target_persona == "타팀 동료":
        system_message += " 변환된 내용은 친절하고 상호 존중하는 어투로, 요청 사항과 마감 기한을 명확히 전달하는 협조 요청 형식이어야 합니다."
        model_to_use = "llama3-8b-8192"
    elif target_persona == "고객":
        system_message += " 변환된 내용은 극존칭을 사용하며, 전문성과 서비스 마인드를 강조하고, 안내/공지/사과 등의 목적에 부합하는 형식이어야 합니다."
        model_to_use = "llama3-8b-8192"
    else:
        return jsonify({"error": "Invalid targetAudience provided"}), 400

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_message,
                },
                {
                    "role": "user",
                    "content": original_text,
                }
            ],
            model=model_to_use,
            temperature=0.7, # Adjust creativity as needed
            max_tokens=1024, # Adjust based on expected output length
        )
        converted_text = chat_completion.choices[0].message.content
        return jsonify({"convertedText": converted_text})
    except Exception as e:
        print(f"Groq API Error: {e}")
        return jsonify({"error": "Failed to convert text using AI. Please try again later."}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
