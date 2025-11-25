# 전체 API서버 (flask)
# backend/app.py

# 전체 API서버 (flask)
from flask import Flask, request, jsonify
from flask_cors import CORS

from models import UserProfile
from scraper import extract_news_text
from gemini_client import summarize_news_with_gemini

app = Flask(__name__)
CORS(app)


# -----------------------
# 1) 서버 헬스 체크
# -----------------------
@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"}), 200


# -----------------------
# 2) 뉴스 요약 + 투자조언
# -----------------------
@app.route("/api/summary", methods=["POST"])
def summarize_news():
    data = request.get_json()

    # ---- 사용자 프로필 파싱 ----
    profile = UserProfile(
        experience_level=data.get("experience_level", "초보"),
        risk_preference=data.get("risk_preference", "낮음"),
        budget=data.get("budget", 0)
    )

    # ---- 뉴스 데이터 ----
    url = data.get("url", "")
    news_text = data.get("news_text", "")

    # URL이 들어오면 → 크롤링
    if url:
        extracted = extract_news_text(url)
        if not extracted.strip():
            return jsonify({"error": "URL에서 뉴스 본문을 가져오지 못했습니다."}), 400

        news_text = extracted

    # URL도 없고 텍스트도 비었으면 에러
    if not news_text.strip():
        return jsonify({"error": "뉴스 텍스트가 비어있습니다."}), 400

    # ---- Gemini에게 요약/분석/추천 요청 ----
    result = summarize_news_with_gemini(news_text, profile)
    return jsonify(result), 200
