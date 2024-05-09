# Flash Card Game

This is a simple flash card game web application built with Flask.

## Getting Started

### Prerequisites
- Python 3.x
- pip

### Installation

1. Clone the repository:
https://github.com/lhienga/flashcard-game.git

2. Navigate to the project directory:
flashcard-game

3. Install the dependencies:
```python
pip install -r requirements.txt
```
## Running the Application

To run the game, execute the following command in your terminal:

```python
python app.py
```
The local app will be running at http://127.0.0.1:5000/

## Using the Application
### Sign up
If you are a new user, please sign up first. 
- Your email must be unique and in valid format: xxx@xxx
- Your username must be unique and longer than 1 character
- Your passwords must matched

![alt text](screenshots\image.png)

### Login
If you are a returning user, please login with your registered email and password. 
![alt text](screenshots\image-2.png)

### Starting Game
Please choose the operation you want to play with (addition, subtraction, multiplication or division).
![alt text](screenshots\image-3.png)

For division, the answer should be round down to 1 decimal place. 

### Playing Game
You will have 60 seconds to answer as many calculation as possible. You will get +1 point for each correct answer and -1 point for each incorrect answer. 
![alt text](screenshots\image-4.png)

### Score 
You will see your score and the top 5 highest scores in the leaderboard. 
![alt text](screenshots\image-5.png)

