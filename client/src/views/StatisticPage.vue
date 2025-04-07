<template>
    <div v-if="loading" class="loader-wrapper">
        <span class="loader"></span>
    </div>
    <template v-else-if="cameras == null || classes == null">
        <h1>Статистика</h1>
        <p>Не удалось загрузить данные камер или классов.</p>
    </template>
    <div v-else class="content">
        <CategorySelector :cameras="cameras" :classes="classes" @update:source="updateGraphicSource" />

        <div v-if="source" class="graphic-wrapper">
            <div class="graphic">
                <chart ref="graphic"
                    :option="chartOption"
                    :autoresize="true" />
            </div>

            <div class="graphic-info">
                <h2>Информация</h2>
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
    height: 200px;
    display: flex;

    background-color: antiquewhite;
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
            this.updateChartOption();
            console.log(this.$refs.graphic);
        },
    },

    mounted() {
        this.deleteAllMessages();
    }
}
</script>