from flask import Flask, jsonify, request
import requests
import sys
import random
import json
import datetime

app = Flask(__name__)


@app.route("/")
def home():
    return "Welcome to the Home Page!"


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


days_of_the_week_list = ["월", "화", "수", "목", "금", "토", "일"]


@app.route("/day", methods=["GET", "POST"])
def day_of_the_week():
    if request.method == "POST":
        request_data = json.loads(request.get_data() or "{}")
        params = request_data.get("action", {}).get("params", {})
        param_date = json.loads(params.get("sys_date_params", "{}"))

        now = datetime.datetime.now()
        year = int(param_date.get("year", now.year))
        month = int(param_date.get("month", now.month))
        day = int(param_date.get("day", now.day))

        date_obj = datetime.datetime(year, month, day)

        response = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": days_of_the_week_list[date_obj.weekday()] + "요일"
                        }
                    }
                ]
            }
        }
        return jsonify(response)
    else:
        return "Please use POST request to send data."


a = {}


@app.route("/webhook/", methods=["GET", "POST"])
def webhook():
    global a
    request_data = json.loads(request.get_data())
    a[request_data['user']] = request_data['result']['choices'][0]['message']['content']
    return 'OK'


@app.route("/question", methods=["GET", "POST"])
def get_question():
    global a
    if request.method == "GET":
        # GET 요청에 대한 처리
        question = request.args.get('question')
        return jsonify({"message": f"GET 요청 받음, 질문: {question}"})
    elif request.method == "POST":
        try:
            request_data = json.loads(request.get_data())
            # POST 요청 처리 로직
            # ...

            # 외부 API 요청
            try:
                api_response = requests.post('https://api.asyncia.com/v1/api/request/', json={
                    # API 요청 관련 데이터
                }, timeout=5)  # 타임아웃 값을 조정
                # API 응답 처리 로직
                # ...
            except requests.exceptions.RequestException as e:
                # 외부 API 요청 오류 처리
                return jsonify({"error": "External API request failed"}), 500

            # 성공적인 응답 반환
            return jsonify({"message": "Success"})
        except json.JSONDecodeError:
            # JSON 파싱 오류 처리
            return jsonify({"error": "Invalid JSON format"}), 400
        except Exception as e:
            # 기타 예외 처리
            return jsonify({"error": "An error occurred"}), 500


@app.route("/ans", methods=["GET", "POST"])
def hello2():
    if request.method == "GET":
        user_id = request.args.get('user_id')
        response_text = a.get(user_id, '질문을 하신적이 없어보여요. 질문부터 해주세요')
        response = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": f"답변: {response_text}"
                        }
                    }
                ]
            }
        }
        return jsonify(response)
    else:
        # POST 요청에 대한 기존 처리를 유지
        request_data = json.loads(request.get_data())
        response_text = a.get(
            request_data['userRequest']['user']['id'], '질문을 하신적이 없어보여요. 질문부터 해주세요')
        response = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": f"답변: {response_text}"
                        }
                    }
                ]
            }
        }
        return jsonify(response)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
