import axios from 'axios';

export default {
    inject: ['addError', 'addWarning', 'addInfo'],

    data() {
        return {
            loading: false,
            snapshots: null,
            objects: null
        }
    },

    methods: {
        async loadSnapshots() {
            try {
                this.loading = true;
                const response = await axios.get(
                    "http://localhost:5050/snapshots"
                );
                this.snapshots = response.data;
            } catch (error) {
                this.addError("Загрузка снимков", `Получена ошибка: ${error}`);
                throw(error);
            } finally {
                this.loading = false;
            }
        },

        async loadObjects() {
            try {
                this.loading = true;
                const response = await axios.get(
                    "http://localhost:5050/snapshots/objects"
                );
                this.objects = response.data;
            } catch (error) {
                this.addError("Загрузка объектов со снимков", `Получена ошибка: ${error}`);
                throw(error);
            } finally {
                this.loading = false;
            }
        },
    }
}