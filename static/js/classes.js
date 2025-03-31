const { createApp } = Vue;

createApp({
    delimiters: ['[[', ']]'],

    data() {
        return {
            classes: [],
            loading: false,
            sending: false,
            current_form: null,
            errors: {},
            form_data: {}
        }
    },

    methods: {
        showAddClassForm() {
            this.current_form = 'add';
            let max_label = -1;
            this.classes.forEach((class_) => {
                if (class_.label > max_label) {
                    max_label = class_.label;
                }
            });
            this.form_data.label = max_label+1;
        },

        showEditClassForm(id) {
            if (!this.sending) {
                this.current_form = 'edit';
                this.classes.forEach((class_) => {
                    if (class_.id === id) {
                        this.form_data = clone_object(class_);
                    }
                });
            }
        },

        showDeleteClassForm(id) {
            if (!this.sending) {
                this.current_form = 'delete';
                this.classes.forEach((class_) => {
                    if (class_.id === id) {
                        this.form_data = clone_object(class_);
                    }
                });
            }
        },

        closeForm() {
            this.current_form = null;
            this.errors = {};
            this.form_data = {};
        },

        formsContainerClicked(event) {
            if (event.target.className === "forms-container") {
                this.closeForm();
            }
        },

        loadClasses() {
            this.loading = true;
            fetch("/api/classes", {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                }
            })
                .then(r => r.json())
                .then((r) => {
                    this.classes = r;
                    this.formatClassesData();
                    this.loading = false;
                })
                .catch(e => {
                    loading = false;
                    throw(e);
                });
        },

        addClass(event) {
            event.preventDefault();
            let data = new FormData(event.target);
            let json = Object.fromEntries(data);
            json = this.processJsonData(json);
            this.form_data = clone_object(json);
            if (this.validateData(json)) {
                let requestBody = JSON.stringify(json);
                this.sending = true;
                fetch("/classes/add", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: requestBody
                })
                    .then(r => r.json())
                    .then((r) => {                        
                        this.classes.push(r);
                        this.formatClassesData();
                    });
                this.sending = false;
                this.closeForm();
            }
        },

        editClass(event) {
            event.preventDefault();
            let data = new FormData(event.target);
            let json = Object.fromEntries(data);
            json = this.processJsonData(json);
            let id = this.form_data.id;
            this.form_data = clone_object(json);
            this.form_data.id = id;
            if (this.validateData(json)) {
                let requestBody = JSON.stringify(json);
                this.sending = true;
                fetch(`/classes/${id}/edit`, {
                    method: "PATCH",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: requestBody
                })
                    .then(r => r.json())
                    .then((r) => {
                        if (r.success) {
                            let class_ = r.class_;
                            for (let i = 0; i < this.classes.length; i++) {
                                if (this.classes[i].id == class_.id) {
                                    this.classes[i] = class_;
                                    this.formatClassesData();
                                    break;
                                }
                            }
                        }
                    });
                this.sending = false;
                this.closeForm();
            }
        },

        deleteClass() {
            this.sending = true;
            let id = this.form_data.id;
            fetch(`/classes/${id}/delete`, {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json"
                }
            })
                .then(r => r.json())
                .then((r) => {
                    if (r.success) {
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
                });
            this.sending = false;
            this.closeForm();
        },

        validateData(json) {
            this.errors = {};
            if (json.name.length === 0) {
                this.errors['name'] = "Имя должно быть заполнено";
            }

            if (json.label.length === 0) {
                this.errors['label'] = "Метка должна быть указана";
            } else if (isNaN(Number(json.label)) || Number(json.label) < 0) {
                this.errors['label'] = "Метка должна быть целым неотрицательным числом";
            }

            if (json.title.length === 0) {
                this.errors['title'] = "Название должно быть заполнено";
            }

            this.classes.forEach((class_) => {      
                if ((class_.id !== this.form_data.id)) {
                    if (class_.name === json.name) {
                        this.errors['name'] = "Такое имя уже существует!";
                    }
                    if (json.label.length && Number(class_.label) === Number(json.label)) {
                        this.errors['label'] = "Такая метка уже существует!";
                    }
                }
            });

            return !Object.keys(this.errors).length;
        },

        formatClassesData() {
            this.classes.forEach((class_) => {
                class_.created_at = formatDate(class_.created_at);
                if (typeof(class_.color) !== "string") {
                    class_.color = get_color(class_.color);
                }
            });
        },

        processJsonData(json) {
            json.name = json.name.trim();
            json.title = json.title.trim();
            return json;
        },
    },

    mounted() {
        this.loadClasses();
    }

}).mount("#app");