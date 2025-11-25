# backend/app.py

from flask import Flask, request, jsonify
from flask_cors import CORS

from models import UserProfile
from scraper import extract_news_html   # ← 여기 중요!!
from gemini_client import summarize_news_with_gemini

app = Flask(__name__)
CORS(app)

@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"}), 200


@app.route("/api/summary", methods=["POST"])
def summarize_news():
    data = request.get_json()

    # 사용자 프로필
    profile = UserProfile(
        experience_level=data.get("experience_level", "초보"),
        risk_preference=data.get("risk_preference", "낮음"),
        budget=data.get("budget", 0)
    )

    # URL 또는 텍스트 입력
    url = data.get("url", "")
    news_text = data.get("news_text", "")

    # -----------------------------
    # 🔥 URL이 들어온 경우 → HTML 전체 가져오기
    # -----------------------------
    if url:
        html = extract_news_html(url)     # ← 여기 넣는 거 맞음!!
        if not html.strip():
            return jsonify({"error": "URL에서 HTML을 가져오지 못했습니다."}), 400

        news_text = html   # ← 이제 HTML 전체를 Gemini에 넘김!!

    # URL도 없고 수동 텍스트도 없으면 에러
    if not news_text.strip():
        return jsonify({"error": "뉴스 텍스트가 비어있습니다."}), 400

    # Gemini 분석
    result = summarize_news_with_gemini(news_text, profile)
    return jsonify(result), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
