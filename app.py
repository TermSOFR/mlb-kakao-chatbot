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
            try:
                team1 = game['teams'][0]
                team2 = game['teams'][1]
            except Exception:
                msg += "- 팀 정보 없음\n"
                continue

            price1 = price2 = '정보 없음'

            try:
                bookmakers = game['bookmakers']
                for bookmaker in bookmakers:
                    markets = bookmaker['markets']
                    for market in markets:
                        outcomes = market['outcomes']
                        if len(outcomes) >= 2:
                            price1 = outcomes[0].get('price', '정보 없음')
                            price2 = outcomes[1].get('price', '정보 없음')
                            break  # 한 쌍만 가져오고 끝냄
                    if price1 != '정보 없음':
                        break
            except Exception:
                pass

            msg += f"- {team1} vs {team2}: {price1} / {price2}\n"

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
