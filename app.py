from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["POST"])
def kakao_webhook():
    data = request.get_json()
    user_message = data['userRequest']['utterance']

    if "/배당" in user_message:
        response_text = "💰 4월 7일 MLB 배당 정보\n- Yankees vs Red Sox: 1.80 / 2.10\n- Dodgers vs Cubs: 1.55 / 2.35"
    elif "/날씨" in user_message:
        response_text = "🌧️ 4월 7일 우천 가능성\n- 뉴욕: 60%\n- 시카고: 10%"
    else:
        response_text = "명령어를 다시 입력해주세요. 예) /배당 4월7일"

    return jsonify({
        "version": "2.0",
        "template": {
            "outputs": [{"simpleText": {"text": response_text}}]
        }
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
