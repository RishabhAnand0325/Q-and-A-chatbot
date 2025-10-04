import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
try:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-2.5-flash')
except (TypeError, AttributeError):
    print("Google API key not configured. Please check your .env file.")
    model = None

@app.route('/api/ask', methods=['POST'])
def ask():
    if not model:
        return jsonify({"error": "AI model not configured on server"}), 500

    # Get the question from the POST request's JSON body
    data = request.get_json()
    if not data or 'question' not in data:
        return jsonify({"error": "No question provided"}), 400

    question = data['question']
    
    try:
        response = model.generate_content(question)
        return jsonify({"answer": response.text.strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)