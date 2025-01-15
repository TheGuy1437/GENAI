from flask import Flask, request, jsonify, render_template
import PyPDF2
import openai
import os

@app.route('/')
def index():
    return render_template('index.html')

# Configure OpenAI API
openai.api_key = 'your_openai_api_key_here'

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-quiz', methods=['POST'])
def generate_quiz():
    if 'pdf' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    pdf_file = request.files['pdf']
    pdf_text = extract_text_from_pdf(pdf_file)

    if not pdf_text:
        return jsonify({"error": "Could not extract text from PDF"}), 500

    # Generate questions using OpenAI
    quiz = create_quiz_from_text(pdf_text)

    if not quiz:
        return jsonify({"error": "Could not generate quiz"}), 500

    return jsonify(quiz)

def extract_text_from_pdf(pdf_file):
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None

def create_quiz_from_text(text):
    try:
        prompt = (
            "Vytvoř 5 multiple-choice otázek na základě následujícího textu."
            " Uveď otázky, čtyři možnosti odpovědi (označené A, B, C, D) a správnou odpověď."
            f"\n\nText:\n{text}"
        )
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=500
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error generating quiz: {e}")
        return None

if __name__ == '__main__':
    app.run(debug=True)
