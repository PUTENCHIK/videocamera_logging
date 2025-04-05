<template>
    <div v-if="cameras == null || classes == null">
        <h1>Статистика</h1>
        <p>Не удалось загрузить данные камер или классов.</p>
    </div>
    <div v-else>
        <h2>{{ getCategoryTitle() }}</h2>

        <CategorySelector :cameras="cameras"
            :classes="classes"
            @update:source="updateGraphicSource" />
        
    </div>
</template>

<style scoped>
    /* html,
    body {
        height: 100%;
        margin: 0;
        overflow: hidden;
    }

    #app {
        height: 100vh;
        width: 100%;
    } */
</style>

<script>
import { firstToUpperCase } from '/src/utils/helpers';
import CamerasMixin from '/src/utils/CamerasMixin';
import ClassesMixin from '/src/utils/ClassesMixin';
import CategorySelector from '/src/components/statistic/CategorySelector.vue';

export default {
    mixins: [CamerasMixin, ClassesMixin],

    components: {
        CategorySelector
    },

    data() {
        return {
            source: null,
        }
    },

    methods: {
        updateGraphicSource(newSource) {
            this.source = newSource;
        },

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
    },

    async mounted() {
        await this.loadCameras();
        await this.loadClasses();
    }
}
</script>