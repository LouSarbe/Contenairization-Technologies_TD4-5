import requests
import random
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

def get_questions(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()

        data = response.json()
        questions = data["results"]

        return questions

    except requests.exceptions.RequestException as e:
        print(f"Error fetching questions: {e}")
        return None

api_url = "https://opentdb.com/api.php?amount=10"

score = 0
current_question = 0
questions = 0

@app.route('/')
def quiz():
    global questions
    if questions!=0:
        question_count = len(questions)
        if current_question < question_count:
            question = questions[current_question]

            # Shuffle the answers
            question['incorrect_answers'].append(question['correct_answer'])
            random.shuffle(question['incorrect_answers'])

            return render_template('quiz.html', question=question, current_question=current_question, question_count=question_count)
        else:
            return render_template('result.html', score=score, question_count=question_count)
    else:
        questions = get_questions(api_url)
        return redirect('/')

@app.route('/check_answer', methods=['POST'])
def check_answer():
    global score
    user_answer = request.form['answer']

    if user_answer == questions[current_question]['correct_answer']:
        score += 1

    return redirect('/next_question')

@app.route('/next_question')
def next_question():
    global current_question
    current_question += 1
    return redirect('/')

@app.route('/health')
def health_check():
    return '200 OK'

if __name__ == '__main__':
    app.run(port=8080, debug=True, threaded=True)