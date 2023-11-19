from flask import Flask, jsonify, request
import sys
import random
import json
import datetime
app = Flask(__name__)



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


days_of_the_week_list = ["월", "화", "수", "목", "금", "토", "일"]
@app.route("/day", methods=["GET", "POST"])
def day_of_the_week():
    if request.method == "POST":
        # 카카오톡 서버에서 스킬이 보내는 요청의 데이터
        request_data = json.loads(request.get_data() or "{}")
        print(request_data)

        params = request_data.get("action", {}).get("params", {})
        param_date = json.loads(params.get("sys_date_params", "{}"))
        print(param_date)

        # 파라미터에서 날짜를 추출하거나 현재 날짜를 사용
        now = datetime.datetime.now()
        year = int(param_date.get("year", now.year))
        month = int(param_date.get("month", now.month))
        day = int(param_date.get("day", now.day))

        date_obj = datetime.datetime(year, month, day)

        # 요일 정보를 텍스트로 반환
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
        # GET 요청에 대한 처리 (예: 간단한 안내 메시지 반환)
        return "Please use POST request to send data."
