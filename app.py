from flask import Flask, request, jsonify, send_from_directory
import requests
import fitz

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

def extract_answers_from_pdf(pdf_bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = ''.join(page.get_text() for page in doc)
    # 🚧 TODO: Parse actual answers based on PDF format
    return {"Q1": "2", "Q2": "1", "Q3": "3"} 

def get_user_answers():
    # 🚧 TODO: Replace with real user answer parsing
    return {"Q1": "2", "Q2": "1", "Q3": "4"}

def calculate_score(user_answers, correct_answers):
    score = 0
    for q, ans in correct_answers.items():
        user_ans = user_answers.get(q, '')
        if user_ans == ans:
            score += 5
        elif user_ans:
            score -= 1
    return score

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    url = data.get('url')
    resp = requests.get(url)
    correct_answers = extract_answers_from_pdf(resp.content)
    user_answers = get_user_answers()
    return jsonify({"score": calculate_score(user_answers, correct_answers)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

