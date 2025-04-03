<script setup>
import Header from './components/header/Header.vue';
</script>

<template>
    <Header current="{{ $route.fullPath }}"></Header>
    
    <div class="main">
        <RouterView />
    </div>
</template>

<style scoped>

</style>
