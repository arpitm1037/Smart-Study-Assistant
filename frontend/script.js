const chatBox = document.getElementById("chatBox");
const button = document.getElementById("sendBtn");

function addMessage(text, className) {
    const msg = document.createElement("div");
    msg.classList.add("message", className);

    
    msg.innerHTML = text.replace(/\n/g, "<br>");

    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function askQuestion() {
    const input = document.getElementById("queryInput");
    const query = input.value.trim();

    if (!query) return;

    // show user message
    addMessage(query, "user");

    input.value = "";

    
    button.disabled = true;
    button.innerText = "Thinking...";

    const loadingMsg = document.createElement("div");
    loadingMsg.classList.add("message", "bot");
    loadingMsg.innerText = "Thinking...";
    chatBox.appendChild(loadingMsg);

    chatBox.scrollTop = chatBox.scrollHeight;

    try {
        const response = await fetch("http://127.0.0.1:8000/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ query: query })
        });

        const data = await response.json();

        
        chatBox.removeChild(loadingMsg);

        
        addMessage(data.answer, "bot");

        
        if (data.mode === "RAG" && data.context && data.context.length > 0) {
            addMessage("📚 From Documents", "bot");
        } else {
            addMessage("🧠 From AI Knowledge", "bot");
        }

    } catch (error) {
        chatBox.removeChild(loadingMsg);
        addMessage("Error occurred", "bot");
    }

    
    button.disabled = false;
    button.innerText = "Send";
}