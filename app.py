from flask import Flask, jsonify
import sys
import random
app = Flask(__name__)

@app.route("/random", methods=["POST"])
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
