from flask import Flask, request, jsonify
import requests
import datetime

app = Flask(__name__)

API_KEY = '9f97dc8994e6ddc5b21551e62362ddc7'  # ← 여기에 너의 Odds API 키를 입력하세요

def get_mlb_odds(date_string):
    try:
        url = f"https://api.the-odds-api.com/v4/sports/baseball_mlb/odds/?regions=us&markets=h2h&apiKey={API_KEY}"
        res = requests.get(url)

        if res.status_code != 200:
            return f"❗ 배당 API 오류: {res.status_code}"

        games = res.json()
        if not games:
            return "📭 해당 날짜에 예정된 MLB 경기가 없습니다."

        msg = f"💰 MLB 배당 정보\n"
        for game in games:
            try:
                teams = game['teams']
                commence_time = game['commence_time'][:10]

                bookmakers = game.get('bookmakers', [])
                if not bookmakers:
                    continue
                markets = bookmakers[0].get('markets', [])
                if not markets:
                    continue
                outcomes = markets[0].get('outcomes', [])
                if len(outcomes) != 2:
                    continue

                msg += f"- {teams[0]} vs {teams[1]}: {outcomes[0]['price']} / {outcomes[1]['price']} (경기일: {commence_time})\n"
            except Exception:
                continue  # 하나라도 빠져 있으면 그냥 건너뜀

        return msg or "📭 배당 정보가 없습니다."

    except Exception as e:
        return f"오류 발생: {str(e)}"


@app.route("/", methods=["POST"])
def kakao_webhook():
    data = request.get_json()
    user_message = data['userRequest']['utterance']

    if "/배당" in user_message:
        response_text = get_mlb_odds(user_message)
    elif "/날씨" in user_message:
        response_text = "🌧️ 우천 확률 기능은 다음 단계에서 구현됩니다!"
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
