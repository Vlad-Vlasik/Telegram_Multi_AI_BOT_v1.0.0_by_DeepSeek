// Функціонал для DeepSeek чату
class DeepSeekChat {
    constructor() {
        this.init();
    }

    init() {
        this.initCopyButtons();
        this.initFeedbackButtons();
        this.initCodeBlocks();
        this.addStyles();
    }

    initCopyButtons() {
        // Копіювання тексту повідомлень
        document.querySelectorAll('.copy-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const messageContent = e.target.closest('.message-content');
                const messageText = messageContent.querySelector('.message-text');
                this.copyToClipboard(this.getTextContent(messageText));
                this.showCopyFeedback('Текст скопійовано!', e.target);
            });
        });

        // Копіювання коду
        document.querySelectorAll('.copy-code-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const codeBlock = e.target.closest('.code-block');
                const code = codeBlock.querySelector('code');
                this.copyToClipboard(code.textContent);
                this.showCopyFeedback('Код скопійовано!', e.target);
            });
        });
    }

    initFeedbackButtons() {
        document.querySelectorAll('.feedback-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                const isLike = e.target.closest('.like-btn');
                this.handleFeedback(isLike, e.target);
            });
        });
    }

    initCodeBlocks() {
        // Підсвітка синтаксису для блоків коду
        document.querySelectorAll('.code-block code').forEach(block => {
            this.highlightSyntax(block);
        });
    }

    getTextContent(element) {
        // Отримання текстового вмісту з форматуванням
        let text = '';
        
        // Обробка параграфів
        element.querySelectorAll('p').forEach(p => {
            text += p.textContent + '\n\n';
        });
        
        // Обробка списків
        element.querySelectorAll('ul, ol').forEach(list => {
            list.querySelectorAll('li').forEach((li, index) => {
                text += `${index + 1}. ${li.textContent}\n`;
            });
            text += '\n';
        });
        
        // Обробка код-блоків
        element.querySelectorAll('.code-block').forEach(codeBlock => {
            const code = codeBlock.querySelector('code');
            if (code) {
                text += code.textContent + '\n\n';
            }
        });
        
        return text.trim();
    }

    async copyToClipboard(text) {
        try {
            await navigator.clipboard.writeText(text);
            return true;
        } catch (err) {
            // Fallback для старих браузерів
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            return true;
        }
    }

    showCopyFeedback(message, target) {
        const feedback = document.createElement('div');
        feedback.textContent = message;
        feedback.style.cssText = `
            position: absolute;
            background: #10b981;
            color: white;
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 500;
            z-index: 1000;
            pointer-events: none;
            animation: fadeInOut 2s ease-in-out;
        `;

        const rect = target.getBoundingClientRect();
        feedback.style.top = `${rect.top - 40}px`;
        feedback.style.left = `${rect.left}px`;

        document.body.appendChild(feedback);

        setTimeout(() => {
            feedback.remove();
        }, 2000);
    }

    handleFeedback(isLike, button) {
        const message = button.closest('.message');
        const feedbackBtns = message.querySelectorAll('.feedback-btn');
        
        // Скидання стану інших кнопок
        feedbackBtns.forEach(btn => {
            btn.style.background = 'white';
            btn.style.color = '#64748b';
            btn.style.borderColor = '#e2e8f0';
        });
        
        // Встановлення стану обраної кнопки
        if (isLike) {
            button.style.background = '#10b981';
            button.style.color = 'white';
            button.style.borderColor = '#10b981';
        } else {
            button.style.background = '#ef4444';
            button.style.color = 'white';
            button.style.borderColor = '#ef4444';
        }
        
        // Показати тимчасове підтвердження
        this.showFeedbackConfirm(isLike, button);
    }

    showFeedbackConfirm(isLike, button) {
        const confirm = document.createElement('div');
        confirm.textContent = isLike ? 'Дякую за лайк! 👍' : 'Дякую за відгук! 👎';
        confirm.style.cssText = `
            position: absolute;
            background: ${isLike ? '#10b981' : '#ef4444'};
            color: white;
            padding: 6px 10px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 500;
            z-index: 1000;
            pointer-events: none;
            animation: fadeInOut 1.5s ease-in-out;
        `;

        const rect = button.getBoundingClientRect();
        confirm.style.top = `${rect.top - 35}px`;
        confirm.style.left = `${rect.left}px`;

        document.body.appendChild(confirm);

        setTimeout(() => {
            confirm.remove();
        }, 1500);
    }

    highlightSyntax(codeElement) {
        // Базова підсвітка ключових слів (спрощена версія)
        const code = codeElement.textContent;
        const keywords = [
            'class', 'def', 'return', 'if', 'else', 'for', 'while',
            'import', 'from', 'as', 'try', 'except', 'finally',
            'self', 'True', 'False', 'None', 'async', 'await'
        ];
        
        let highlighted = code;
        
        keywords.forEach(keyword => {
            const regex = new RegExp(`\\b${keyword}\\b`, 'g');
            highlighted = highlighted.replace(regex, `<span class="keyword">${keyword}</span>`);
        });
        
        // Підсвітка рядків
        highlighted = highlighted.replace(/(['"])(.*?)\1/g, '<span class="string">$1$2$1</span>');
        
        // Підсвітка коментарів
        highlighted = highlighted.replace(/(#.*$)/gm, '<span class="comment">$1</span>');
        
        codeElement.innerHTML = highlighted;
    }