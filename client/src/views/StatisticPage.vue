<template>
    <div v-if="loading" class="loader-wrapper">
        <span class="loader"></span>
    </div>
    <div v-else-if="cameras == null || classes == null">
        <h1>Статистика</h1>
        <p>Не удалось загрузить данные камер или классов.</p>
    </div>
    <div v-else class="content">
        <CategorySelector :cameras="cameras" :classes="classes" @update:source="updateGraphicSource" />

        <div v-if="source" class="graphic-wrapper">
            <div class="graphic">
                <chart :option="chartOption" :autoresize="true" />
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
    overflow: hidden;

    outline: 1px solid blue;
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

import { firstToUpperCase } from '/src/utils/helpers';
import CamerasMixin from '/src/mixins/CamerasMixin';
import ClassesMixin from '/src/mixins/ClassesMixin';
import SnapshotsMixin from '/src/mixins/SnapshotsMixin';
import GraphicTypesMixin from '/src/mixins/GraphicTypesMixin';
import CategorySelector from '/src/components/statistic/CategorySelector.vue';

export default {
    mixins: [CamerasMixin, ClassesMixin, SnapshotsMixin],

    components: {
        CategorySelector,
        'chart': ECharts
    },

    data() {
        return {
            source: null,
            data: [
                { value: 10, imageUrl: '/src/assets/icons/bear.png' },
                { value: 20, imageUrl: '/src/assets/icons/human.png' },
                { value: 15, imageUrl: '/src/assets/icons/fox.png' }
            ],
            chartOption: {}
        }
    },

    methods: {
        getCategoryTitle() {
            if (this.source == null) {
                return "Выберите категорию и объект";
            } else {
                let result = "Статистика ";
                if (this.source.category == "camera") {
                    this.cameras.forEach((camera) => {
                        if (camera.id == this.source.id) {
                            result += `камеры #${camera.id}`;
                        }
                    });
                } else {
                    this.classes.forEach((class_) => {
                        if (class_.id == this.source.id) {
                            result += `класса '${firstToUpperCase(class_.title)}'`;
                        }
                    });
                }
                return result;
            }
        },

        updateGraphicSource(newSource) {
            this.source = newSource;
            this.chartOption = {
                title: {
                    text: this.getCategoryTitle()
                },
                xAxis: {
                    type: 'category',
                    data: ['A', 'B', 'C']
                },
                yAxis: {
                    type: 'value'
                },
                series: [
                    {
                        data: this.data.map((item) => ({
                            value: item.value,
                            symbol: 'image://' + item.imageUrl,
                            symbolSize: 24,
                            symbolOffset: [0, 0],
                        })),
                        type: 'line',
                    }
                ]
            };
        },
    },

    async mounted() {
        await this.loadCameras();
        await this.loadClasses();
        await this.loadObjects();
    }
}
</script>