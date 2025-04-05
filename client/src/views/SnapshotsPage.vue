<template>
    <h1>Снимки с камер</h1>

    <div v-if="loading" class="loader-wrapper">
        <span class="loader"></span>
    </div>
    <p v-else-if="snapshots == null">Не удалось загрузить снимки с камер.</p>
    <div v-else class="__content">
        <div v-if="snapshots.length" class="filters-container">
            <form name="filters">
                <div class="form-group">
                    <label class="filled">
                        <span>id изображения:</span>
                        <input type="number" name="id" min="1" placeholder="123">
                    </label>
                    <label class="fixed">
                        <span>От:</span>
                        <input type="date" name="from">
                    </label>
                    <label class="fixed">
                        <span>До:</span>
                        <input type="date" name="until">
                    </label>
                    <label class="filled">
                        <span>Кол-во объектов:</span>
                        <input type="number" name="amount" min="1" value="1">
                    </label>
                </div>

                <button class="primary" type="submit">
                    <span>Применить</span>
                </button>
            </form>
        </div>

        <div v-if="snapshots.length" class="snapshots-container">
            <SnapshotBox v-for="snapshot in snapshots"
                :key="snapshot.id"
                :data="snapshot" />
        </div>
        <p v-else>В базе нет ещё ни одного снимка с камер.</p>
    </div>
</template>

<style scoped>
    @import url('../assets/styles/loader.css');

    .main > .__content {
        display: flex;
        flex-direction: column;
        row-gap: 40px;
    }

    .filters-container {
        display: flex;
        width: 100%;
    }

    .filters-container > form {
        display: flex;
        align-items: center;
        justify-content: space-between;
        width: 100%;
    }

    form > .form-group {
        display: flex;
        column-gap: 20px;
    }

    .snapshots-container {
        display: flex;
        flex-direction: column;
        gap: 32px;
    }
</style>

<script>
import axios from 'axios';
import { formatDate } from '/src/utils/helpers';
import SnapshotBox from '/src/components/snapshots/SnapshotBox.vue';

export default {
    inject: ['addError', 'addWarning', 'addInfo'],

    components: {
        SnapshotBox
    },

    data() {
        return {
            loading: false,
            snapshots: null,
            objectBboxHoverId: 0,
            objects_styles: {}
        }
    },

    methods: {
        async loadSnapshots() {
            try {
                this.loading = true;
                const response = await axios.get(
                    "http://localhost:5050/api/snapshots"
                );
                this.snapshots = response.data;
            } catch (error) {
                this.addError("Загрузка снимков", `Получена ошибка: ${error}`);
                throw(error);
            } finally {
                this.loading = false;
                this.formatDates();
            }
        },

        formatDates() {
            this.snapshots.forEach((snapshot) => {
                snapshot.created_at = formatDate(snapshot.created_at);
            });
        },
    },

    mounted() {
        this.loadSnapshots();
    }
}
</script>