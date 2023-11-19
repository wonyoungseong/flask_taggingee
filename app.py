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

a = {}


@app.route("/webhook/", methods=["POST"])
def webhook():
    global a
    request_data = json.loads(request.get_data(), encoding='utf-8')
    a[request_data['user']] = request_data['result']['choices'][0]['message']['content']
    return 'OK'


@app.route("/question", methods=["POST"])
def get_question():
    global a
    request_data = json.loads(request.get_data(), encoding='utf-8')
    response = {"version": "2.0", "template": {"outputs": [{
        "simpleText": {"text": f"질문을 받았습니다. AI에게 물어보고 올께요!: {request_data['action']['params']['question']}"}
    }]}}
    a[request_data['userRequest']['user']['id']] = '아직 AI가 처리중이에요'
    try:
        api = requests.post('https://api.asyncia.com/v1/api/request/', json={
            "apikey": "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",
            "messages": [{"role": "user", "content": request_data['action']['params']['question']}],
            "userdata": [["user", request_data['userRequest']['user']['id']]]},
            headers={"apikey": "A0.cd6a467e-67e7-47a7-87fa-6524ac0fee92._lE5wodHE3xjzO0EMcoS8PV1732wXG-lvg"}, timeout=0.3)
    except requests.exceptions.ReadTimeout:
        pass
    return jsonify(response)


@app.route("/ans", methods=["POST"])
def hello2():
    request_data = json.loads(request.get_data(), encoding='utf-8')
    response = {"version": "2.0", "template": {"outputs": [{
        "simpleText": {"text": f"답변: {a.get(request_data['userRequest']['user']['id'], '질문을 하신적이 없어보여요. 질문부터 해주세요')}"}
    }]}}
    return jsonify(response)
