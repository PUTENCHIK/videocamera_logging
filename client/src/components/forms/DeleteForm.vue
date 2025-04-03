<template>
    <div class="delete-window">
        <p>Вы точно хотите удалить камеру #{{ id }}?</p>
        <div class="buttons-box">
            <button @click="handleButtonClose" class="basic close-window">
                <span>Закрыть</span>
            </button>
            <button @click="handleButtonDelete" class="danger delete-camera">
                <span>Удалить камеру</span>
            </button>
        </div>
    </div>
</template>

<style scoped>
    @import url('../../assets/styles/windows.css');

    .delete-window {
        row-gap: 30px;
        padding: 20px 30px;
    }

    .delete-window .buttons-box {
        display: flex;
        column-gap: 30px;
    }

    .delete-window p {
        margin: 0;
    }

    .delete-window button.close-window {
        display: inline-flex;
    }

    .delete-window form,
    .delete-window button.delete-camera {
        display: flex;
        width: 100%;
    }
</style>

<script>
export default {
    props: {
        id: {
            required: true
        },
        onClose: {
            type: Function,
            required: true
        },
        onDelete: {
            type: Function,
            required: true
        }
    },

    methods: {
        handleButtonClose() {
            if (this.onClose) {
                this.onClose();
            }
        },

        handleButtonDelete() {
            if (this.onDelete) {
                this.onDelete();
            }
        }
    }
}
</script>