<template>
    <div class="messages-container">
        <slot name="messages"></slot>
    </div>
</template>

<style scoped>
    .messages-container {
        display: flex;
        flex-direction: column;
        row-gap: 20px;

        position: absolute;
        bottom: 50px;
        right: 50px;
        z-index: 10;
    }
</style>