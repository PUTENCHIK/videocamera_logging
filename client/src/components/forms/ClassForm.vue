<template>
    <div class="add-edit-window">
        <div class="row-right-container">
            <div @click="handleButtonClose" class="button-cross"></div>
        </div>
        <div class="window__content">
            <h2 v-if="type == 'add'">Добавление нового класса в БД</h2>
            <h2 v-else>Изменение класса #{{ data.id }}</h2>
            <form @submit="(event) => handleFormSubmit(event)">
                <div class="form-inputs">
                    <label class="filled" :class="{ 'error' : errors.name }">
                        <span class="label-bold">системное имя:</span>
                        <input
                            :value="data.name"
                            type="text" name="name" maxlength="100"
                            placeholder="human">
                        <span v-if="errors.name" class="error-text">{{ errors.name }}</span>
                    </label>
                    <label class="filled" :class="{ 'error' : errors.label }">
                        <span class="label-bold">метка:</span>
                        <input
                            :value="data.label"
                            type="number" name="label"
                            placeholder="целое неотрицательное число">
                        <span v-if="errors.label" class="error-text">{{ errors.label }}</span>
                    </label>
                    <label class="filled" :class="{ 'error' : errors.title }">
                        <span class="label-bold">название:</span>
                        <input
                            :value="data.title"
                            type="text" name="title" maxlength="100"
                            placeholder="понятное вам описание">
                        <span v-if="errors.title" class="error-text">{{ errors.title }}</span>
                    </label>
                    <label class="filled color" :class="{ 'error' : errors.color }">
                        <div>
                            <span class="label-bold">цвет для отображения:</span>
                            <input
                                :value="data.color"
                                type="color" name="color">
                        </div>
                        <span v-if="errors.color" class="error-text">{{ errors.color }}</span>
                    </label>
                </div>
                <button type="submit" class="primary submit-form">
                    <span v-if="type == 'add'">Добавить класс</span>
                    <span v-else>Сохранить</span>
                </button>
            </form>
        </div>
    </div>
</template>

<style scoped>
    @import url('../../assets/styles/windows.css');
</style>

<script>
import { getFormData } from '/src/utils/helpers';

export default {
    props: {
        type: {
            required: true
        },
        data: {
            type: Object,
            required: true
        },
        classes: {
            type: Object,
            required: true
        },
        onClose: {
            type: Function,
            required: true
        },
        onSubmit: {
            type: Function,
            required: true
        }
    },

    data() {
        return {
            errors: {}
        }
    },

    methods: {
        handleButtonClose() {
            if (this.onClose) {
                this.onClose();
            }
        },

        handleFormSubmit(event) {
            event.preventDefault();
            let id = this.data.id;
            let data = this.processFormData(getFormData(event));
            data.id = id;
            this.$emit('update:data', data);
            if (this.validateClassData(data)) {
                if (this.onSubmit) {
                    this.onSubmit();
                } else {
                    console.error("onSubmit not implemented");
                }
            }          
        },

        processFormData(data) {
            data.name = data.name.trim();
            data.title = data.title.trim();
            return data;
        },

        validateClassData(data) {
            this.errors = {};
            if (data.name.length === 0) {
                this.errors['name'] = "Имя должно быть заполнено";
            }

            if (data.label.length === 0) {
                this.errors['label'] = "Метка должна быть указана";
            } else if (isNaN(Number(data.label)) || Number(data.label) < 0) {
                this.errors['label'] = "Метка должна быть целым неотрицательным числом";
            }

            if (data.title.length === 0) {
                this.errors['title'] = "Название должно быть заполнено";
            }

            this.classes.forEach((class_) => {      
                if ((class_.id !== data.id)) {
                    if (class_.name === data.name) {
                        this.errors['name'] = "Такое имя уже существует!";
                    }
                    if (data.label.length && Number(class_.label) === Number(data.label)) {
                        this.errors['label'] = "Такая метка уже существует!";
                    }
                }
            });

            return !Object.keys(this.errors).length;
        }
    }
}
</script>