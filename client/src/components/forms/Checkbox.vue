<template>
    <div class="wrapper" :class="{ 'checked' : checked }"></div>
</template>

<style scoped>
    .wrapper {
        min-width: 24px;
        min-height: 24px;
        box-sizing: border-box;

        display: flex;

        border-radius: 4px;
        background-color: white;
        border: 1px solid #808080;
        transition-duration: 0.3s;
    }

    .wrapper.checked {
        border: 0px;
        background-color: #0714FF;
    }

    .wrapper.checked::before {
        width: 12px;
        height: 7px;

        display: block;
        content: "";

        position: relative;
        top: 4px;
        left: 5px;

        border-bottom: 3px solid white;
        border-left: 3px solid white;
        background-color: transparent;
        transform: rotate(-45deg);
    }
</style>

<script>
export default {
    props: {
        checked: {
            type: Boolean,
            required: true
        }
    },

    data() {
        return {

        }
    },

    methods: {

    }
}
</script>