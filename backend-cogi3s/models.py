# backend/models.py

from dataclasses import dataclass


@dataclass
class UserProfile:
    experience_level: str  # '초보', '중급', '상급' 등
    risk_preference: str   # '낮음', '보통', '높음'
    budget: int            # 투자 가능 금액 (원 단위, 선택)
