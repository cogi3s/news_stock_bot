# backend/gemini_client.py

from models import UserProfile


def analyze_news_with_gemini(news_text: str, profile: UserProfile) -> dict:
    """
    실제로는 여기서 Gemini API를 호출해서
    - 뉴스 요약
    - 주식/섹터 영향 분석
    - 초보자용 포트폴리오 추천
    을 받아오게 될 자리.

    지금은 임시 더미 데이터를 리턴해두고
    나중에 실제 Gemini 연동 코드만 교체하면 됨.
    """

    if not news_text.strip():
        return {
            "summary": "뉴스 내용이 비어 있습니다.",
            "impact": "분석할 수 있는 뉴스가 없습니다.",
            "suggested_portfolio": [],
            "risk_comment": "먼저 뉴스 내용을 입력해 주세요."
        }

    # TODO: 여기에 나중에 실제 Gemini 호출 코드 추가
    # 예시 프롬프트:
    # prompt = f"""
    # 너는 초보 투자자를 위한 주식 투자 코치야.
    # 사용자 프로필: 경험수준={profile.experience_level}, 위험선호={profile.risk_preference}, 예산={profile.budget}
    # 아래 뉴스가 주식시장에 어떤 영향을 줄지 간단 요약하고,
    # 너무 위험하지 않은 수준에서 ETF/섹터 위주 포트폴리오를 추천해줘.
    # 뉴스: {news_text}
    # """

    # ---- 여기까지가 프롬프트 예시, 실제 API 호출은 나중에 구현 ----

    # 임시 더미 응답
    return {
        "summary": "이 뉴스는 국내 증시에 단기적인 변동성을 줄 수 있는 이슈입니다.",
        "impact": "특히 IT/반도체 섹터에 주목할 필요가 있습니다.",
        "suggested_portfolio": [
            {"name": "국내 대형주 ETF", "weight": 50},
            {"name": "IT/반도체 ETF", "weight": 30},
            {"name": "현금성 자산", "weight": 20},
        ],
        "risk_comment": f"당신의 투자 경험('{profile.experience_level}')과 위험 선호('{profile.risk_preference}')를 고려해 상대적으로 보수적인 비중으로 구성했습니다."
    }
