<template>
    <h1>Главная страница</h1>

    <p>Информация о приложении</p>
</template>

<script>
export default {
    inject: ['addError', 'addWarning', 'addInfo', 'deleteAllMessages'],

    mounted() {
        this.deleteAllMessages();
    }
}
</script>