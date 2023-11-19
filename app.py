from flask import Flask
import sys
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello typeCloud"
