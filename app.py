import streamlit as st
import requests
from bs4 import BeautifulSoup
from google import genai
import re


# ---------------------------------------------------
# SECRETS (Gemini + Naver API)
# ---------------------------------------------------
NAVER_ID = st.secrets["NAVER_ID"]
NAVER_SECRET = st.secrets["NAVER_SECRET"]
GEMINI_KEY = st.secrets["GEMINI_KEY"]

client = genai.Client(api_key=GEMINI_KEY)


# ---------------------------------------------------
# HTML 태그 제거 함수 (중요!)
# ---------------------------------------------------
def clean_html(raw_text):
    """Gemini가 실수로 생성한 태그 제거"""
    return re.sub(r"<.*?>", "", raw_text)


# ---------------------------------------------------
# 네이버 뉴스 API 검색
# ---------------------------------------------------
def search_news(query):
    url = "https://openapi.naver.com/v1/search/news.json"
    headers = {
        "X-Naver-Client-Id": NAVER_ID,
        "X-Naver-Client-Secret": NAVER_SECRET
    }
    params = {"query": query, "display": 7}
    res = requests.get(url, headers=headers, params=params)
    return res.json()


# ---------------------------------------------------
# 기사 본문 크롤링
# ---------------------------------------------------
def extract_article(url):
    try:
        res = requests.get(url, timeout=6, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(res.text, "html.parser")

        article = soup.select_one("#dic_area")
        if article:
            return article.get_text(separator="\n").strip()

        body = soup.select_one("div#newsct_article")
        if body:
            return body.get_text(separator="\n").strip()

        paragraphs = soup.find_all("p")
        return "\n".join(p.get_text().strip() for p in paragraphs)

    except:
        return None


# ---------------------------------------------------
# Gemini 요약
# ---------------------------------------------------
def summarize(text):
    prompt = f"""
    당신은 전문 뉴스 에디터이자 재무 분석가입니다.

    아래 기사를 기반으로 핵심 내용을 3~4문장으로 요약하고,
    투자 관점에서 도움이 되는 인사이트를 제공합니다.

    ✦ 요약 규칙 ✦
    - 핵심 주장, 원인, 결과, 수치 포함
    - 광고/저작권/구독 안내 제거
    - 중립적이고 간결하게 작성
    - HTML 태그(<div>, </div>, <p>, <br> 등) 절대 생성 금지
    - 순수 텍스트만 작성
    - 마지막에 '투자자 관점 분석' 포함

    ✦ 출력 형식 ✦
    📌 핵심 요약:
    - 3~4문장 요약

    🔍 주요 포인트:
    - bullet 2~3개

    💹 투자자 관점 분석:
    - 긍정/부정/중립 판단
    - 간단한 이유 제시
    - "투자할만함 / 관망 필요 / 리스크 높음" 중 하나 선택

    ▼ 원문 기사:
    {text}
    """

    try:
        result = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        cleaned = clean_html(result.text)
        return cleaned

    except Exception as e:
        return f"[요약 불가] API 오류 발생: {e}"


# ---------------------------------------------------
# Streamlit UI
# ---------------------------------------------------
st.set_page_config(page_title="🌤️ 오늘의 뉴스 브리핑", layout="wide")

st.markdown("""
<style>
body {
    background: #f9fafb;
    font-family: 'Apple SD Gothic Neo', sans-serif;
}
.title {
    font-size: 38px;
    font-weight: 700;
    padding: 10px 0;
    background: linear-gradient(90deg, #FFD89B, #FEC863);
    -webkit-background-clip: text;
    color: transparent;
    text-align: center;
    margin-bottom: 30px;
}
.news-card {
    background: white;
    padding: 22px;
    border-radius: 18px;
    margin-bottom: 25px;
    border: 1px solid #f0f0f0;
    box-shadow: 0 4px 12px rgba(0,0,0,0.04);
}
.summary-box {
    background: #fff7e6;
    border-left: 4px solid #FFB347;
    padding: 15px 18px;
    margin-top: 14px;
    border-radius: 12px;
    font-size: 15px;
    line-height: 1.6;
}
a.source-link {
    display: inline-block;
    margin-top: 10px;
    font-weight: bold;
    color: #ff9900;
    text-decoration: none;
}
a.source-link:hover {
    text-decoration: underline;
}
</style>
""", unsafe_allow_html=True)


st.markdown('<h1 class="title">🌤️ 오늘의 뉴스 브리핑</h1>', unsafe_allow_html=True)

query = st.text_input("검색어 입력", placeholder="예: 삼성전자, 금리, AI, 테슬라")


# ---------------------------------------------------
# 검색 처리
# ---------------------------------------------------
if query:
    st.info("뉴스를 검색하는 중입니다…⏳")

    data = search_news(query)
    items = data.get("items", [])

    for item in items:

        # 뉴스 카드 헤더
        st.markdown(f"""
        <div class="news-card">
            <h3>{item['title']}</h3>
            <a class="source-link" href="{item['link']}" target="_blank">원문 보기 →</a>
        """, unsafe_allow_html=True)

        # 기사 본문 추출
        article = extract_article(item["link"])

        if article:
            summary = summarize(article)

            st.markdown(f"""
<div class="summary-box">
    <strong>📌 요약</strong><br>
    {summary}
</div>
</div>
""", unsafe_allow_html=True)

        else:
            st.warning("본문을 가져오지 못했습니다.")
