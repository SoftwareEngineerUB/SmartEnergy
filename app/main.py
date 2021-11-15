from flask import Flask

app = Flask(__name__)

@app.route('/')
def indexPage():
    return "Hello world"
