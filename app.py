import os
from flask import Flask, render_template, request, jsonify, session
from quiz_logic import get_transcript, generate_quiz_from_text

# --- Initialize the Flask application ---
app = Flask(__name__)
app.secret_key = os.urandom(24)

# --- FLASK ROUTES ---

@app.route('/')
def index():
    """Renders the main page."""
    return render_template('index.html')

@app.route('/generate_quiz', methods=['POST'])
def handle_generate_quiz():
    """
    Handles quiz generation from a YouTube URL.
    This is the unified endpoint for quiz generation.
    """
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"error": "No YouTube URL provided."}), 400

    url = data['url']
    try:
        # Get transcript
        transcript_text = get_transcript(url)
        
        # Generate quiz from transcript
        quiz_data = generate_quiz_from_text(transcript_text)

        # Store the full quiz data (including answers) in the session
        session['quiz_data'] = quiz_data

        # Return only questions and options to the client to prevent cheating
        questions_for_client = [
            {"question": q["question"], "options": q["options"]} for q in quiz_data
        ]
        return jsonify(questions_for_client)

    except (ValueError, ConnectionError) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(f"An unexpected error occurred during quiz generation: {e}")
        return jsonify({"error": "An internal server error occurred."}), 500

@app.route('/submit_quiz', methods=['POST'])
def handle_submit_quiz():
    """
    Handles the AJAX request to score the quiz.
    Compares user answers with the correct answers stored in the session.
    """
    user_answers = request.get_json().get('answers', {})
    correct_answers = session.get('quiz_data')

    if not correct_answers:
        return jsonify({"error": "Quiz data not found. Please generate a new quiz."}), 400

    score = 0
    results = []
    total = len(correct_answers)

    for i, question_data in enumerate(correct_answers):
        user_answer = user_answers.get(f'q{i}')
        is_correct = user_answer == question_data['correct_answer']
        if is_correct:
            score += 1
        results.append({
            "question": question_data['question'],
            "user_answer": user_answer,
            "correct_answer": question_data['correct_answer'],
            "is_correct": is_correct
        })

    return jsonify({"score": score, "total": total, "results": results})


# --- MAIN EXECUTION ---
if __name__ == '__main__':
    # Using debug=True is fine for development, but should be turned off in production.
    app.run(debug=True)


