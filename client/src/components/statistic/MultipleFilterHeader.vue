<template>
    <div v-click-outside="handleClickOutside"
        class="selector-header"
        :class="{ 'chosen': chosen }"
        @click="updateFilters">

        <div class="title-wrapper" @click="updateChoosing">
            <span class="title">{{ title }}</span>
        </div>

        <div v-if="choosing" class="items-wrapper">
            <div class="items-container">
                <div class="items">
                    <div v-for="item in cameras"
                        :key="item.id"
                        @click="updateSelected(item, selected_cameras)"
                        class="item">
                        <Checkbox :checked="checkItemIsSelected(item, selected_cameras)" />
                        <span :title="item.name">{{ item.name }}</span>
                    </div>
                </div>
    
                <div class="items">
                    <div v-for="item in classes"
                        :key="item.id"
                        @click="updateSelected(item, selected_classes)"
                        class="item">
                        <Checkbox :checked="checkItemIsSelected(item, selected_classes)" />
                        <span :title="item.name">{{ item.name }}</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
    .selector-header {
        width: 100%;

        display: flex;
        flex-direction: column;
    }

    .title-wrapper {
        width: 100%;
        height: 60px;

        display: flex;
        align-items: center;
        justify-content: center;

        box-sizing: border-box;
        cursor: pointer;
        color: #414141;
    }

    .title-wrapper:hover {
        box-shadow: 0 2px 0 0 #808080;
    }

    .selector-header.chosen .title-wrapper {
        color: #000000;
        box-shadow: 0 2px 0 0 black;
    }

    span.title {
        font-size: 20px;
    }

    .items-wrapper {
        width: 100%;

        position: relative;
        top: 10px;
        z-index: 5;
    }

    .items-container {
        width: 100%;

        display: flex;
        column-gap: 10px;
        align-items: start;

        position: absolute;
    }

    .items {
        width: 100%;
        max-height: 500px;
        
        display: flex;
        flex-direction: column;
        overflow-y: auto;

        border-radius: 10px;
        background-color: white;
        outline: 1px solid black;
    }

    .item {
        width: 100%;
        min-height: 60px;
        box-sizing: border-box;
        padding-left: 20px;

        display: flex;
        align-items: center;
        justify-content: flex-start;
        column-gap: 10px;
    }

    .item:first-child {
        border-top-left-radius: 10px;
        border-top-right-radius: 10px;
    }

    .item:last-child {
        border-bottom-left-radius: 10px;
        border-bottom-right-radius: 10px;
    }

    .item:hover {
        cursor: pointer;
        background-color: #E1E1E1;
    }

    .item > span {
        font-size: 18px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
</style>

<script>
import clickOutside from '../../directives/click-outside';
import Checkbox from '../forms/Checkbox.vue';

export default {
    directives: {
        clickOutside: clickOutside
    },

    components: {
        Checkbox
    },

    inject: ['addError', 'addWarning', 'addInfo'],

    props: {
        title: {
            required: true
        },
        cameras: {
            type: Object,
            required: true
        },
        classes: {
            type: Object,
            required: true
        },
        chosen: {
            required: true
        }
    },

    data() {
        return {
            choosing: false,
            selected_cameras: [],
            selected_classes: [],
        }
    },

    methods: {
        checkItemIsSelected(item, selected) {
            for (let i = 0; i < selected.length; i++) {
                if (item.id === selected[i].id) {
                    return true;
                }
            }
            return false;
        },

        updateChoosing() {
            if (this.cameras.length && this.classes.length) {
                this.choosing = !this.choosing;
            } else if (!this.chosen) {
                let text = !this.cameras.length ? "камер" : "классов"; 
                this.addWarning(`Категория '${this.title}'`,
                    `В таблице ${text} нет объектов. Добавьте их для отображения статистики`
                );
            }
        },

        handleClickOutside() {
            this.choosing = false;
        },

        updateSelected(item, selected) {
            for (let i = 0; i < selected.length; i++) {
                if (item.id === selected[i].id) {
                    selected.splice(i, 1);
                    return;
                }
            }
            selected.push(item);
        },

        updateFilters() {
            if (this.selected_cameras.length || this.selected_classes.length) {
                this.$emit('update:current', {
                    'cameras': this.selected_cameras,
                    'classes': this.selected_classes
                });
            }
        }
    }
}
</script>