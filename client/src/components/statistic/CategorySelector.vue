<template>
    <div class="category">
        <SelectorHeader :title="'Камеры'"
            :items="cameras_titles"
            :chosen="current_camera_id != null"
            @update:current="updateCurrentCameraId" />
        <div class="vertical-line"></div>
        <SelectorHeader :title="'Классы'"
            :items="classes_titles"
            :chosen="current_class_id != null"
            @update:current="updateCurrentClassId" />
    </div>
</template>

<style scoped>
    .category {
        width: 100%;
        display: flex;
        align-items: center;
        column-gap: 20px;
    }

    .vertical-line {
        min-width: 2px;
        height: 60px;
        display: block;

        background-color: black;
    }
</style>

<script>
import { firstToUpperCase } from '../../utils/helpers';
import SelectorHeader from '../../components/statistic/SelectorHeader.vue';

export default {
    components: {
        SelectorHeader
    },

    props: {
        cameras: {
            type: Object,
            required: true
        },
        classes: {
            type: Object,
            required: true
        },
    },

    data() {
        return {
            cameras_titles: [],
            classes_titles: [],
            current_camera_id: null,
            current_class_id: null,
        }
    },

    methods: {
        updateTitles() {
            this.cameras_titles = [];
            this.classes_titles = [];
            this.cameras.forEach((camera) => {
                if (camera.id != this.current_camera_id) {
                    this.cameras_titles.push({
                        id: camera.id,
                        name: `Камера #${camera.id}`
                    });
                }
            });
            this.classes.forEach((class_) => {
                if (class_.id != this.current_class_id) {
                    this.classes_titles.push({
                        id: class_.id,
                        name: firstToUpperCase(class_.title)
                    });
                }
            });
        },

        updateCurrentCameraId(newId) {
            if (this.current_camera_id == newId) {
                return;
            }
            this.current_camera_id = newId;
            this.current_class_id = null;
            this.$emit('update:source', {
                category: 'camera',
                id: newId
            });
            this.updateTitles();
        },

        updateCurrentClassId(newId) {
            if (this.current_class_id == newId) {
                return;
            }
            this.current_class_id = newId;
            this.current_camera_id = null;
            this.$emit('update:source', {
                category: 'class',
                id: newId
            });
            this.updateTitles();
        }
    },

    mounted() {
        this.updateTitles();
    }
}
</script>