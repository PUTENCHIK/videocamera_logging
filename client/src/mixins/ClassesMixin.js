import axios from 'axios';

export default {
    inject: ['addError', 'addWarning', 'addInfo'],

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
                    "http://localhost:5050/classes"
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