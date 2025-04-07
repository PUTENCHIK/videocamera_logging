<script setup>
import WebsocketsMixin from './mixins/WebsocketsMixin';
import Header from './components/header/Header.vue';
import MessagesContainer from './components/messages/MessagesContainer.vue';
import Message from './components/messages/Message.vue';
</script>

<template>
    <Header current="{{ $route.fullPath }}"></Header>
    
    <main>
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
    </main>
</template>

<style scoped>
    main {
        height: calc(100% - 40px);
        margin-top: 80px;
        overflow-y: auto;
    }
</style>

<script>
export default {
    components: {
        Header, MessagesContainer, Message
    },

    mixins: [WebsocketsMixin],

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
            deleteAllMessages: this.deleteAllMessages
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

        deleteAllMessages() {
            this.messages = [];
        },

        
    }
}
</script>