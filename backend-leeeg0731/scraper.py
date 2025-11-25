# backend/scraper.py

import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def extract_news_html(url: str) -> str:
    """
    뉴스/블로그 HTML 전체를 가져오는 함수.
    본문 추출은 Gemini가 담당한다.
    """
    try:
        res = requests.get(url, headers=headers, timeout=7)
        return res.text  # HTML 전체 반환
    except Exception as e:
        print("[HTML 스크래핑 오류]", e)
        return ""
