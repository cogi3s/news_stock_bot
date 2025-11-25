# Gemini 요약/분석/추천 생성
# backend/gemini_client.py

from models import UserProfile
from google import genai
import json

# ----------------------------
# 1) Gemini 클라이언트 설정
# ----------------------------
API_KEY = "AIzaSyDpxSOU4pvAUbYmn8GmfjqPlYRFCC2h6no"   # ← 이거만 바꾸면 끝!
client = genai.Client(api_key=API_KEY)


def summarize_news_with_gemini(news_text: str, profile: UserProfile) -> dict:
    """
    실제 Gemini API로 뉴스 요약 + 키워드 + 시장영향 + 포트폴리오 추천을 반환.
    """

    if not news_text.strip():
        return {
            "summary": "뉴스 내용이 비어 있습니다.",
            "keywords": [],
            "impact": "",
            "suggested_portfolio": [],
            "risk_comment": ""
        }

    # ----------------------------
    # 2) Gemini 프롬프트 구성
    # ----------------------------
    prompt = f"""
너는 초보 투자자를 위한 AI 투자 코치야.

[사용자 정보]
- 경험 수준: {profile.experience_level}
- 위험 성향: {profile.risk_preference}
- 투자 예산: {profile.budget}원

[뉴스 내용]
{news_text}

[요구 사항]
1) 뉴스를 3줄로 요약
2) 핵심 키워드 5개 추출
3) 주식시장·업종·ETF 영향 분석
4) 사용자 위험 성향에 맞춘 ETF 중심 포트폴리오 추천
5) 초보자도 이해하기 쉬운 설명
6) 모든 출력은 반드시 JSON 형식으로 반환:

{{
  "summary": "",
  "keywords": [],
  "impact": "",
  "suggested_portfolio": [
        {{"name": "", "weight": 0}}
  ],
  "risk_comment": ""
}}
    """

    # ----------------------------
    # 3) Gemini API 호출
    # ----------------------------
    response = client.models.generate_content(
        model="gemini-1.5-flash",  
        contents=prompt
    )

    # ----------------------------
    # 4) 응답 JSON 파싱
    # ----------------------------
    try:
        ai_text = response.text
        data = json.loads(ai_text)
        return data

    except Exception as e:
        print("[Gemini JSON 파싱 오류]", e)
        return {
            "summary": "AI 분석 중 오류가 발생했습니다.",
            "keywords": [],
            "impact": "",
            "suggested_portfolio": [],
            "risk_comment": ""
        }
