const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');
const typingIndicator = document.getElementById('typing-indicator');

// 支持回车发送
userInput.addEventListener('keypress', function (e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    // 禁用输入和按钮
    userInput.disabled = true;
    sendButton.disabled = true;

    // 添加用户消息
    addMessage(message, 'user');

    // 清空输入框
    userInput.value = '';

    // 显示"正在思考"提示
    showTypingIndicator();

    // 调用Django后端API
    fetch('/api/chat/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify({
            message: message,
            // 可以添加更多参数，如会话ID等
            session_id: getSessionId()
        })
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP错误! 状态: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }
            // 添加AI回复
            addMessage(data.reply, 'bot');
        })
        .catch(error => {
            console.error('Error:', error);
            addMessage('抱歉，服务暂时不可用，请稍后再试。', 'bot');
        })
        .finally(() => {
            // 隐藏思考提示，重新启用输入
            hideTypingIndicator();
            userInput.disabled = false;
            sendButton.disabled = false;
            userInput.focus();
        });
}

function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;

    if (sender === 'bot') {
        const avatar = document.createElement('div');
        avatar.className = `avatar bot-avatar`;
        const img = document.createElement('img');
        img.src = '/static/home/img/indeximg/chat_ai_avatar.jpg';
        img.alt = 'AI头像';
        avatar.appendChild(img);
        messageDiv.appendChild(avatar);
    }
    // 用户消息不添加头像

    const content = document.createElement('div');
    content.className = `message-content ${sender}-content`;
    if (sender === 'bot' && window.marked) {
        content.innerHTML = marked.parse(text);
    } else {
        content.textContent = text;
    }

    messageDiv.appendChild(content);
    chatMessages.appendChild(messageDiv);

    // 滚动到底部
    scrollToBottom();
}

function showTypingIndicator() {
    typingIndicator.style.display = 'block';
    scrollToBottom();
}

function hideTypingIndicator() {
    typingIndicator.style.display = 'none';
}

function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function getCSRFToken() {
    const name = 'csrftoken';
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function getSessionId() {
    // 生成或获取会话ID，用于保持对话上下文
    let sessionId = sessionStorage.getItem('ai_chat_session_id');
    if (!sessionId) {
        sessionId = Date.now().toString() + Math.random().toString(36).substr(2, 9);
        sessionStorage.setItem('ai_chat_session_id', sessionId);
    }
    return sessionId;
}

// 页面加载时自动聚焦到输入框
window.addEventListener('load', function () {
    userInput.focus();
});