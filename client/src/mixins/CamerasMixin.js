import axios from 'axios';

export default {
    inject: ['addError', 'addWarning', 'addInfo'],

    data() {
        return {
            loading: false,
            cameras: null,
        }
    },

    methods: {
        async loadCameras() {
            try {
                this.loading = true;
                const response = await axios.get(
                    "http://localhost:5050/cameras"
                );
                this.cameras = response.data;
            } catch (error) {
                this.addError("Загрузка камер", `Получена ошибка: ${error}`);
                throw(error);
            } finally {
                this.loading = false;
            }
        },
    }
}