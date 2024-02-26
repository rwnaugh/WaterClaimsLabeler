import pandas as pd
from flask import Flask, render_template, request, jsonify
from fileinput import filename

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'















if __name__ == '__main__':
    app.run(host='localhost', port=4000)