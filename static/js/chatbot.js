/* =====================================================
   CHATBOT.JS — AI Portfolio Assistant Widget
   ===================================================== */

class PortfolioChatbot {
    constructor() {
        this.trigger = document.querySelector('.chatbot-trigger');
        this.window = document.querySelector('.chatbot-window');
        this.messagesContainer = document.querySelector('.chatbot-messages');
        this.input = document.querySelector('.chatbot-input');
        this.sendBtn = document.querySelector('.chatbot-send');

        if (!this.trigger || !this.window) return;

        this.sessionId = this.generateSessionId();
        this.isOpen = false;

        this.init();
    }

    init() {
        // Toggle chat window
        this.trigger.addEventListener('click', () => this.toggle());

        // Send message
        this.sendBtn.addEventListener('click', () => this.sendMessage());
        this.input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendMessage();
        });

        // Quick actions
        document.querySelectorAll('.quick-action-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                this.input.value = btn.dataset.message;
                this.sendMessage();
            });
        });

        // Welcome message
        this.addBotMessage(
            "👋 Hi! I'm Gagan's AI assistant. Ask me anything about his projects, " +
            "skills, experience, or certifications. How can I help you today?"
        );
    }

    toggle() {
        this.isOpen = !this.isOpen;
        this.trigger.classList.toggle('active');
        this.window.classList.toggle('open');

        if (this.isOpen) {
            setTimeout(() => this.input.focus(), 300);
        }
    }

    async sendMessage() {
        const message = this.input.value.trim();
        if (!message) return;

        // Add user message
        this.addUserMessage(message);
        this.input.value = '';

        // Show typing indicator
        const typingEl = this.showTyping();

        try {
            const response = await fetch('/api/chat/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: message,
                    session_id: this.sessionId,
                }),
            });

            const data = await response.json();

            // Remove typing indicator
            typingEl.remove();

            if (data.response) {
                this.addBotMessage(data.response, data.action, data.action_url);
            } else if (data.error) {
                this.addBotMessage("Sorry, I encountered an error. Please try again.");
            }
        } catch (error) {
            typingEl.remove();
            this.addBotMessage("I'm having trouble connecting. Please try again later.");
        }
    }

    addUserMessage(text) {
        const messageEl = document.createElement('div');
        messageEl.className = 'chat-message user';
        messageEl.innerHTML = `
            <div class="chat-message-avatar">👤</div>
            <div class="chat-bubble">${this.escapeHtml(text)}</div>
        `;
        this.messagesContainer.appendChild(messageEl);
        this.scrollToBottom();
    }

    addBotMessage(text, action, actionUrl) {
        const messageEl = document.createElement('div');
        messageEl.className = 'chat-message bot';

        let actionHtml = '';
        if (action === 'download_resume' && actionUrl) {
            actionHtml = `<a href="${actionUrl}" class="chat-action-btn" download>📄 Download Resume</a>`;
        }

        messageEl.innerHTML = `
            <div class="chat-message-avatar">🤖</div>
            <div class="chat-bubble">
                ${this.formatMarkdown(text)}
                ${actionHtml}
            </div>
        `;
        this.messagesContainer.appendChild(messageEl);
        this.scrollToBottom();
    }

    showTyping() {
        const typingEl = document.createElement('div');
        typingEl.className = 'chat-message bot';
        typingEl.innerHTML = `
            <div class="chat-message-avatar">🤖</div>
            <div class="chat-bubble">
                <div class="typing-indicator">
                    <span></span><span></span><span></span>
                </div>
            </div>
        `;
        this.messagesContainer.appendChild(typingEl);
        this.scrollToBottom();
        return typingEl;
    }

    formatMarkdown(text) {
        // Basic markdown formatting
        return text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/## (.*?)$/gm, '<h3>$1</h3>')
            .replace(/### (.*?)$/gm, '<h4>$1</h4>')
            .replace(/\n\n/g, '<br><br>')
            .replace(/\n/g, '<br>')
            .replace(/📧|🔗|📱|📍|🏆|🎓|📅|---/g, match => match);
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    scrollToBottom() {
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }

    generateSessionId() {
        return 'session_' + Math.random().toString(36).substr(2, 9);
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    new PortfolioChatbot();
});
