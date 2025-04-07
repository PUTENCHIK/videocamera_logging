<template>
    <div class="snapshot-box">
        <div class="snapshot-content">
            <div class="snapshot-wrapper">
                <img
                    :src="'http://localhost:5050/storage/snapshots/' + data.id + '.jpg'"
                    :ref="'snapshot_' + data.id"
                    @load="onImageLoaded()"
                    alt="snapshot">
                <div
                    v-for="object in data.objects"
                    :key="object.id"
                    :ref="'bbox_' + object.id"
                    class="object-bbox"
                    :class="{ 'current' : currentBbox == object.id }"
                    :style="bbox_styles[object.id]"></div>
            </div>
        </div>

        <SnapshotDescription
            :data="this.data"
            @update:current_bbox="updateCurrent" />
    </div>
</template>

<style scoped>
    .snapshot-box {
        width: 100%;
        box-sizing: border-box;
        padding: 30px;

        display: inline-flex;
        align-items: flex-start;
        justify-content: space-between;
        column-gap: 30px;

        border-radius: 20px;
        border: 4px dashed black;
        box-shadow: 0px 5px 7px 2px rgba(34, 60, 80, 0.2);
    }

    .snapshot-content {
        width: 70%;
        display: flex;
        justify-content: center;
    }

    .snapshot-wrapper {
        display: flex;
        position: relative;
        z-index: 1;
    }

    .snapshot-wrapper > img {
        max-width: 640px;
        max-height: 640px;
        z-index: 1;
    }

    .object-bbox {
        position: absolute;
        box-sizing: border-box;
        border: 4px solid;
        border-color: black;
        border-radius: 2px;
        z-index: 2;
    }

    .object-bbox.current {
        background-color: rgba(128, 128, 128, 0.2);
        z-index: 3;
    }
</style>

<script>
import { colorToString, getClassColor } from '../../utils/helpers';
import SnapshotDescription from './SnapshotDescription.vue';

export default {
    components: {
        SnapshotDescription
    },

    props: {
        data: {
            type: Object,
            required: true
        }
    },

    data() {
        return {
            currentBbox: 0,
            bbox_styles: {},
        }
    },

    methods: {
        onImageLoaded() {
            let ref_snapshot = this.$refs['snapshot_' + this.data.id];
            this.data.objects.forEach((object) => {
                let color = getClassColor(object);
                let sizes = {
                    width: ref_snapshot.width,
                    height: ref_snapshot.height,
                }
                this.bbox_styles[object.id] = {
                    'width': `${(object.bbox.x2-object.bbox.x1) * sizes.width}px`,
                    'height': `${(object.bbox.y2-object.bbox.y1) * sizes.height}px`,
                    'top': `${(object.bbox.y1) * sizes.height}px`,
                    'left': `${(object.bbox.x1) * sizes.width}px`,
                    'border-color': `rgb(${colorToString(color)})`,
                }
            });
        },

        updateCurrent(newCurrent, newColor) {
            let idToChange = newCurrent === 0 ? this.currentBbox : newCurrent;
            if (this.bbox_styles[idToChange]) {
                this.bbox_styles[idToChange]['background-color'] = newColor;
                this.currentBbox = newCurrent;
            }
        }
    }
}
</script>