import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response, abort
import sqlite3

app = Flask(__name__)

# Get absolute path of the database file
def get_db_connection():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(base_dir, 'questions.db')
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row  # To access columns by name
    return conn

def init_db():
    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                response TEXT
            )
        ''')
        conn.commit()


import socket

def get_host_ip():
    try:
        # Create a dummy socket connection to get the host IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # The IP and port here are arbitrary; we don't actually connect
        s.connect(('8.8.8.8', 80))
        ip_address = s.getsockname()[0]
    except Exception:
        ip_address = '127.0.0.1'
    finally:
        s.close()
    return ip_address

host_ip = get_host_ip()
print(f"Host IP address: {host_ip}")  # Debug log

@app.context_processor
def inject_host_ip():
    return dict(host_ip=host_ip)

# Home page
@app.route('/')
def home():
    return render_template('home.html')

# Route for submitting questions (moved from '/')
@app.route('/submit', methods=['GET', 'POST'])
def submit_question():
    if request.method == 'POST':
        question = request.form['question']
        print(f"Received question: {question}")
        if question.strip() != '':
            with get_db_connection() as conn:
                c = conn.cursor()
                c.execute('INSERT INTO questions (question) VALUES (?)', (question,))
                conn.commit()
                print("Question saved to database.")
            return redirect(url_for('thank_you'))
        else:
            print("Empty question submitted.")
            return "Please enter a question.", 400
    return render_template('submit_question.html')

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

@app.route('/questions')
def view_questions():
    return render_template('view_questions.html')

@app.route('/get_questions')
def get_questions():
    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute('SELECT question, response FROM questions')
        questions = c.fetchall()
    # Convert list of Row objects to list of dictionaries
    questions_list = [{'question': q['question'], 'response': q['response']} for q in questions]
    print('Fetched questions with responses:', questions_list)  # Debug log
    response = make_response(jsonify(questions=questions_list))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response


# Teacher-only route
@app.route('/teacher', methods=['GET', 'POST'])
def teacher_page():
    allowed_ips = ['127.0.0.1', host_ip]
    client_ip = request.remote_addr
    print(f"Access attempt to /teacher from IP: {client_ip}")  # Debug log

    if client_ip not in allowed_ips:
        abort(403)  # Forbidden access

    if request.method == 'POST':
        # Get the response data from the form
        question_id = request.form.get('question_id')
        response_text = request.form.get('response')
        print(f"Received response for question ID {question_id}: {response_text}")
        with get_db_connection() as conn:
            c = conn.cursor()
            c.execute('UPDATE questions SET response = ? WHERE id = ?', (response_text, question_id))
            conn.commit()
        return redirect(url_for('teacher_page'))

    # Fetch all questions and responses from the database
    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM questions')
        questions = c.fetchall()

    return render_template('teacher.html', questions=questions)

@app.route('/delete_all_questions', methods=['POST'])
def delete_all_questions():
    allowed_ips = ['127.0.0.1', host_ip]
    client_ip = request.remote_addr
    print(f"Access attempt to /delete_all_questions from IP: {client_ip}")  # Debug log

    if client_ip not in allowed_ips:
        abort(403)  # Forbidden access

    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute('DELETE FROM questions')
        conn.commit()
        print("All questions have been deleted.")

    return redirect(url_for('teacher_page'))


# Error handler for 403 Forbidden
@app.errorhandler(403)
def forbidden(error):
    return render_template('403.html'), 403

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5001, debug=True)