import axios from 'axios';

export default {
    inject: ['addError', 'addWarning', 'addInfo', 'API_PORT'],

    data() {
        return {
            loading: false,
            classes: null,
        }
    },

    methods: {
        async loadClasses() {
            try {
                this.loading = true;
                const response = await axios.get(
                    `http://localhost:${this.API_PORT}/classes`
                );
                this.classes = response.data;
            } catch (error) {
                this.addError("Загрузка классов", `Получена ошибка: ${error}`);
                throw(error);
            } finally {
                this.loading = false;
            }
        },
    }
}