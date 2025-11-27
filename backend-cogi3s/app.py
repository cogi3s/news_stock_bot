# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS

from gemini_client import analyze_news_with_gemini
from models import UserProfile
from crawler import fetch_news_text

app = Flask(__name__)
CORS(app)  # 프론트엔드(브라우저)에서 호출하기 위해 CORS 허용


@app.route("/api/health", methods=["GET"])
def health_check():
    """서버 살아있는지 확인용 엔드포인트"""
    return jsonify({"status": "ok"}), 200


@app.route("/api/advice", methods=["POST"])
def get_invest_advice():
    """
    프론트에서 보내는 데이터 예시:
    {
        "experience_level": "초보",
        "risk_preference": "낮음",
        "budget": 1000000,
        "news_text": "오늘 코스피가..."
    }
    """
    data = request.get_json()

    experience_level = data.get("experience_level", "초보")
    risk_preference = data.get("risk_preference", "낮음")
    budget = data.get("budget", 0)
    news_text = data.get("news_text", "")

    if not news_text or not news_text.strip():
        return jsonify({
            "summary": "뉴스 내용이 비어 있습니다.",
            "impact": "뉴스 텍스트를 입력해 주세요.",
            "suggested_portfolio": [],
            "risk_comment": "또는 URL 분석 기능을 사용해 보세요."
        }), 400

    profile = UserProfile(
        experience_level=experience_level,
        risk_preference=risk_preference,
        budget=budget
    )

    analysis_result = analyze_news_with_gemini(news_text, profile)
    return jsonify(analysis_result), 200


@app.route("/api/advice_from_url", methods=["POST"])
def get_invest_advice_from_url():
    """
    프론트에서 보내는 데이터 예시:
    {
        "experience_level": "초보",
        "risk_preference": "낮음",
        "budget": 1000000,
        "news_url": "https://n.news.naver.com/article/xxx/yyy"
    }
    """
    data = request.get_json()

    experience_level = data.get("experience_level", "초보")
    risk_preference = data.get("risk_preference", "낮음")
    budget = data.get("budget", 0)
    news_url = data.get("news_url", "")

    if not news_url:
        return jsonify({
            "summary": "뉴스 URL이 비어 있습니다.",
            "impact": "URL을 입력해 주세요.",
            "suggested_portfolio": [],
            "risk_comment": "분석을 위해 뉴스 URL이 필요합니다."
        }), 400

    # 1) URL에서 기사 본문 크롤링
    news_text = fetch_news_text(news_url)

    if not news_text:
        return jsonify({
            "summary": "뉴스 본문을 가져오지 못했습니다.",
            "impact": "해당 URL은 지원하지 않거나, 구조가 바뀌었을 수 있습니다.",
            "suggested_portfolio": [],
            "risk_comment": "다른 뉴스 링크로 다시 시도해 주세요."
        }), 500

    # 2) 유저 프로필 생성
    profile = UserProfile(
        experience_level=experience_level,
        risk_preference=risk_preference,
        budget=budget
    )

    # 3) Gemini 분석 호출
    analysis_result = analyze_news_with_gemini(news_text, profile)

    # 4) 결과 반환
    return jsonify(analysis_result), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
