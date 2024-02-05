from flask import Flask, render_template, redirect, session, flash, request
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

RESPONSES_KEY = "responses"

app = Flask(__name__)

app.config['SECRET_KEY'] = "survey"
# app.config['DEBUG_TO_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

# responses = []

@app.route('/')
def start():
    """Show a homepage/start page where the user can see the survey title, instrutions, and can start 
    the survey."""
    return render_template('start.html', survey=survey)

@app.route('/begin', methods=["POST"])
def start_survey():
    """Clear the session of any previous responses"""

    session[RESPONSES_KEY] = []

    return redirect("/questions/0")

@app.route('/answer', methods=["POST"])
def answers():
    """Append responses and redirect to the next question"""
    #get the response choice form
    choice = request.form['answer']

    #add responses to the session
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    #conditional to check if all questions have been answered
    if (len(responses) == len(survey.questions)):
        return redirect('/finished') 
    
    else:
        return redirect(f'/questions/{len(responses)}')

@app.route('/questions/<int:qid>')
def show_question(qid):
    """Display the current question"""
    responses = session.get(RESPONSES_KEY)

    #conditionals checking the responses
    if (responses is None):
        # Not answering the question or accessing a future question too soon
        return redirect("/")
    
    if (len(responses) == len(survey.questions)):
        # All questions have been answered
        return redirect('/finished') 
    
    if (len(responses) != qid):
        # Answering the questions out of order
        flash(f'Invalid question id: {qid}.')
        return redirect(f"/questions/{len(responses)}")
    
    question = survey.questions[qid]
    return render_template('question.html', question_num=qid, question=question)

@app.route('/finished')
def finish():
    """Survey completed. Show final page"""
    return render_template('finished.html')