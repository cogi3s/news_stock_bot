# backend/gemini_client.py

import os
import json
from typing import Dict, Any

import google.generativeai as genai
from models import UserProfile


# 1) 환경변수에서 API 키 가져와서 설정
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
  # 터미널에 경고만 찍고, 코드가 완전히 죽지는 않게 처리
  # (api_key 없으면 뒤에서 더미 데이터 리턴)
  print("[WARN] GEMINI_API_KEY 환경변수가 설정되어 있지 않습니다.")
else:
  genai.configure(api_key=API_KEY)


def _build_prompt(news_text: str, profile: UserProfile) -> str:
  """
  Gemini에게 보낼 프롬프트 문자열 생성.
  가능한 한 구조화된 JSON 형태로 답을 달라고 요청한다.
  """
  prompt = f"""
너는 주식 초보자(주린이)를 도와주는 한국어 투자 코치야.

사용자 프로필:
- 투자 경험 수준: {profile.experience_level}
- 위험 선호도: {profile.risk_preference}
- 투자 가능 금액(원): {profile.budget}

아래 뉴스가 주식/ETF/산업 섹터에 어떤 영향을 줄 수 있을지 분석해줘.
그리고 초보자에게 너무 공격적이지 않게 포트폴리오를 추천해줘.

반드시 아래 JSON 형식으로만 대답해. 다른 말은 쓰지 마.
형식:
{{
  "summary": "뉴스 한 줄 요약",
  "impact": "주식시장/어떤 섹터에 영향이 있는지 설명",
  "suggested_portfolio": [
    {{"name": "자산 이름(예: 국내 대형주 ETF)", "weight": 50}},
    {{"name": "자산 이름", "weight": 30}},
    {{"name": "자산 이름", "weight": 20}}
  ],
  "risk_comment": "사용자의 경험과 위험 선호를 고려한 코멘트"
}}

뉴스 원문:
\"\"\"{news_text}\"\"\"
"""
  return prompt


def analyze_news_with_gemini(news_text: str, profile: UserProfile) -> Dict[str, Any]:
    """
    뉴스 텍스트와 사용자 프로필을 받아서
    Gemini로 분석한 결과를 dict 형태로 반환.
    """

    # news_text가 비어있으면 더미 응답
    if not news_text.strip():
      return {
        "summary": "뉴스 내용이 비어 있습니다.",
        "impact": "분석할 수 있는 뉴스가 없습니다.",
        "suggested_portfolio": [],
        "risk_comment": "먼저 분석할 뉴스를 입력해 주세요."
}

    # API 키 없는 경우: 더미 응답 (개발 단계용)
    if not API_KEY:
        return {
            "summary": "[DEMO] 실제 Gemini API 키가 설정되지 않았습니다.",
            "impact": "지금은 더미 데이터로만 동작합니다.",
            "suggested_portfolio": [
                {"name": "국내 주식 ETF", "weight": 60},
                {"name": "해외 주식 ETF", "weight": 30},
                {"name": "현금성 자산", "weight": 10},
            ],
            "risk_comment": "API 키를 설정하면 실제 Gemini 분석 결과가 나옵니다."
        }

    prompt = _build_prompt(news_text, profile)

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)

        # Gemini 응답에서 텍스트 꺼내기
        raw_text = response.text.strip()

        # JSON으로 파싱 시도
        try:
            data = json.loads(raw_text)
        except json.JSONDecodeError:
            # 모델이 JSON 형식을 살짝 어기더라도 앱이 터지지 않게 예외 처리
            print("[WARN] Gemini 응답이 JSON 형식이 아님. 원문을 그대로 사용합니다.")
            data = {
                "summary": raw_text,
                "impact": "모델이 JSON 형식을 지키지 않아 원문 전체를 summary로 반환합니다.",
                "suggested_portfolio": [],
                "risk_comment": "프롬프트를 조금 더 수정해서 JSON 형식을 강하게 요구해 보세요."
            }

        # 혹시 빠진 key가 있어도 에러 나지 않게 기본값 채우기
        return {
            "summary": data.get("summary", ""),
            "impact": data.get("impact", ""),
            "suggested_portfolio": data.get("suggested_portfolio", []),
            "risk_comment": data.get("risk_comment", "")
        }

    except Exception as e:
        # API 호출 에러가 나도 앱이 죽지 않도록 방어
        print(f"[ERROR] Gemini API 호출 중 오류 발생: {e}")
        return {
            "summary": "Gemini API 호출 중 오류가 발생했습니다.",
            "impact": "잠시 후 다시 시도해 주세요.",
            "suggested_portfolio": [],
            "risk_comment": str(e)
        }
