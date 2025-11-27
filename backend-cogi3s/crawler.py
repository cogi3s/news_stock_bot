# backend/crawler.py

import re
from typing import Optional

import requests
from bs4 import BeautifulSoup


def _clean_text(text: str) -> str:
    """불필요한 공백, 줄바꿈 정리용 간단 유틸 함수"""
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def fetch_naver_news_body(url: str) -> Optional[str]:
    """네이버 뉴스 기사 본문 크롤링"""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    body = soup.select_one("#dic_area")
    if not body:
        article = soup.find("article")
        if not article:
            return None
        body = article

    paragraphs = [p.get_text(" ", strip=True) for p in body.find_all("p")]
    text = " ".join(paragraphs) if paragraphs else body.get_text(" ", strip=True)

    return _clean_text(text)


def fetch_generic_article_body(url: str) -> Optional[str]:
    """네이버 외 일반 뉴스 구조 기본 크롤링"""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    article = soup.find("article")
    paragraphs = article.find_all("p") if article else soup.find_all("p")

    if not paragraphs:
        return None

    text = " ".join([p.get_text(" ", strip=True) for p in paragraphs])
    return _clean_text(text)


def fetch_news_text(url: str) -> str:
    """뉴스 URL 입력받아 본문 텍스트 반환"""

    try:
        if "n.news.naver.com" in url or "news.naver.com" in url:
            text = fetch_naver_news_body(url)
        else:
            text = fetch_generic_article_body(url)

        return text or ""
    except Exception as e:
        print(f"[ERROR] 크롤링 실패: {e}")
        return ""
