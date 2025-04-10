import axios from 'axios';

export default {
    inject: ['addError', 'addWarning', 'addInfo', 'API_PORT'],

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
                    `http://localhost:${this.API_PORT}/cameras`
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