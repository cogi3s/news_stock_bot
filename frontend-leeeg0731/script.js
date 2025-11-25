async function summarizeNews() {
    const url = document.getElementById("newsUrl").value;
    const experience = document.getElementById("experience").value;
    const risk = document.getElementById("risk").value;
    const budget = Number(document.getElementById("budget").value);

    // 로딩 표시
    document.getElementById("loader").classList.remove("hidden");

    // ★ payload 정의 필수!
    const payload = {
        url: url,
        experience_level: experience,
        risk_preference: risk,
        budget: budget
    };

    try {
        const response = await fetch("http://127.0.0.1:5000/api/summary", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const data = await response.json();
        document.getElementById("loader").classList.add("hidden");

        renderAnalysis(data);

    } catch (error) {
        console.error("요청 실패:", error);
        alert("AI 서버 요청 중 오류가 발생했습니다.");
        document.getElementById("loader").classList.add("hidden");
    }
}

function renderAnalysis(data) {
    const area = document.getElementById("chatArea");
    area.innerHTML = "";

    area.innerHTML += bubble("요약", data.summary || "데이터 없음");
    area.innerHTML += bubble("핵심 키워드", data.keywords?.join(", ") || "데이터 없음");
    area.innerHTML += bubble("시장 영향 분석", data.impact || "데이터 없음");

    const portfolioList = data.suggested_portfolio
        ?.map(p => `${p.name} — ${p.weight}%`)
        .join("<br>") || "데이터 없음";

    area.innerHTML += bubble("포트폴리오 추천", portfolioList);
    area.innerHTML += bubble("AI 조언", data.risk_comment || "데이터 없음");
}

function bubble(title, content) {
    return `
    <div class="chat-bubble">
        <h2>${title}</h2>
        <p>${content}</p>
    </div>`;
}
