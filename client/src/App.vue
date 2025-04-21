<script setup>
import { MESSAGES_DELAY } from './constants';

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
        padding-top: 80px;
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
            message_id: 1,
            API_PORT: import.meta.env.VITE_API_PORT,
        }
    },

    provide() {
        return {
            addError: this.addError,
            addWarning: this.addWarning,
            addInfo: this.addInfo,
            deleteAllMessages: this.deleteAllMessages,
            API_PORT: this.API_PORT
        }
    },

    methods: {
        addError(title, text) {
            this.addMessage({
                title: title,
                text: text
            }, "error", MESSAGES_DELAY['error']);
        },

        addWarning(title, text) {
            this.addMessage({
                title: title,
                text: text
            }, "warning", MESSAGES_DELAY['warning']);
        },

        addInfo(title, text) {
            this.addMessage({
                title: title,
                text: text
            }, "info", MESSAGES_DELAY['info']);
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
    },
}
</script>