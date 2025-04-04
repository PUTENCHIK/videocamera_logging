<template>
    <div class="window add-edit-window">
        <div class="row-right-container">
            <div @click="handleButtonClose" class="button-cross"></div>
        </div>
        <div class="window__content">
            <h2 v-if="type == 'add'">Добавление новой видеокамеры в БД</h2>
            <h2 v-else>Изменение видеокамеры #{{ data.id }}</h2>
            <form @submit="(event) => handleFormSubmit(event)" name="form">
                <div class="form-inputs">
                    <label class="filled" :class="{ 'error' : errors.address }">
                        <span class="label-bold">адрес:</span>
                        <input
                            :value="data.address"
                            type="text" name="address" maxlength="100"
                            placeholder="rtsp://{ip}:{port}/{thread}">
                        <span v-if="errors.address" class="error-text">{{ errors.address }}</span>
                    </label>
                </div>
                <button type="submit" class="primary submit-form">
                    <span v-if="type === 'add'">Добавить видеокамеру</span>
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
            let data = getFormData(event);
            data.address = data.address.trim();
            data.id = id;
            this.$emit('update:data', data);
            if (this.validateCameraData(data)) {
                if (this.onSubmit) {
                    this.onSubmit();
                } else {
                    console.error("onSubmit not implemented");
                }
            }
        },

        validateCameraData(data) {
            this.error = {};
            if (data.address.length === 0) {
                this.errors['address'] = "Адрес не может быть пустым";
                return false;
            } else if (/^rtsp:\/\//.exec(data.address) == null) {
                this.errors['address'] = "Адрес не валиден RTSP протоколу";
                return false;
            }
            return true;
        }
    }
}
</script>