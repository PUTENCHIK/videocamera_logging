<template>
    <div class="message"
        :class="data.type"
        @mousedown="handleClick">
        <div class="icon-wrapper">
            <img :src="'/src/assets/icons/' + data.type + '.png'"
                :alt="data.type">
        </div>
        <div class="__content">
            <div class="title label-bold">{{ data.title }}</div>
            <div class="text">{{ data.text }}</div>
        </div>
    </div>
</template>

<style scoped>
    .message {
        width: 350px;
        box-sizing: border-box;
        padding: 20px;

        display: flex;
        column-gap: 15px;

        border-radius: 10px;
        background-color: #808080;
        box-shadow: 5px 5px 7px #808080;
        color: #fff;
    }

    .message:hover {
        cursor: pointer;
    }

    .message.info {
        background-color: #0790FF;
    }

    .message.warning {
        background-color: #FF9C46;
    }

    .message.error {
        background-color: #FF4649;
    }

    .message .icon-wrapper {
        display: flex;
        align-items: center;
        user-select: none;
    }

    .message .icon-wrapper > img {
        width: 28px;
        height: 28px;
        display: inline-block;
    }

    .message .__content {
        width: 100%;

        display: flex;
        flex-direction: column;
        row-gap: 8px;

        word-break: break-word;
    }
</style>

<script>
export default {
    props: {
        data: {
            type: Object,
            required: true
        },
        onClose: {
            type: Function,
            required: true
        }
    },

    methods: {
        handleClick(event) {
            let b = event.button;
            if ((b == 0 || b == 1) && this.onClose) {
                this.onClose(this.data.id);
            }
        }
    }
}
</script>