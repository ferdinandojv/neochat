let activeConversationId = null;
let currentSocket = null;

const conversationListEl = document.getElementById("conversationList");
const messageListEl = document.getElementById("messageList");
const chatHeaderEl = document.getElementById("chatHeader");
const messageFormEl = document.getElementById("messageForm");
const messageInputEl = document.getElementById("messageInput");
const sendBtnEl = document.getElementById("sendBtn");
const newConversationBtnEl = document.getElementById("newConversationBtn");
const newConversationDialogEl = document.getElementById("newConversationDialog");
const newConversationFormEl = document.getElementById("newConversationForm");

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
        return parts.pop().split(";").shift();
    }
    return "";
}

async function api(path, options = {}) {
    const headers = {
        "Content-Type": "application/json",
        ...(options.headers || {}),
    };

    if (["POST", "PUT", "PATCH", "DELETE"].includes((options.method || "GET").toUpperCase())) {
        headers["X-CSRFToken"] = getCookie("csrftoken");
    }

    const response = await fetch(path, {
        credentials: "same-origin",
        ...options,
        headers,
    });

    if (!response.ok) {
        throw new Error(`Erro na requisicao: ${response.status}`);
    }

    return response.json();
}

function renderConversationItem(item) {
    const div = document.createElement("div");
    div.className = `conversation-item ${item.id === activeConversationId ? "active" : ""}`;
    div.innerHTML = `
        <strong>${item.customer_name}</strong>
        <small>${item.pet_name || "Sem pet"} - ${item.channel}</small>
    `;

    div.addEventListener("click", async () => {
        activeConversationId = item.id;
        await loadConversations();
        await loadMessages(item.id, item.customer_name);
        connectConversationSocket(item.id);
    });

    return div;
}

function renderMessage(message, isRealtime = false) {
    const mine = message.sender_type === "agent";
    const div = document.createElement("div");
    div.className = `message ${mine ? "mine" : ""}`;
    div.innerHTML = `
        <div>${message.content}</div>
        <small>${message.sender_user_name || message.sender_type} - ${new Date(message.created_at).toLocaleString("pt-BR")}</small>
    `;
    messageListEl.appendChild(div);

    if (isRealtime || true) {
        messageListEl.scrollTop = messageListEl.scrollHeight;
    }
}

async function loadConversations() {
    const conversations = await api("/api/conversations/");
    conversationListEl.innerHTML = "";
    conversations.forEach((item) => {
        conversationListEl.appendChild(renderConversationItem(item));
    });
}

async function loadMessages(conversationId, customerName) {
    const messages = await api(`/api/messages/?conversation=${conversationId}`);
    messageListEl.innerHTML = "";
    chatHeaderEl.textContent = `Conversa com ${customerName}`;
    messageInputEl.disabled = false;
    sendBtnEl.disabled = false;

    messages.forEach((msg) => renderMessage(msg));
}

function connectConversationSocket(conversationId) {
    if (currentSocket) {
        currentSocket.close();
    }

    const protocol = window.location.protocol === "https:" ? "wss" : "ws";
    currentSocket = new WebSocket(`${protocol}://${window.location.host}/ws/conversations/${conversationId}/`);

    currentSocket.onmessage = (event) => {
        const payload = JSON.parse(event.data);
        if (payload.type === "chat.message") {
            renderMessage(payload.message, true);
        }
    };
}

messageFormEl.addEventListener("submit", async (event) => {
    event.preventDefault();

    if (!activeConversationId) {
        return;
    }

    const content = messageInputEl.value.trim();
    if (!content) {
        return;
    }

    const body = {
        conversation: activeConversationId,
        content,
        sender_type: "agent",
    };

    await api("/api/messages/", {
        method: "POST",
        body: JSON.stringify(body),
    });

    messageInputEl.value = "";
});

newConversationBtnEl.addEventListener("click", () => {
    newConversationDialogEl.showModal();
});

newConversationFormEl.addEventListener("submit", async (event) => {
    event.preventDefault();

    const formData = new FormData(newConversationFormEl);
    const body = {
        customer_name: formData.get("customer_name"),
        pet_name: formData.get("pet_name"),
        channel: formData.get("channel"),
        customer_phone: formData.get("customer_phone"),
        status: "open",
        priority: "medium",
        subject: "Atendimento geral",
    };

    await api("/api/conversations/", {
        method: "POST",
        body: JSON.stringify(body),
    });

    newConversationDialogEl.close();
    newConversationFormEl.reset();
    await loadConversations();
});

loadConversations();
