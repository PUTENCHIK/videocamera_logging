<template>
    <h1>Снимки с камер</h1>

    <div v-if="!loading" class="__content">
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
            <div v-for="snapshot in snapshots" class="snapshot-box" :key="snapshot.id">
                <div class="snapshot-content">
                    <div class="snapshot-wrapper">
                        <img
                            :src="'http://localhost:5050/storage/snapshots/' + snapshot.id + '.jpg'"
                            :ref="'snapshot_' + snapshot.id"
                            @load="onSnapshotImageLoaded(snapshot)"
                            alt="snapshot">
                        <div
                            v-for="object in snapshot.objects"
                            :key="object.id"
                            class="object-bbox"
                            :class="{ 'current' : objectBboxHoverId == object.id }"
                            :style="objects_styles[object.id]"></div>
                    </div>
                </div>

                <div class="snapshot-description">
                    <div class="snapshot-information">
                        <div class="__content">
                            <h3>Общая информация:</h3>
                            <div class="information-rows">
                                <span>ID: {{ snapshot.id }}</span>
                                <span>Сохранено: {{ snapshot.created_at }}</span>
                                <span>ID камеры: {{ snapshot.camera_id }}</span>
                            </div>
                        </div>
                        <img src="/src/assets/icons/info.svg" alt="info">
                    </div>
                    <div class="objects-box">
                        <h3>Замеченные объекты:</h3>
                        <div class="objects">
                            <div
                                    v-for="object in snapshot.objects"
                                    :key="object.id"
                                    @mouseover="handlerObjectIconMouseover(object.id, (object.trackable_class?.color || default_color))"
                                    @mouseleave="handlerObjectIconMouseleave"
                                    class="object-icon-wrapper">
                                <img
                                    :src="'/src/assets/icons/' + (object.trackable_class?.name || 'unknown') + '.png'"
                                    :alt="(object.trackable_class?.name || 'unknown')"
                                    :title="(object.trackable_class?.title || 'unknown') + ': ' + object.probability">
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <p v-else>В базе нет ещё ни одного снимка с камер.</p>
    </div>
    <div v-else class="loader-wrapper">
        <span class="loader"></span>
    </div>
</template>

<style scoped>
    @import url('../assets/styles/loader.css');
    @import url('../assets/styles/messages.css');

    :root {
        --color-bbox-hover: rgba(0, 0, 0, 0.2);
    }

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

    .snapshot-description {
        width: 30%;
        padding: 15px 20px;

        display: flex;
        flex-direction: column;
        row-gap: 40px;

        border-radius: 8px;
        border: 3px solid black;
        box-shadow: 0px 5px 7px 2px rgba(34, 60, 80, 0.2);
    }

    .snapshot-information {
        display: flex;
        column-gap: 30px;
    }

    .snapshot-information > .__content {
        display: flex;
        flex-direction: column;
        row-gap: 15px;
    }

    .information-rows {
        display: inline-flex;
        flex-direction: column;
        row-gap: 10px;

        font-weight: 600;
    }

    .objects-box {
        display: flex;
        flex-direction: column;
        row-gap: 10px;
    }

    .objects {
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
        gap: 10px;
    }

    .object-icon-wrapper {
        width: 48px;
        height: 48px;

        display: flex;
        justify-content: center;
        align-items: center;

        box-sizing: border-box;
        border-radius: 15px;
    }

    .object-icon-wrapper:hover {
        background-color: var(--color-bbox-hover);
        border: none;
    }

    .object-icon-wrapper > img {
        width: 36px;
        height: 36px;
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
        background-color: var(--color-bbox-hover);
        z-index: 3;
    }
</style>

<script>
import axios from 'axios';
import { formatDate, colorToString } from '/src/utils/helpers';

export default {
    data() {
        return {
            loading: false,
            snapshots: [],
            objectBboxHoverId: 0,
            default_color: {r: 128, g: 128, b: 128},
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
                this.formatDates();
            } catch (error) {
                throw(error);
            } finally {
                this.loading = false;
            }
        },

        formatDates() {
            this.snapshots.forEach((snapshot) => {
                snapshot.created_at = formatDate(snapshot.created_at);
            });
        },

        handlerObjectIconMouseover(id, color) {
            this.objectBboxHoverId = id;
            document.documentElement.style.setProperty('--color-bbox-hover', `rgba(${colorToString(color)}, 0.2)`);
        },

        handlerObjectIconMouseleave() {
            this.objectBboxHoverId = 0;
        },

        getSnapshotImageSizes(id) {
            
            console.log(img_snapshot);
            
            if (img_snapshot === undefined) {
                return {
                    width: 640,
                    height: 480,
                }
            } else {
                return {
                    width: img_snapshot[0].width,
                    height: img_snapshot[0].height,
                } 
            }
        },

        onSnapshotImageLoaded(snapshot) {
            let img_snapshot = this.$refs['snapshot_' + snapshot.id][0];
            snapshot.objects.forEach((object) => {
                let color;
                if (object.trackable_class !== null) {
                    color = object.trackable_class.color;
                } else {
                    color = this.default_color;
                }
                let sizes = {
                    width: img_snapshot.width,
                    height: img_snapshot.height,
                }
                
                this.objects_styles[object.id] = {
                    'width': `${(object.bbox.x2-object.bbox.x1) * sizes.width}px`,
                    'height': `${(object.bbox.y2-object.bbox.y1) * sizes.height}px`,
                    'top': `${(object.bbox.y1) * sizes.height}px`,
                    'left': `${(object.bbox.x1) * sizes.width}px`,
                    'border-color': `rgb(${colorToString(color)})`,
                }
            });
        },
    },

    mounted() {
        this.loadSnapshots();
    }
}
</script>