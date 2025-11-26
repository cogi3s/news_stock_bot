import streamlit as st
import requests
from bs4 import BeautifulSoup
from google import genai

# ---------------------------------------------------
# SECRETS (Gemini + Naver API)
# ---------------------------------------------------
NAVER_ID = st.secrets["NAVER_ID"]
NAVER_SECRET = st.secrets["NAVER_SECRET"]
GEMINI_KEY = st.secrets["GEMINI_KEY"]

client = genai.Client(api_key=GEMINI_KEY)


# ---------------------------------------------------
# 네이버 뉴스 API 검색 함수
# ---------------------------------------------------
def search_news(query):
    url = "https://openapi.naver.com/v1/search/news.json"
    headers = {
        "X-Naver-Client-Id": NAVER_ID,
        "X-Naver-Client-Secret": NAVER_SECRET
    }
    params = {"query": query, "display": 5}
    res = requests.get(url, headers=headers, params=params)
    return res.json()


# ---------------------------------------------------
# 기사 본문 크롤링
# ---------------------------------------------------
def extract_article(url):
    try:
        r = requests.get(url, timeout=6)
        soup = BeautifulSoup(r.text, "html.parser")
        texts = [p.get_text().strip() for p in soup.find_all("p")]
        return "\n".join(texts)
    except:
        return None


# ---------------------------------------------------
# Gemini 요약
# ---------------------------------------------------
def summarize(text):
    prompt = f"""
    다음 기사를 3줄로 요약해줘.
    - 핵심만 간단히
    - 1분 안에 읽기 좋게

    기사내용:
    {text}
    """
    result = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=prompt
)

    return result.text


# ---------------------------------------------------
# Streamlit UI
# ---------------------------------------------------
st.set_page_config(page_title="1분 뉴스 요약", layout="wide")

st.markdown("""
    <h1 style="color:#00b4db; font-size:40px;">📰 1분 뉴스 요약 서비스</h1>
""", unsafe_allow_html=True)

query = st.text_input("검색어 입력", placeholder="예: 삼성전자, 금리, AI")

if query:
    st.info("뉴스를 검색하는 중입니다…⏳")

    data = search_news(query)
    items = data.get("items", [])

    for item in items:
        st.subheader(item["title"])
        st.write(f"[원문 보기]({item['link']})")

        article = extract_article(item["link"])
        if article:
            summary = summarize(article)
            st.markdown("---")
            st.markdown("### 📌 요약 결과")
            st.write(summary)
            st.markdown("---")
        else:
            st.warning("본문을 가져오지 못했습니다.")
