from flask import Flask, jsonify
import sys
import random
app = Flask(__name__)

# 루트 경로 ("/") 라우트


@app.route("/")
def home():
    return "Welcome to the Home Page!"

# "/random" 경로 라우트


@app.route("/random", methods=["GET", "POST"])
def random_function():
    response = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": str(random.randint(1, 100))
                    }
                }
            ]
        }
    }
    return jsonify(response)
