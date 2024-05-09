from flask import Flask, request, render_template, redirect, url_for, Blueprint
from flask_login import login_required, current_user
import random
import time
from __init__ import create_app, db
from models import User
import math

app = Flask(__name__)
app = create_app()
global started, combinations
started = False



@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    global started, combinations, start_time, duration
    started = False  # Reset the started flag
    combinations = None  # Reset the combinations list
    start_time = None
    duration = None
    print("hihi")
    return render_template("start_game.html", user=current_user)

@app.route('/game', methods=['GET', 'POST'])
def game():
    global start_time, started, combinations, duration
    
    if request.method == 'POST' and started:
        # Handle form submission
        operation = request.form['operation']
        duration = int(request.form['duration'])
        score = int(request.form.get('score', 0))

        if 'answer' in request.form:
            user_answer = float(request.form['answer'])

            num1 = int(request.form['num1'])
            num2 = int(request.form['num2'])
            
            # Calculate the expected answer based on the operation
            if operation == '+':
                expected_answer = num1 + num2
            elif operation == '-':
                expected_answer = num1 - num2
            elif operation == '*':
                expected_answer = num1 * num2
            else:
                expected_answer = math.floor((num1/num2)*10)/10

            # Compare user's answer with the expected answer
            if user_answer == expected_answer:
                score += 1
                remove_pair(num1, num2)

        # Check if the duration is over
        elapsed_time = time.time() - start_time
        if elapsed_time >= duration:
            # Duration is over, redirect to the score page
            return redirect(url_for('score', score=score))

        # Generate new numbers for the flashcard
        # Check if there are no pairs left
        if not combinations:
            # Calculate the elapsed time
            elapsed_time = time.time() - start_time
            # Calculate the correction rate based on the score divided by the elapsed time
            duration = elapsed_time
            # Redirect to the score page with the correction rate
            return redirect(url_for('score', score=score))
        num1, num2 = generate_new_numbers(operation)

        # Render the game HTML with updated values
        return render_template('game.html', num1=num1, num2=num2, operation=operation, score=score, duration=duration, start_time=start_time, user=current_user)

    else:
        # Initial game setup
        operation = request.form.get('operation')  # Get operation from query string
        duration = int(request.form.get('duration'))  # Get duration from query string
        start_time = time.time()
        started = True

        # Generate combinations list if not already generated
        if 'combinations' not in globals():
            generate_combinations()

        # Render the game HTML with initial values
        num1, num2 = generate_new_numbers(operation)
        return render_template('game.html', num1=num1, num2=num2,  operation=operation, score=0, duration=duration, start_time=start_time, user=current_user)

def generate_combinations():
    global combinations
    combinations = [(i, j) for i in range(13) for j in range(i, 13)]  # Generate pairs with num1 <= num2
    random.shuffle(combinations)

def generate_new_numbers(operation):
    global combinations
    if not combinations:
        generate_combinations()
    return combinations.pop()

def remove_pair(num1, num2):
    global combinations
    combinations = [(x, y) for x, y in combinations if not ((x == num1 and y == num2) or (x == num2 and y == num1))]

@app.route('/score')
def score():
    global duration
    score = request.args.get('score')
    # Update the user's rate if the new score is higher
    update = User.query.filter_by(id=current_user.id).first()
    if not update.rate or update.rate < int(score) / duration:
        update.rate = int(score) / duration
        db.session.commit()
    
    # Fetch the top 5 users with the highest rate
    top_users = User.query.order_by(User.rate.desc()).limit(5).all()
    
    return render_template('score.html', score=score, user=current_user, top_users=top_users)

@app.route('/play-again')
def play_again():
    global started, combinations
    started = False  # Reset the started flag
    combinations = None  # Reset the combinations list
    return redirect(url_for('home'))

@app.route('/back_to_home')
def back_to_home():
    return play_again()

if __name__ == '__main__':
    app.run(debug=True)
