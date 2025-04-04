<script setup>
import Header from './components/header/Header.vue';
import MessagesContainer from './components/messages/MessagesContainer.vue';
import Message from './components/messages/Message.vue';
</script>

<template>
    <Header current="{{ $route.fullPath }}"></Header>
    
    <div class="main">
        <RouterView />
        <MessagesContainer>
            <template #messages>
                <Message v-for="message in messages"
                    :key="message.id"
                    :data="message"
                    :onClose="deleteMessage" />
            </template>
        </MessagesContainer>
    </div>
</template>

<style scoped>

</style>

<script>
export default {
    components: {
        Header, MessagesContainer, Message
    },

    data() {
        return {
            max_messages: 4,
            messages: [],
            message_id: 1
        }
    },

    provide() {
        return {
            addError: this.addError,
            addWarning: this.addWarning,
            addInfo: this.addInfo,
        }
    },

    methods: {
        addError(title, text) {
            this.addMessage({
                title: title,
                text: text
            }, "error", 10000);
        },

        addWarning(title, text) {
            this.addMessage({
                title: title,
                text: text
            }, "warning", 7500);
        },

        addInfo(title, text) {
            this.addMessage({
                title: title,
                text: text
            }, "info", 5000);
        },

        addMessage(message, type, delay) {
            message.id = this.message_id++;
            if (type != undefined) {
                message.type = type;
            }
            if (this.messages.length === this.max_messages) {
                this.messages.pop();
            }
            this.messages.unshift(message);
            if (delay != undefined) {
                setTimeout(() => {
                    this.deleteMessage(message.id);
                }, delay);
            }
        },

        deleteMessage(id) {
            let index;
            for (let i = 0; i < this.messages.length; i++) {
                let message = this.messages[i];
                if (message.id === id) {
                    index = i;
                    break;
                }
            };
            if (index != undefined) {
                this.messages.splice(index, 1);
            }
        },

        initMessagesWebSocket() {
            const ws_reinit = 3;
            this.ws_messages = new WebSocket('ws://localhost:5050/ws');
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
    }
}
</script>