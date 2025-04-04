<template>
    <div class="forms-container"
        @mousedown="(event) => handleMouseDown(event)"
        @mouseup="(event) => handleMouseUp(event)">
        <slot name="form">
            <span>Form must be defined</span>
        </slot>
    </div>
</template>

<style scoped>
    .forms-container {
        position: absolute;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        display: flex;

        background-color: rgba(69, 69, 69, 0.4);
        z-index: 9;
    }
</style>

<script>
export default {
    props: {
        onClose: {
            type: Function,
            required: true
        }
    },

    data() {
        return {
            was_mouse_down: false
        }
    },

    methods: {
        handleMouseDown(event) {
            if (event.target.className === "forms-container") {
                this.was_mouse_down = true;
            }
        },

        handleMouseUp(event) {
            if (this.was_mouse_down && event.target.className === "forms-container") {
                this.was_mouse_down = false;
                if (this.onClose) {
                    this.onClose();
                }
            }
        }
    }
}
</script>