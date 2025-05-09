from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = '9f97dc8994e6ddc5b21551e62362ddc7'  # ← 네 API 키 넣기

def get_mlb_odds(date_string):
    try:
        url = f"https://api.the-odds-api.com/v4/sports/baseball_mlb/odds/?regions=us&markets=h2h&apiKey={API_KEY}"
        res = requests.get(url)

        if res.status_code != 200:
            return f"❗ 배당 API 오류: {res.status_code}"

        games = res.json()
        if not games:
            return "📭 오늘 예정된 MLB 경기가 없습니다."

        msg = f"💰 MLB 배당 정보 ({len(games)}경기)\n"

        for game in games:
            home = game.get("home_team", "홈팀 없음")
            away = game.get("away_team", "원정팀 없음")
            odds = "배당 정보 없음"

            try:
                # 첫 번째 bookmaker만 사용
                bookmaker = game['bookmakers'][0]
                market = bookmaker['markets'][0]
                outcomes = market['outcomes']
                team1 = outcomes[0]
                team2 = outcomes[1]

                odds = f"{team2['name']} @ {team1['name']}: {team2['price']} / {team1['price']}"

            except Exception:
                odds = f"{away} @ {home}: 배당 정보 없음"

            msg += f"- {odds}\n"

        return msg

    except Exception as e:
        return f"❗ 처리 중 오류 발생: {str(e)}"


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
