<template>
    <div class="snapshot-description">
        <div class="snapshot-information">
            <div class="__content">
                <h3>Общая информация:</h3>
                <div class="information-rows">
                    <span>ID: {{ data.id }}</span>
                    <span>Сохранено: {{ data.created_at }}</span>
                    <span>ID камеры: {{ data.camera_id }}</span>
                </div>
            </div>
            <img src="/src/assets/icons/info.svg" alt="info">
        </div>
        <div class="objects-box">
            <h3>Замеченные объекты:</h3>
            <div class="objects">
                <div v-for="object in data.objects"
                    :key="object.id"
                    :ref="'icon_' + object.id"
                    @mouseover="handlerObjectIconMouseover(object)"
                    @mouseleave="handlerObjectIconMouseleave(object)"
                    class="object-icon-wrapper"
                    :style="icon_styles[object.id]">

                    <img :src="'/src/assets/icons/' + (object.trackable_class?.name || 'unknown') + '.png'"
                        :alt="(object.trackable_class?.name || 'unknown')"
                        :title="(object.trackable_class?.title || 'unknown') + ': ' + object.probability">
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
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

        border: none;
        box-sizing: border-box;
        border-radius: 15px;
    }

    .object-icon-wrapper > img {
        width: 36px;
        height: 36px;
    }
</style>

<script>
import { colorToString, getClassColor } from '../../utils/helpers';

export default {
    props: {
        data: {
            type: Object,
            required: true
        }
    },

    data() {
        return {
            icon_styles: {},
        }
    },

    methods: {
        handlerObjectIconMouseover(object) {
            let color = `rgba(${colorToString(getClassColor(object))}, 0.2)`;
            this.$emit('update:current_bbox', object.id, color);
            this.icon_styles[object.id]['background-color'] = color;
        },

        handlerObjectIconMouseleave(object) {
            this.$emit('update:current_bbox', 0, 'transparent');
            this.icon_styles[object.id]['background-color'] = 'transparent';
        },
    },

    mounted() {
        this.data.objects.forEach((object) => {
            this.icon_styles[object.id] = {
                'backgroud-color': 'transparent'
            }
        });
    }
}
</script>