import requests
import random
from flask import Flask, render_template, request, redirect, jsonify
import psycopg2

db_host = "db"
db_port = "5432"
db_name = "CT_PW04-database"
db_user = "LouSarbe"
db_password = "Password01"


app = Flask(__name__)

def insert_data_into_db(data):
    try:
        connection = psycopg2.connect(
            host=db_host,
            port=db_port,
            dbname=db_name,
            user=db_user,
            password=db_password
        )

        cursor = connection.cursor()

        insert_query = "INSERT INTO products (name, price) VALUES (%s, %s)"
        cursor.execute(insert_query, (data['value1'], data['value2']))

        connection.commit()

        cursor.close()
        connection.close()

        return True
    except Exception as e:
        print("Error inserting data into database:", e)
        return False

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
    
@app.route('/api/insert', methods=['POST'])
def insert_into_db():
    # Example JSON data
    data = {
        'value1': 'Louis',
        'value2': 999.99
    }

    if insert_data_into_db(data):
        return jsonify({'message': 'Data inserted successfully'}), 200
    else:
        return jsonify({'message': 'Failed to insert data into database'}), 500

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
    app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)