from flask import Flask, redirect, request, render_template, jsonify, flash
from flask_debugtoolbar import DebugToolbarExtension
import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "chickensarecool"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

response = []
survey = surveys.satisfaction_survey

@app.route('/')
def home_page():
    return render_template('home.html', title = survey.title, instructions = survey.instructions)

@app.route('/questions/<number>')
def questions(number):
    number = int(number)
    question_number = len(response)
    if number == question_number:
        big_question = survey.questions[number]
        question = big_question.question
        choices = big_question.choices
        text = big_question.allow_text
        return render_template('questions.html', question = question, choices = choices, text = text, number = number)
    else:
        flash('Please answer questions in order.')
        return redirect(f'/questions/{question_number}')


@app.route('/answer', methods = ["POST"])
def answer_collect():
    number = request.form['number']
    answer = request.form[number]
    response.append(answer)

    if len(survey.questions) > len(response):
        next_question = len(response)
        return redirect(f'/questions/{next_question}?')

    else: 
        return render_template('done.html')
    
