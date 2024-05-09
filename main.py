from flask import Flask, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
import random
import time
from __init__ import create_app, db
from models import User
import math

app = Flask(__name__)
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
