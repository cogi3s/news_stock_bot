# backend/gemini_client.py

from google.genai import Client
from models import UserProfile
import json

API_KEY = "AIzaSyCNwPGqX9dgPlcb5sNuEib6ykZ2DrwkW9o"   # ← 네가 준 API 키
client = Client(api_key=API_KEY)

def summarize_news_with_gemini(news_text: str, profile: UserProfile) -> dict:

    if not news_text.strip():
        return {
            "summary": "뉴스 내용이 비어 있습니다.",
            "keywords": [],
            "impact": "",
            "suggested_portfolio": [],
            "risk_comment": ""
        }

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
3) 시장·업종·ETF 영향 분석
4) 사용자 위험 성향에 맞는 포트폴리오 추천
5) 아래 형식의 JSON으로만 출력

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

    try:
        response = client.generate(
            model="models/gemini-1.5-flash",
            prompt=prompt
        )

        print("[AI 원본 응답]", response.text)

        return json.loads(response.text)

    except Exception as e:
        print("Gemini API 오류:", e)
        return {
            "summary": "AI 분석 중 오류 발생",
            "keywords": [],
            "impact": "",
            "suggested_portfolio": [],
            "risk_comment": ""
        }
