const analyzeUrlBtn = document.getElementById("analyze-url-btn");

analyzeUrlBtn.addEventListener("click", async () => {
  const experience = document.getElementById("experience").value;
  const risk = document.getElementById("risk").value;
  const budget = parseInt(document.getElementById("budget").value || "0", 10);
  const newsUrl = document.getElementById("news-url").value;

  if (!newsUrl.trim()) {
    alert("뉴스 URL을 입력해 주세요!");
    return;
  }

  const payload = {
    experience_level: experience,
    risk_preference: risk,
    budget: budget,
    news_url: newsUrl,
  };

  try {
    const response = await fetch("http://localhost:5000/api/advice_from_url", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error("서버 응답 에러");
    }

    const data = await response.json();
    resultEl.textContent = JSON.stringify(data, null, 2);
  } catch (err) {
    console.error(err);
    resultEl.textContent = "URL 분석 중 오류가 발생했습니다.";
  }
});
