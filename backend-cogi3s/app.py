from flask import Flask, request, jsonify
from flask_cors import CORS

from gemini_client import analyze_news_with_gemini
from models import UserProfile

app = Flask(__name__)
CORS(app)



@app.route('/api/health", methods=['GET']')
def helth_check():
    """서버 살아있는지 확인용 엔드포인트"""
    return jsonify({"status": "ok"}), 200



@app.route("/api/advice", metods=["POST"])
def get_investment_advice():
    """프론트에서 보내는 데이터 예시:
    {
        "experience_level": "초보",
        "risk_preference": "낮음",
        "budget": 1000000,
        "news_text": "오늘 코스피가..."
    }
    """
    data = request.get_json()

    #요청 값 파싱 (기본값도 설정해두기)
    experience_level =  data.get("experience_level", "초보")
    risk_preference = data.get("risk_preference", "낮음")
    budget = data.get("budget", 0)
    news_text = data.get("news_text", "")

    # 3) Gemini 분석 호출 (지금은 더미 구현, 나중에 실제 API 연동)
    analysis_result = analyze_news_with_gemini(news_text, profile)

    # 4) 프론트로 JSON 응답
    return jsonify(analysis_result), 200


if __name__ == "__main__":
    # 개발용 서버 실행
    app.run(host="0.0.0.0", port=5000, debug=True)