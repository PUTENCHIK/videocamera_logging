<template>
    <h1>Классы модели</h1>

    <div class="row-right-container">
        <button @click="showAddClassForm"
                class="primary"
                :disabled="loading || sending">
            <span>Добавить класс</span>
        </button>
    </div>

    <div v-if="loading" class="loader-wrapper">
        <span class="loader"></span>
    </div>
    <p v-else-if="classes == null">Не удалось загрузить классы.</p>
    <div v-else-if="classes.length" class="table-display">
        <div class="table-row">
            <div class="label-bold">id</div>
            <div class="label-bold">системное имя</div>
            <div class="label-bold">метка</div>
            <div class="label-bold">название</div>
            <div class="label-bold">цвет</div>
            <div class="label-bold">добавлен</div>
        </div>
        
        <div v-for="class_ in classes" class="table-row" :key="class_.id">
            <div>{{ class_.id }}</div>
            <div>{{ class_.name }}</div>
            <div>{{ class_.label }}</div>
            <div>{{ class_.title }}</div>
            <div class="row-cell">
                <div class="color-box" :style="{'background-color': class_.color}"></div>
                {{ class_.color }}
            </div>
            <div>{{ class_.created_at }}</div>
            <div class="icons-box">
                <img @click="showEditClassForm(class_.id)"
                    class="icon-button"
                    :class="{ 'disabled' : sending }"
                    src="../assets/icons/edit.png"
                    alt="edit">
                <img @click="showDeleteClassForm(class_.id)"
                    class="icon-button"
                    :class="{ 'disabled' : sending }"
                    src="../assets/icons/delete.png"
                    alt="delete">
            </div>
        </div>
    </div>
    <p v-else="!classes.length">В базе нет ещё ни одного класса.</p>

    <FormsContainer v-if="current_form" :onClose="closeForm">
        <template #form>
            <ClassForm
                v-if="current_form == 'add'"
                :type="current_form"
                :data="form_data"
                :classes="classes"
                :onClose="closeForm"
                :onSubmit="addClass"
                @update:data="updateFormData" />
            <ClassForm
                v-else-if="current_form == 'edit'"
                :type="current_form"
                :data="form_data"
                :classes="classes"
                :onClose="closeForm"
                :onSubmit="editClass"
                @update:data="updateFormData" />
            <DeleteForm
                v-else
                :id="form_data.id"
                :entity="'класс'"
                :onClose="closeForm"
                :onDelete="deleteClass"/>
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
import { formatDate, cloneObject, colorToHex } from '/src/utils/helpers';
import ClassesMixin from '/src/utils/ClassesMixin';
import FormsContainer from '/src/components/forms/FormsContainer.vue';
import ClassForm from '/src/components/forms/ClassForm.vue';
import DeleteForm from '/src/components/forms/DeleteForm.vue';

export default {
    inject: ['addError', 'addWarning', 'addInfo'],

    mixins: [ClassesMixin],

    components: {
        FormsContainer, ClassForm, DeleteForm
    },
    
    data() {
        return {
            sending: false,
            current_form: null,
            form_data: {}
        }
    },

    methods: {
        async addClass() {
            try {
                let data = cloneObject(this.form_data);
                this.closeForm();
                this.sending = true;
                const response = await axios.post(
                    "http://localhost:5050/classes/add",
                    data
                );
                this.classes.push(response.data);
                this.formatClassesData();
            } catch (error) {
                this.addError("Добавление класса", `Получена ошибка: ${error}`);
                throw(error);
            } finally {
                this.sending = false;
            }
        },

        async editClass() {
            try {
                let data = cloneObject(this.form_data);
                this.closeForm();
                this.sending = true;
                const response = await axios.patch(
                    `http://localhost:5050/classes/${data.id}/edit`,
                    data
                );
                let result = response.data;                
                if (result.success) {
                    let class_ = result.class_;
                    for (let i = 0; i < this.classes.length; i++) {
                        if (this.classes[i].id == class_.id) {
                            this.classes[i] = class_;
                            this.formatClassesData();
                            break;
                        }
                    }
                }
            } catch (error) {
                this.addError("Редактирование класса", `Получена ошибка: ${error}`);
                throw(error);
            } finally {
                this.sending = false;
            }
        },

        async deleteClass() {
            try {
                let id = this.form_data.id;
                this.closeForm();
                this.sending = true;
                const response = await axios.delete(
                    `http://localhost:5050/classes/${id}/delete`
                );
                let result = response.data;
                if (result.success) {
                    let index;                        
                    for (let i = 0; i < this.classes.length; i++) {
                        if (this.classes[i].id === id) {
                            index = i;
                            break;
                        }
                    }                        
                    if (index != undefined) {
                        this.classes.splice(index, 1);
                    }
                }
            } catch (error) {
                this.addError("Удаление класса", `Получена ошибка: ${error}`);
                throw(error);
            } finally {
                this.sending = false;
            }
        },

        formatClassesData() {
            this.classes.forEach((class_) => {
                class_.created_at = formatDate(class_.created_at);
                if (typeof(class_.color) !== "string") {
                    class_.color = colorToHex(class_.color);
                }
            });
        },

        showAddClassForm() {
            this.current_form = 'add';
        },

        showEditClassForm(id) {
            if (!this.sending) {
                this.current_form = 'edit';
                this.classes.forEach((class_) => {
                    if (class_.id === id) {
                        this.form_data = cloneObject(class_);
                    }
                });
            }
        },

        showDeleteClassForm(id) {
            if (!this.sending) {
                this.current_form = 'delete';
                this.classes.forEach((class_) => {
                    if (class_.id === id) {
                        this.form_data = cloneObject(class_);
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

    async mounted() {
        await this.loadClasses();
        if (this.classes != null) {
            this.formatClassesData();
        }
    }
}
</script>