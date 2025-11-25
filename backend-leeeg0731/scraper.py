# 뉴스 본문 추출 모듈 
# backend/scraper.py

import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def extract_news_text(url: str) -> str:
    """
    뉴스 URL을 받아 본문 텍스트만 추출하는 함수.
    실패하거나 빈 본문이면 "" 반환.
    """

    try:
        res = requests.get(url, headers=headers, timeout=5)
        html = res.text
    except Exception as e:
        print(f"[스크래핑 오류] {e}")
        return ""

    soup = BeautifulSoup(html, "html.parser")

    # 1) 가장 기본적인 모든 <p> 태그 내용 수집
    paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
    text = "\n".join(paragraphs)

    # 2) 너무 짧으면 실패라고 판단
    if len(text) < 50:
        return ""

    # 3) 불필요한 공백 제거
    text = text.replace("\xa0", " ").replace("\u200b", " ").strip()

    return text
