<template>
    <div v-click-outside="handleClickOutside"
        class="selector-header"
        :class="{ 'chosen': chosen }">

        <div class="title-wrapper" @click="updateChoosing">
            <span class="title">{{ chosen ? currentItem.name : title }}</span>
        </div>

        <div v-if="choosing" class="items-wrapper">
            <div class="items">
                <div v-for="item in items"
                    :key="item.id"
                    @click="updateCurrentItem(item)"
                    class="item">
                    <span>{{ item.name }}</span>
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

.hidden span {
    display: none;
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

.items {
    width: 100%;
    max-height: 500px;
    
    display: flex;
    flex-direction: column;
    overflow-y: auto;

    position: absolute;

    border-radius: 10px;
    background-color: white;
    outline: 1px solid black;
}

.item {
    width: 100%;
    min-height: 60px;

    display: flex;
    align-items: center;
    justify-content: center;
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

.item>span {
    font-size: 18px;
}
</style>

<script>
import clickOutside from '/src/directives/click-outside';

export default {
    directives: {
        clickOutside: clickOutside
    },

    props: {
        title: {
            required: true
        },
        items: {
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
            currentItem: null
        }
    },

    methods: {
        updateChoosing() {
            if (this.items.length) {
                this.choosing = !this.choosing;
            }
        },

        handleClickOutside() {
            this.choosing = false;
        },

        updateCurrentItem(newItem) {
            this.currentItem = newItem;
            this.$emit('update:current', newItem.id);
            this.choosing = false;
        }
    }
}
</script>