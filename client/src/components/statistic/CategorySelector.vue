<template>
    <div class="category">
        <SelectorHeader :title="'Камеры'"
            :items="camera_items"
            :chosen="current_camera_id != null"
            @update:current="updateCurrentCameraId" />
        <div class="vertical-line"></div>
        <SelectorHeader :title="'Классы'"
            :items="class_items"
            :chosen="current_class_id != null"
            @update:current="updateCurrentClassId" />
        <div class="vertical-line"></div>
        <MultipleFilterHeader :title="'Смешанные'"
            :cameras="camera_items"
            :classes="class_items"
            :chosen="current_filters != null"
            @update:current="updateCurrentFilters" />
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
import MultipleFilterHeader from './MultipleFilterHeader.vue';

export default {
    components: {
        SelectorHeader, MultipleFilterHeader
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
            camera_items: [],
            class_items: [],
            current_camera_id: null,
            current_class_id: null,
            current_filters: null,
        }
    },

    methods: {
        updateTitles() {
            this.camera_items = [];
            this.class_items = [];
            this.cameras.forEach((camera) => {
                if (camera.id != this.current_camera_id) {
                    this.camera_items.push({
                        id: camera.id,
                        name: `Камера #${camera.id}`
                    });
                }
            });
            this.classes.forEach((class_) => {
                if (class_.id != this.current_class_id) {
                    this.class_items.push({
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
            this.current_filters = null,
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
            this.current_filters = null,
            this.$emit('update:source', {
                category: 'class',
                id: newId
            });
            this.updateTitles();
        },

        updateCurrentFilters(newFilters) {
            this.current_camera_id = null;
            this.current_class_id = null;
            this.current_filters = newFilters;
            this.$emit('update:source', {
                category: 'mixed',
                filters: newFilters,
            });
            this.updateTitles();
        }
    },

    mounted() {
        this.updateTitles();
    }
}
</script>