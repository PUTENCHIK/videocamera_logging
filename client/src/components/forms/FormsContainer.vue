<template>
    <div class="forms-container">
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