// frontend/script.js

const analyzeBtn = document.getElementById("analyze-btn");
const resultEl = document.getElementById("result");

analyzeBtn.addEventListener("click", async () => {
  const experience = document.getElementById("experience").value;
  const risk = document.getElementById("risk").value;
  const budget = parseInt(document.getElementById("budget").value || "0", 10);
  const newsText = document.getElementById("news-text").value;

  // 간단한 유효성 검사
  if (!newsText.trim()) {
    alert("뉴스 내용을 입력해 주세요!");
    return;
  }

  const payload = {
    experience_level: experience,
    risk_preference: risk,
    budget: budget,
    news_text: newsText,
  };

  try {
    const response = await fetch("http://localhost:5000/api/advice", {
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
    resultEl.textContent = "오류가 발생했습니다. 콘솔을 확인해 주세요.";
  }
});
