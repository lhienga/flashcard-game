from flask import Blueprint, Flask, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
import random
import time
from __init__ import create_app, db
from models import User
import math

game = Blueprint('game', __name__)

@game.route('/', methods=['GET', 'POST'])
@login_required
def home():
    global started, combinations, start_time, duration
    started = False  # Reset the started flag
    combinations = None  # Reset the combinations list
    start_time = None
    duration = 60
    return render_template("start_game.html", user=current_user)

@game.route('/start-game', methods=['POST'])
def start_game():
    global start_time, started, combinations, duration
    # Initial game setup
    operation = request.form.get('operation')  # Get operation from query string
    
    start_time = time.time()
    started = True

    # Generate combinations list if not already generated
    if 'combinations' not in globals():
        generate_combinations(operation)

    # Render the game HTML with initial values
    num1, num2 = generate_new_numbers(operation)
    return render_template('game.html', num1=num1, num2=num2,  operation=operation, score=0, start_time=start_time, user=current_user)

@game.route('/game', methods=['POST'])
def play_game():
    global start_time, started, combinations, duration
    
    
    # Handle form submission
    operation = request.form['operation']
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
        elif operation == 'x':
            expected_answer = num1 * num2
        else:
            expected_answer = math.floor((num1/num2)*10)/10

        # Compare user's answer with the expected answer
        if user_answer == expected_answer:
            score += 1
            remove_pair(num1, num2)
            flash('Correct answer!', 'success')  # Flash a success message
        else:
            score -= 1
            flash('Incorrect answer!', 'danger')  # Flash an error message


    # Check if the duration is over
    elapsed_time = time.time() - start_time
    if elapsed_time >= duration:
        # Duration is over, redirect to the score page
        return redirect(url_for('game.score', score=score))

    # Generate new numbers for the flashcard
    # Check if there are no pairs left
    if not combinations:
        return redirect(url_for('game.score', score=score))
    num1, num2 = generate_new_numbers(operation)

    # Render the game HTML with updated values
    return render_template('game.html', num1=num1, num2=num2, operation=operation, score=score, start_time=start_time, user=current_user)

def generate_combinations(operation):
    global combinations
    if operation == '+' or operation == "x":
        combinations = [(i, j) for i in range(13) for j in range(i, 13)]  # Generate pairs with num1 <= num2
    elif operation == '-':
        combinations = [(i, j) for i in range(13) for j in range(13)] 
    else:
        combinations = [(i, j) for i in range(13) for j in range(1, 13)] # no division by 0
    random.shuffle(combinations)

def generate_new_numbers(operation):
    global combinations
    if not combinations:
        generate_combinations(operation)
    return combinations.pop()

def remove_pair(num1, num2):
    global combinations
    combinations = [(x, y) for x, y in combinations if not ((x == num1 and y == num2) or (x == num2 and y == num1))]

@game.route('/score')
def score():
    #global duration
    score = request.args.get('score')
    # Update the user's score if the new score is higher
    update = User.query.filter_by(id=current_user.id).first()
    if not update.score or update.score < int(score) :
        update.score = int(score) 
        db.session.commit()
    
    # Fetch the top 5 users with the highest score
    top_users = User.query.order_by(User.score.desc()).limit(5).all()
    
    return render_template('score.html', score=score, user=current_user, top_users=top_users)

@game.route('/play-again')
def play_again():
    global started, combinations
    started = False  # Reset the started flag
    combinations = None  # Reset the combinations list
    return redirect(url_for('game.home'))


