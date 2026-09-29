const questionForm = document.getElementById("question-form");
const questionInput = document.getElementById("question-input");
const responseText = document.getElementById("response-text");

questionForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const question = questionInput.value;

    const response = await fetch("/api/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            question: question
        })
    });

    const data = await response.json();

    responseText.textContent = data.response;
});