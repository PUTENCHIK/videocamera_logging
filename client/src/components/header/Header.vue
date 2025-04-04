<script setup>
    const props = defineProps(['current']);
</script>

<template>
    <header>
        <div class="header__content">
            <RouterLink to="/" class="header__logo">
                <span>
                    videocameras
                    <br>
                    logging
                </span>
            </RouterLink>
            <nav>
                <RouterLink to="/classes" class="header__link">
                    <span>Классы</span>
                </RouterLink>
                <RouterLink to="/snapshots" class="header__link">
                    <span>Снимки</span>
                </RouterLink>
                <RouterLink to="/cameras" class="header__link">
                    <span>Видеокамеры</span>
                </RouterLink>
                <RouterLink to="/statistic" class="header__link">
                    <span>Статистика</span>
                </RouterLink>
                <RouterLink to="/about" class="header__link">
                    <span>О проекте</span>
                </RouterLink>
            </nav>
        </div>
    </header>
</template>

<style scoped>
    header {
        display: flex;
        position: fixed;
        width: calc(100% + 8px);
        height: 80px;
        left: -8px;
        top: 0px;

        border-bottom: 1px solid #808080;
        background-color: white;
        z-index: 8;
    }

    header a {
        text-decoration: none;
        color: black;
    }

    header > .header__content {
        display: flex;
        align-items: center;
        width: 1240px;
        height: 100%;

        margin: auto;
    }

    .header__logo {
        font-size: 24px;
        text-transform: uppercase;
        margin-right: 40px;
    }

    header nav {
        display: flex;
        width: 100%;
        height: 100%;
    }

    a.header__link {
        display: flex;
        align-items: center;
        height: 100%;
        font-size: 18px;
    }

    a.header__link:not(:last-child) {
        margin-right: 20px;
    }

    a.header__link:last-child {
        margin-left: auto;
    }

    a.header__link:hover {
        border-bottom: 3px solid #8086FF;
    }

    a.header__link.router-link-active {
        border-bottom: 3px solid #0714FF;
    }

    a.header__link > span {
        display: block;
    }
</style>