<template>
    <div class="wrapper">

    </div>
</template>

<style scoped>
    :root {
        --checkbox-size: 32px
    }

    .wrapper {
        width: var(--checkbox-size);
        height: var(--checkbox-size);
        box-sizing: border-box;

        display: flex;

        border-radius: 4px;
        background-color: white;
        border: 1px solid #808080;
    }
</style>

<script>
export default {
    props: {
        checked: {
            type: Boolean,
            required: true
        },
        size: {
            type: Number
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