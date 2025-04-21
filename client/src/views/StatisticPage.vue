<template>
    <div v-if="loading" class="loader-wrapper">
        <span class="loader"></span>
    </div>
    <template v-else-if="cameras == null || classes == null">
        <h1>Статистика</h1>
        <p>Не удалось загрузить данные камер или классов.</p>
    </template>
    <div v-else class="content">
        <CategorySelector :cameras="cameras"
            :classes="classes"
            @update:source="updateGraphicSource" />

        <div v-if="source" class="graphic-wrapper">
            <div class="graphic">
                <chart ref="graphic"
                    :option="chart_option"
                    :autoresize="true"
                    @click="chartClickHandle" />
            </div>

            <div class="graphic-info">
                <h2>Подробная информация</h2>
                <div class="__content">
                    <div class="row">
                        <div>Общее количество: {{ graphic_info.amount }}</div>
                        <div>Промежуток: {{ graphic_data.min_date || '-' }} - {{ graphic_data.max_date || '-' }}</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
    @import url('../assets/styles/loader.css');

    .content {
        display: flex;
        flex-direction: column;
        row-gap: 30px;
    }

    .graphic-wrapper {
        display: flex;
        flex-direction: column;
        row-gap: 30px;
    }

    .graphic {
        height: 400px;
        min-height: 200px;
        max-height: 700px;
        resize: vertical;
        
        outline: 1px solid blue;
        overflow: hidden;
    }

    .graphic-info {
        display: flex;
        flex-direction: column;
        row-gap: 20px;
    }
    
    .graphic-info > .__content {
        display: flex;
        flex-direction: column;
        row-gap: 15px;
    }

    .graphic-info .row {
        display: flex;
        justify-content: space-between;
    }
</style>

<script>
import ECharts from 'vue-echarts';
import * as echarts from 'echarts';

import GraphicTypesMixin from '../mixins/GraphicTypesMixin';
import CategorySelector from '../components/statistic/CategorySelector.vue';

export default {
    inject: ['addError', 'addWarning', 'addInfo', 'deleteAllMessages'],

    mixins: [GraphicTypesMixin],

    components: {
        CategorySelector,
        'chart': ECharts
    },

    data() {
        return {
            
        }
    },

    methods: {
        updateGraphicSource(newSource) {
            this.source = newSource;
            this.no_trackable_class_warning_shown = false;
            this.updateChartOption();
        },

        chartClickHandle(event) {
            if (event && event.data) {
                let object = event.data.value[2];
                if (object && object.snapshot_id) {
                    this.$router.push({
                        path: '/snapshots',
                        hash: `#${object.snapshot_id}`
                    });
                } else {
                    this.addError(
                        "Нет снимка",
                        `Не удалось перейти к объекту #${object.id}`
                    );
                }
            }
        },
    },

    mounted() {
        this.deleteAllMessages();
    }
}
</script>