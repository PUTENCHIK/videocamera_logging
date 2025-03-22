const { createApp } = Vue;

createApp({
    delimiters: ['[[', ']]'],

    data() {
        return {
            current_form: null,
            cameras: [],
            loading: false,
            sending: false,
            errors: {},
            form_data: {},
        }
    },

    methods: {
        showAddCameraForm() {
            this.current_form = 'add';
        },

        showEditCameraForm(id) {
            this.current_form = 'edit';
            this.cameras.forEach((camera) => {
                if (camera.id === id) {
                    this.form_data = camera;
                }
            });
        },

        showDeleteCameraForm(id) {
            this.current_form = 'delete';
            this.cameras.forEach((camera) => {
                if (camera.id === id) {
                    this.form_data = camera;
                }
            });
        },

        closeForm() {
            this.current_form = null;
            this.errors = {};
            this.form_data = {};
        },

        loadCameras() {
            this.loading = true;
            fetch("/api/cameras", {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                }
            })
                .then(r => r.json())
                .then((r) => {
                    this.cameras = r;
                    this.loading = false;
                });
        },

        addCamera(event) {
            event.preventDefault();
            let data = new FormData(event.target);
            let json = Object.fromEntries(data);
            if (this.validateData(json)) {
                let requestBody = JSON.stringify(json);
                this.sending = true;
                fetch("/cameras/add", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: requestBody
                })
                    .then(r => r.json())
                    .then((r) => {
                        this.cameras.push(r);
                    });
                this.sending = false;
                this.closeForm();
            }
        },

        editCamera(event) {
            event.preventDefault();
            let data = new FormData(event.target);
            let json = Object.fromEntries(data);
            if (this.validateData(json)) {
                let requestBody = JSON.stringify(json);
                this.sending = true;
                fetch(`/cameras/${this.form_data.id}/edit`, {
                    method: "PATCH",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: requestBody
                })
                    .then(r => r.json())
                    .then((r) => {
                        if (r.success) {
                            let camera = r.camera;
                            for (let i = 0; i < this.cameras.length; i++) {
                                if (this.cameras[i].id == camera.id) {
                                    this.cameras[i] = camera;
                                    break;
                                }
                            }
                        }
                    });
                this.sending = false;
                this.closeForm();
            }
        },

        deleteCamera() {
            this.sending = true;
            let id = this.form_data.id;
            fetch(`/cameras/${id}/delete`, {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json"
                }
            })
                .then(r => r.json())
                .then((r) => {
                    if (r.success) {
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
                });
            this.sending = false;
            this.closeForm();
        },

        validateData(json) {
            if (json.address.length === 0) {
                this.errors['address'] = "Адрес не может быть пустым";
                return false;
            } else if (/^rtsp:\/\//.exec(json.address) == null) {
                this.errors['address'] = "Адрес не валиден RTSP протоколу";
                return false;
            }
            return true;
        }
    },

    mounted() {
        this.loadCameras();
    }

}).mount("#app");
