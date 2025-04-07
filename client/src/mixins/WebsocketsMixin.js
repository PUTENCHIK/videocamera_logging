export default {
    data() {
        return {
            ws_messages: null
        }
    },

    methods: {
        initMessagesWebSocket() {
            const ws_reinit = 3;
            this.ws_messages = new WebSocket('ws://localhost:5050/ws/messages');
            this.ws_messages.addEventListener("open", () => {
                this.addInfo("Вебсокет", "Получение сообщений с сервера установлено");
                this.ws_inits_counter = 0;
            });
    
            this.ws_messages.addEventListener("message", (event) => {
                try {
                    const data = JSON.parse(event.data);
                    this.addMessage(data);
                } catch (e) {
                    this.addError("Получение сообщения", "Ошибка при получении сообщения с сервера");
                }                
            });
        
            this.ws_messages.addEventListener("close", () => {
                if (this.ws_inits_counter < ws_reinit) {
                    this.addWarning("Вебсокет",
                        `Соединение с вебсокетом разорвано. Переподключение ${this.ws_inits_counter+1}/${ws_reinit}`);
                    setTimeout(() => {
                        this.initMessagesWebSocket();
                    }, 3000);
                } else {
                    this.addError("Вебсокет", 'Соединение с вебсокетом разорвано');
                }
            });
        
            this.ws_messages.addEventListener("error", (error) => {
                console.error('WebSocket error:', error);
                this.ws_inits_counter++;
            });
        },
    },

    mounted() {
        this.initMessagesWebSocket();
    },
}