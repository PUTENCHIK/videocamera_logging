import { createApp } from 'vue'
import './assets/styles/common.css'
import App from './App.vue'

import { createMemoryHistory, createRouter } from 'vue-router'
import MainPage from './views/MainPage.vue'
import ClassesPage from './views/ClassesPage.vue'
import SnapshotsPage from './views/SnapshotsPage.vue'
import CamerasPage from './views/CamerasPage.vue'
import StatisticPage from './views/StatisticPage.vue'
import AboutPage from './views/AboutPage.vue'

const routes = [
    { path: '/', component: MainPage, name: 'Главная' },
    { path: '/classes', component: ClassesPage, name: 'Классы' },
    { path: '/snapshots', component: SnapshotsPage, name: 'Снимки' },
    { path: '/cameras', component: CamerasPage, name: 'Видеокамеры' },
    { path: '/statistic', component: StatisticPage, name: 'Статистика' },
    { path: '/about', component: AboutPage, name: 'О проекте' },
]

const router = createRouter({
    history: createMemoryHistory(),
    routes,
})

router.beforeEach((to, from, next) => {
    document.title = to.name || 'Videocamera Logging';
    next();
});

createApp(App)
    .use(router)
    .mount('#app')
