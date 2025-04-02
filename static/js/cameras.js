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
                    this.addError({
                        title: "Загрузка камер",
                        text: "Ошибка при загрузке"
                    });
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
                        this.sending = false;
                    })
                    .catch(e => {
                        this.addError({
                            title: "Добавление камеры",
                            text: `Ошибка при добавлении камеры`
                        }, 10000);
                        this.sending = false;
                        throw(e);
                    });
                this.closeForm();
            }
        },

        editCamera(event) {
            event.preventDefault();
            let id = this.form_data.id;
            let data = new FormData(event.target);
            let json = Object.fromEntries(data);
            json = this.processJsonData(json);
            this.form_data.address = json.address;
            if (this.validateData(json)) {
                let requestBody = JSON.stringify(json);
                this.sending = true;
                fetch(`/cameras/${id}/edit`, {
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
                        } else {
                            this.addWarning({
                                title: "Редактирование камеры",
                                text: `Камеры [${id}] не существует`
                            }, 5000);
                        }
                        this.sending = false;
                    })
                    .catch(e => {
                        this.addError({
                            title: "Редактирование камеры",
                            text: `Ошибка при редактировании камеры`
                        }, 10000);
                        this.sending = false;
                        throw(e);
                    });
                this.sending = false;
                this.closeForm();
            }
        },

        deleteCamera() {
            let id = this.form_data.id;
            this.sending = true;
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
                    } else {
                        this.addWarning({
                            title: "Удаление камеры",
                            text: `Камеры [${id}] не существует`
                        }, 5000);
                    }
                    this.sending = false;
                })
                .catch(e => {
                    this.addError({
                        title: "Удаление камеры",
                        text: `Ошибка при удалении камеры`
                    }, 10000);
                    this.sending = false;
                    throw(e);
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
                        } else {
                            this.addWarning({
                                title: "Переключение камеры",
                                text: `Камеры [${id}] не существует`
                            }, 5000);
                        }
                        this.sending = false;
                    })
                    .catch(e => {
                        this.addError({
                            title: "Переключение камеры",
                            text: `Ошибка при переключении камеры`
                        }, 10000);
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
            const ws_reinit = 3;
            this.ws_messages = new WebSocket('ws://localhost:5050/ws');
            this.ws_messages.addEventListener("open", () => {
                this.addInfo({
                    title: "Вебсокет",
                    text: "Получение сообщений с сервера работает"
                }, 5000);
                this.ws_inits_counter = 0;
            });
    
            this.ws_messages.addEventListener("message", (event) => {
                try {
                    const data = JSON.parse(event.data);
                    this.addMessage(data);
                } catch (e) {
                    this.addCamera({
                        type: "error",
                        title: "Получение сообщения",
                        text: "Ошибка при получении сообщения с сервера"
                    }, 10000);
                }                
            });
        
            this.ws_messages.addEventListener("close", () => {
                if (this.ws_inits_counter < ws_reinit) {
                    this.addWarning({
                        title: "Вебсокет",
                        text: `Соединение с вебсокетом разорвано. Переподключение ${this.ws_inits_counter+1}/${ws_reinit}`,
                    }, 5000);
                    setTimeout(() => {
                        this.initWebSocket();
                    }, 3000);
                } else {
                    this.addError({
                        title: "Вебсокет",
                        text: `Соединение с вебсокетом разорвано.`,
                    });
                }
            });
        
            this.ws_messages.addEventListener("error", (error) => {
                console.error('WebSocket error:', error);
                this.ws_inits_counter++;
            });
        },

        addError(data, delay) {
            this.addMessage(data, "error", delay)
        },

        addWarning(data, delay) {
            this.addMessage(data, "warning", delay)
        },

        addInfo(data, delay) {
            this.addMessage(data, "info", delay)
        },

        addMessage(message, type, delay) {
            message.id = this.ws_id++;
            if (type != undefined) {
                message.type = type;
            }
            this.system_errors.push(message);
            if (delay != undefined) {
                setTimeout(() => {
                    this.deleteMessage(message.id);
                }, delay);
            }
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
