from flask import Flask, jsonify, request
import sys
import json
import datetime

application = Flask(__name__)

days_of_the_week_list = ["월", "화", "수", "목", "금", "토", "일"]


@application.route("/day", methods=["POST"])
def day_of_the_week():
    # 카카오톡 서버에서 스킬이 보내는 요청의 데이터
    request_data = json.loads(request.get_data(), encoding="utf-8")
    print(request_data)

    params = request_data["action"]["params"]
    param_date = json.loads(params["sys_date_params"])
    print(param_date)

    # 현재 날짜를 기본값으로 설정
    now = datetime.datetime.now()
    year = int(param_date["year"]) if "year" in param_date else now.year
    month = int(param_date["month"]) if "month" in param_date else now.month
    day = int(param_date["day"]) if "day" in param_date else now.day

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


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=int(sys.argv[1]), debug=True)
