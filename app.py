from flask import Flask, jsonify, request
import requests, sys, json
app = Flask(__name__)
a = {}

@app.route("/webhook/", methods=["POST"])
def webhook():
    global a
    request_data = json.loads(request.get_data())
    a[request_data['user']] = request_data['result']['choices'][0]['message']['content']
    return 'OK'

@app.route("/question", methods=["POST"])
def get_question():
    global a
    request_data = json.loads(request.get_data())
    response = { "version": "2.0", "template": { "outputs": [{
        "simpleText": {"text": f"질문을 받았습니다. AI에게 물어보고 올께요!: {request_data['action']['params']['question']}"}
    }]}}
    a[request_data['userRequest']['user']['id']] = '아직 AI가 처리중이에요'
    try:
        api = requests.post('https://api.asyncia.com/v1/api/request/', json={
            "apikey": "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",
            "messages" :[{"role": "user", "content": request_data['action']['params']['question']}],
            "userdata": [["user", request_data['userRequest']['user']['id']]]},
            headers={"apikey":"A0.cd6a467e-67e7-47a7-87fa-6524ac0fee92._lE5wodHE3xjzO0EMcoS8PV1732wXG-lvg"}, timeout=0.3)
    except requests.exceptions.ReadTimeout:
        pass
    return jsonify(response)

@app.route("/ans", methods=["POST"])
def hello2():
    request_data = json.loads(request.get_data())
    response = { "version": "2.0", "template": { "outputs": [{
        "simpleText": {"text": f"답변: {a.get(request_data['userRequest']['user']['id'], '질문을 하신적이 없어보여요. 질문부터 해주세요')}"}
    }]}}
    return jsonify(response)
