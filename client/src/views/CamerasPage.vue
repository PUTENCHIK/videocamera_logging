<template>
    <h1>Отслеживаемые камеры</h1>

    <div class="row-right-container">
        <button @click="showAddCameraForm"
                class="primary"
                :disabled="loading || sending">
            <span>Добавить видеокамеру</span>
        </button>
    </div>

    <div v-if="cameras.length && !loading" class="table-display">
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
                <div @click="switchCameraMonitoring(camera.id)" class="switch"
                    :class="{ 'on': camera.is_monitoring, 'disabled': sending }"></div>
            </div>
            <div>{{ camera.created_at }}</div>
            <div class="icons-box">
                <img @click="showEditCameraForm(camera.id)"
                    class="icon-button"
                    :class="{ 'disabled': sending }"
                    src="../assets/icons/edit.png"
                    alt="edit">
                <img @click="showDeleteCameraForm(camera.id)"
                    class="icon-button"
                    :class="{ 'disabled': sending }"
                    src="../assets/icons/delete.png"
                    alt="delete">
            </div>
        </div>
    </div>
    <p v-else-if="!loading">В базе нет ещё ни одной камеры.</p>
    <div v-else class="loader-wrapper">
        <span class="loader"></span>
    </div>

    <FormsContainer v-if="current_form">
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
                :entity="entity"
                :onClose="closeForm"
                :onDelete="deleteCamera"/>
        </template>
    </FormsContainer>
</template>

<style scoped>
@import url('../assets/styles/tables.css');
@import url('../assets/styles/windows.css');
@import url('../assets/styles/loader.css');
@import url('../assets/styles/messages.css');
</style>

<script>
import axios from 'axios';
import { formatDate, cloneObject } from '/src/utils/helpers';
import FormsContainer from '/src/components/forms/FormsContainer.vue';
import CameraForm from '/src/components/forms/CameraForm.vue';
import DeleteForm from '/src/components/forms/DeleteForm.vue';

export default {
    components: {
        FormsContainer, CameraForm, DeleteForm
    },

    data() {
        return {
            loading: false,
            sending: false,
            cameras: [],
            current_form: null,
            form_data: {},
            entity: "камеру"
        }
    },

    methods: {
        async loadCameras() {
            try {
                this.loading = true;
                const response = await axios.get(
                    "http://localhost:5050/api/cameras"
                );
                this.cameras = response.data;
                this.formatDates();
            } catch (error) {
                throw(error);
            } finally {
                this.loading = false;
            }
        },

        async addCamera() {
            try {
                let data = cloneObject(this.form_data);
                this.closeForm();
                this.sending = true;
                const response = await axios.post(
                    "http://localhost:5050/cameras/add",
                    data
                );
                this.cameras.push(response.data);
                this.formatDates();
            } catch (error) {
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
                    `http://localhost:5050/cameras/${data.id}/edit`,
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
                }
            } catch (error) {
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
                    `http://localhost:5050/cameras/${id}/delete`
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
                }
            } catch (error) {
                throw(error);
            } finally {
                this.sending = false;
            }
        },

        async switchCameraMonitoring(id) {
            try {
                this.sending = true;
                const response = await axios.patch(
                    `http://localhost:5050/cameras/${id}/switch`
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
                }
            } catch (error) {
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

        showEditCameraForm(id) {
            if (!this.sending) {
                this.current_form = 'edit';
                this.cameras.forEach((camera) => {
                    if (camera.id === id) {
                        this.form_data = cloneObject(camera);
                    }
                });
            }
        },

        showDeleteCameraForm(id) {
            if (!this.sending) {
                this.current_form = 'delete';
                this.cameras.forEach((camera) => {
                    if (camera.id === id) {
                        this.form_data = cloneObject(camera);
                    }
                });
            }
        },

        closeForm() {
            this.current_form = null;
            this.form_data = {};
        },

        updateFormData(newData) {
            this.form_data = newData;
        }
    },

    mounted() {
        this.loadCameras();
    },
};
</script>