
import json
from flask import render_template, redirect, url_for, session, flash, request, g
from app import app

@app.route('/')
def index():
    return render_template('index.html', title="Home")
