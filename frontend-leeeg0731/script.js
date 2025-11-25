async function summarizeNews() {
    const url = document.getElementById("newsUrl").value;
    const experience = document.getElementById("experience").value;
    const risk = document.getElementById("risk").value;
    const budget = Number(document.getElementById("budget").value);

    document.getElementById("loader").classList.remove("hidden");

    const response = await fetch("http://localhost:5000/api/summary", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            url: url,
            experience_level: experience,
            risk_preference: risk,
            budget: budget
        })
    });

    const data = await response.json();
    document.getElementById("loader").classList.add("hidden");

    renderAnalysis(data);
}

function renderAnalysis(data) {
    const area = document.getElementById("chatArea");
    area.innerHTML = "";

    area.innerHTML += bubble("요약", data.summary);
    area.innerHTML += bubble("핵심 키워드", data.keywords.join(", "));
    area.innerHTML += bubble("시장 영향 분석", data.impact);

    const portfolioList = data.suggested_portfolio
        .map(p => `${p.name} — ${p.weight}%`)
        .join("<br>");

    area.innerHTML += bubble("포트폴리오 추천", portfolioList);
    area.innerHTML += bubble("AI 조언", data.risk_comment);
}

function bubble(title, content) {
    return `
    <div class="chat-bubble">
        <h2>${title}</h2>
        <p>${content}</p>
    </div>`;
}
