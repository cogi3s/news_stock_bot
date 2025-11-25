# 유저프로필관리
# backend/models.py

from dataclasses import dataclass

@dataclass
class UserProfile:
    """
    사용자 정보 모델.
    뉴스 기반 투자 조언 시 필요한 개인 프로필 데이터.
    """
    experience_level: str   # '초보', '중급', '상급'
    risk_preference: str    # '낮음', '보통', '높음'
    budget: int             # 예산 (원 단위)
