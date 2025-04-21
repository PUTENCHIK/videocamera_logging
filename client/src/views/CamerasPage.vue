<template>
    <h1>Отслеживаемые камеры</h1>

    <div v-if="!loading && cameras != null" class="row-right-container">
        <button @click="showAddCameraForm"
                class="primary"
                :disabled="loading || sending">
            <span>Добавить видеокамеру</span>
        </button>
    </div>

    <div v-if="loading" class="loader-wrapper">
        <span class="loader"></span>
    </div>
    <p v-else-if="cameras == null">Не удалось загрузить камеры.</p>
    <div v-else-if="cameras.length" class="table-display">
        <div class="table-row">
            <div class="label-bold">id</div>
            <div class="label-bold">Адрес</div>
            <div class="label-bold">Отслеживать</div>
            <div class="label-bold">Добавлена</div>
        </div>

        <div v-for="camera in cameras" class="table-row" :key="camera.id">
            <div>{{ camera.id }}</div>
            <div>{{ camera.address }}</div>
            <div>
                <div @click="switchCameraMonitoring(camera.id)"
                    class="switch"
                    :class="{ 'on': camera.is_monitoring, 'disabled': sending }"></div>
            </div>
            <div>{{ camera.created_at }}</div>
            <div class="icons-box">
                <img @click="!sending ? showEditCameraForm(camera) : null"
                    class="icon-button"
                    :class="{ 'disabled': sending || camera.is_monitoring }"
                    src="../assets/icons/edit.png"
                    alt="edit">
                <img @click="!sending ? showDeleteCameraForm(camera) : null"
                    class="icon-button"
                    :class="{ 'disabled': sending }"
                    src="../assets/icons/delete.png"
                    alt="delete">
            </div>
        </div>
    </div>
    <p v-else="!cameras.length">В базе нет ещё ни одной камеры.</p>

    <FormsContainer v-if="current_form" :onClose="closeForm">
        <template #form>
            <CameraForm 
                v-if="current_form == 'add'"
                :type="current_form"
                :data="form_data"
                :onClose="closeForm"
                :onSubmit="addCamera"
                @update:data="updateFormData" />
            <CameraForm
                v-else-if="current_form == 'edit'"
                :type="current_form"
                :data="form_data"
                :onClose="closeForm"
                :onSubmit="editCamera"
                @update:data="updateFormData" />
            <DeleteForm
                v-else
                :id="form_data.id"
                :entity="'камеру'"
                :onClose="closeForm"
                :onDelete="deleteCamera"/>
        </template>
    </FormsContainer>
</template>

<style scoped>
@import url('../assets/styles/tables.css');
@import url('../assets/styles/windows.css');
@import url('../assets/styles/loader.css');
</style>

<script>
import axios from 'axios';
import { formatDate, cloneObject } from '../utils/helpers';
import CamerasMixin from '../mixins/CamerasMixin';
import FormsContainer from '../components/forms/FormsContainer.vue';
import CameraForm from '../components/forms/CameraForm.vue';
import DeleteForm from '../components/forms/DeleteForm.vue';

export default {
    inject: ['addError', 'addWarning', 'addInfo', 'deleteAllMessages', 'API_PORT'],

    mixins: [CamerasMixin],

    components: {
        FormsContainer, CameraForm, DeleteForm
    },

    data() {
        return {
            sending: false,
            current_form: null,
            form_data: {}
        }
    },

    methods: {
        async addCamera() {
            try {
                let data = cloneObject(this.form_data);
                this.closeForm();
                this.sending = true;
                const response = await axios.post(
                    `http://localhost:${this.API_PORT}/cameras/add`,
                    data
                );
                this.cameras.push(response.data);
                this.formatDates();
            } catch (error) {
                this.addError("Добавление камеры", `Получена ошибка: ${error}`);
                throw(error);
            } finally {
                this.sending = false;
            }
        },

        async editCamera() { 
            try {
                let data = cloneObject(this.form_data);
                this.closeForm();
                this.sending = true;
                const response = await axios.patch(
                    `http://localhost:${this.API_PORT}/cameras/${data.id}/edit`,
                    data
                );
                let result = response.data;
                if (result.success) {
                    let camera = result.camera;
                    for (let i = 0; i < this.cameras.length; i++) {
                        if (this.cameras[i].id == camera.id) {
                            this.cameras[i] = camera;
                            this.formatDates();
                            break;
                        }
                    }
                } else {
                    if (result.error) {
                        this.addError("Редактирование камеры", result.error);
                    }
                }
            } catch (error) {
                this.addError("Редактирование камеры", `Получена ошибка: ${error}`);
                throw(error);
            } finally {
                this.sending = false;
            }
        },

        async deleteCamera() {
            try {
                let id = this.form_data.id;
                this.closeForm();
                this.sending = true;
                const response = await axios.delete(
                    `http://localhost:${this.API_PORT}/cameras/${id}/delete`
                );
                let result = response.data;                
                if (result.success) {
                    let index;                        
                    for (let i = 0; i < this.cameras.length; i++) {
                        if (this.cameras[i].id === id) {
                            index = i;
                            break;
                        }
                    }                        
                    if (index != undefined) {
                        this.cameras.splice(index, 1);
                    }
                } else {
                    if (result.error) {
                        this.addError("Удаление камеры", result.error);
                    }
                }
            } catch (error) {
                this.addError("Удаление камеры", `Получена ошибка: ${error}`);
                throw(error);
            } finally {
                this.sending = false;
            }
        },

        async switchCameraMonitoring(id) {
            try {
                this.sending = true;
                const response = await axios.patch(
                    `http://localhost:${this.API_PORT}/cameras/${id}/switch`
                );
                let result = response.data;
                if (result.success) {
                    let camera = result.camera;
                    for (let i = 0; i < this.cameras.length; i++) {
                        if (this.cameras[i].id == camera.id) {
                            this.cameras[i] = camera;
                            this.formatDates();
                            break;
                        }
                    }
                } else {
                    if (result.error) {
                        this.addError("Переключение камеры", result.error);
                    }
                }
            } catch (error) {
                this.addError("Переключение камеры", `Получена ошибка: ${error}`);
                throw(error);
            } finally {
                this.sending = false;
            }
        },

        formatDates() {
            this.cameras.forEach((camera) => {
                camera.created_at = formatDate(camera.created_at);
            });
        },

        showAddCameraForm() {
            this.current_form = 'add';
        },

        showEditCameraForm(camera) {
            if (!camera.is_monitoring) {
                this.current_form = 'edit';
                this.form_data = cloneObject(camera);
            } else {
                this.addWarning(
                    "Редактирование камеры",
                    "Нельзя изменить камеру, пока она отслеживается"
                );
            }
        },

        showDeleteCameraForm(camera) {
            this.current_form = 'delete';
            this.form_data = cloneObject(camera);
        },

        closeForm() {
            this.current_form = null;
            this.form_data = {};
        },

        updateFormData(newData) {
            this.form_data = newData;
        }
    },

    async mounted() {
        this.deleteAllMessages();
        await this.loadCameras();
        if (this.cameras != null) {
            this.formatDates();
        }
    },
};
</script>