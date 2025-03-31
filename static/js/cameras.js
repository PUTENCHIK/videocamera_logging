const { createApp } = Vue;
import Message from "./Message.js";

createApp({
    delimiters: ['[[', ']]'],

    components: {
        'message': Message,
    },

    data() {
        return {
            current_form: null,
            cameras: [],
            loading: false,
            sending: false,
            form_errors: {},
            form_data: {},
            system_errors: [],
            ws_messages: null,
            ws_inits_counter: 0,
            ws_id: 1
        }
    },

    methods: {
        showAddCameraForm() {
            this.current_form = 'add';
        },

        showEditCameraForm(id) {
            if (!this.sending) {
                this.current_form = 'edit';
                this.cameras.forEach((camera) => {
                    if (camera.id === id) {
                        this.form_data = clone_object(camera);
                    }
                });
            }
        },

        showDeleteCameraForm(id) {
            if (!this.sending) {
                this.current_form = 'delete';
                this.cameras.forEach((camera) => {
                    if (camera.id === id) {
                        this.form_data = clone_object(camera);
                    }
                });
            }
        },

        closeForm() {
            this.current_form = null;
            this.form_errors = {};
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
                    this.formatDates();
                    this.loading = false;
                })
                .catch((e) => {
                    this.loading = false;
                    throw(e);
                });
        },

        addCamera(event) {
            event.preventDefault();
            let data = new FormData(event.target);
            let json = Object.fromEntries(data);
            json = this.processJsonData(json);
            this.form_data.address = json.address;
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
                        this.formatDates();
                    });
                this.sending = false;
                this.closeForm();
            }
        },

        editCamera(event) {
            event.preventDefault();
            let data = new FormData(event.target);
            let json = Object.fromEntries(data);
            json = this.processJsonData(json);
            this.form_data.address = json.address;
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
                                    this.formatDates();
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

        switchCameraMonitoring(id) {            
            if (!this.sending) {
                this.sending = true;
                fetch(`/cameras/${id}/switch`, {
                    method: "PATCH",
                    headers: {
                        "Content-Type": "application/json"
                    }
                })
                    .then(r => r.json())
                    .then((r) => {
                        if (r.success) {
                            let camera = r.camera;
                            for (let i = 0; i < this.cameras.length; i++) {
                                if (this.cameras[i].id == camera.id) {
                                    this.cameras[i] = camera;
                                    this.formatDates();
                                    break;
                                }
                            }
                            this.sending = false;
                        }
                    })
                    .catch(e => {
                        this.sending = false;
                        throw(e);
                    });
            }
        },

        validateData(json) {
            if (json.address.length === 0) {
                this.form_errors['address'] = "Адрес не может быть пустым";
                return false;
            } else if (/^rtsp:\/\//.exec(json.address) == null) {
                this.form_errors['address'] = "Адрес не валиден RTSP протоколу";
                return false;
            }
            return true;
        },

        formatDates() {
            this.cameras.forEach((camera) => {
                camera.created_at = formatDate(camera.created_at);
            });
        },

        formsContainerClicked(event) {
            if (event.target.className === "forms-container") {
                this.closeForm();
            }
        },

        processJsonData(json) {
            json.address = json.address.trim();
            return json;
        },

        initWebSocket() {
            this.ws_messages = new WebSocket('ws://localhost:5050/ws');
            this.ws_messages.addEventListener("open", () => {
                console.log("WebSocket opened");            
                this.ws_inits_counter = 0;
            });
    
            this.ws_messages.addEventListener("message", (event) => {
                try {
                    const data = JSON.parse(event.data);
                    this.addMessage(data);
                } catch (e) {
                    console.log(event.data);
                    throw(e);
                }                
            });
        
            this.ws_messages.addEventListener("close", () => {
                console.log('WebSocket disconnected');
                if (this.ws_inits_counter < 3) {
                    setTimeout(() => {
                        this.initWebSocket();
                    }, 3000);
                }
            });
        
            this.ws_messages.addEventListener("error", (error) => {
                console.error('WebSocket error:', error);
                this.ws_inits_counter++;
            });
        },

        addMessage(message) {
            message.id = this.ws_id++;
            this.system_errors.push(message);
            setTimeout(() => {
                this.deleteMessage(message.id);
            }, 5000);
        },

        deleteMessage(id) {
            let index;
            for (let i = 0; i < this.system_errors.length; i++) {
                let error = this.system_errors[i];
                if (error.id === id) {
                    index = i;
                    break;
                }
            };
            if (index != undefined) {
                this.system_errors.splice(index, 1);
                console.log(`Message ${id} has been deleted`);
                
            }
        },
    },

    mounted() {
        this.loadCameras();
        this.initWebSocket();
    },

    unmounted() {
        if (this.ws_messages) {
            this.ws_messages.close();
        }
    }

}).mount("#app");
