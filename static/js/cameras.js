// window.addEventListener("DOMContentLoaded", () => {

//     function getLabelOfInput(input) {
//         let label = input.parentElement;
//         if (input.getAttribute("name") === "password") {
//             label = label.parentElement;
//         }
//         return label;
//     }

//     function setFormError(name, value) {
//         let input = document.getElementsByName(name)[0];
//         let label = getLabelOfInput(input);
//         label.classList.add("error");

//         let errorText = label.getElementsByClassName("error-text");
//         if (!errorText.length) {
//             errorText = document.createElement("span");
//         } else {
//             errorText = errorText[0];
//         }

//         errorText.className = "error-text";
//         errorText.textContent = value;

//         label.append(errorText);
//     }

//     function validateForm(event) {
//         event.preventDefault();

//         const noValueError = "Поле не заполнено";
//         let form = event.target;
//         let errors = {};
//         if (!form.login.value) {
//             errors["login"] = noValueError;
//         }
//         if (!form.password.value) {
//             errors["password"] = noValueError;
//         }
//         if (!form.ip.value) {
//             errors["ip"] = noValueError;
//         } else {
//             const re = /^(?<first>[1-9]?[1-9]?[0-9])\.(?<second>[1-9]?[1-9]?[0-9])\.(?<third>[1-9]?[1-9]?[0-9])\.(?<fourth>[1-9]?[1-9]?[0-9])$/
//             result = re.exec(form.ip.value);
//             if (result != null) {
//                 for (key in result.groups) {
//                     let value = Number(result.groups[key]);                    
//                     if (value < 0 || value > 255) {
//                         errors["ip"] = "Невалидное значение ip адреса";
//                     }
//                 };
//             } else {
//                 errors["ip"] = "Невалидная форма ip адреса";
//             }
//         }
//         if (!form.port.value) {
//             errors["port"] = noValueError;
//         }

//         if (!Object.keys(errors).length) {
//             form.submit();
//         } else {
//             for (key in errors) {
//                 setFormError(key, errors[key]);
//             }
//         }   
//     }

//     function createLabelInput(params) {
//         let label = document.createElement("label");
//         label.className = params.labelClasses;

//         let span = document.createElement("span");
//         span.className = "label-bold";
//         span.textContent = params.spanText;
//         label.append(span);

//         let input = document.createElement("input");
//         for (key in params.inputAttrs) {
//             input.setAttribute(key, params.inputAttrs[key]);
//         }
//         input.addEventListener("focus", () => {
//             label.classList.remove("error");
//             let errorText = label.getElementsByClassName("error-text");
//             if (errorText.length) {
//                 errorText[0].remove();
//             }
//         });
//         if (params.labelClasses.includes("password")) {
//             let inputBox = document.createElement("div");
//             inputBox.className = "input-box";
//             let img = document.createElement("img");
//             img.className = "icon-button show-password";
//             img.src = img_look;
//             img.alt = "show";
//             img.addEventListener("click", () => {                
//                 let oldType = input.getAttribute("type");
//                 input.setAttribute("type", oldType === "password" ? "text": "password");
//             });

//             inputBox.append(input);
//             inputBox.append(img);
//             label.append(inputBox);
//         } else {
//             label.append(input);
//         }
        
//         return label
//     }

//     function createCameraWindow(values) {
//         let cameraWindow = document.createElement("div");
//         cameraWindow.className = "camera-window";
        
//         let btnCrossContainer = document.createElement("div");
//         btnCrossContainer.className = "row-right-container";
//         let btnCross = document.createElement("div");
//         btnCross.className = "button-cross";
//         btnCross.addEventListener("click", () => {
//             formsContainer.classList.add("hidden");
//             cameraWindow.remove();
//         });
//         btnCrossContainer.append(btnCross);

//         let content = document.createElement("div");
//         content.className = "container__content";
//         let title = document.createElement("h2");
//         title.textContent = values["title"];
//         let form = document.createElement("form");
//         form.setAttribute("name", values.formName);
//         form.setAttribute("action", values.formAction);
//         form.setAttribute("method", "post");
//         form.addEventListener("submit", validateForm);

//         let formInputs = document.createElement("div");
//         formInputs.className = "form-inputs";

//         formInputs.append(createLabelInput({
//             "labelClasses": "filled",
//             "spanText": "login:",
//             "inputAttrs": {
//                 type: "text",
//                 name: "login",
//                 value: values.values != null ? values.values.login : "",
//                 maxlength: "100",
//                 placeholder: "camera123",
//             }
//         }));
//         formInputs.append(createLabelInput({
//             "labelClasses": "filled password",
//             "spanText": "password:",
//             "inputAttrs": {
//                 type: "password",
//                 name: "password",
//                 value: values.values != null ? values.values.password : "",
//                 maxlength: "100",
//                 placeholder: "verydifficultpassword",
//             }
//         }));
//         formInputs.append(createLabelInput({
//             "labelClasses": "filled",
//             "spanText": "ip:",
//             "inputAttrs": {
//                 type: "text",
//                 name: "ip",
//                 value: values.values != null ? values.values.ip : "",
//                 maxlength: "20",
//                 placeholder: "220.110.120.13",
//             }
//         }));
//         formInputs.append(createLabelInput({
//             "labelClasses": "filled",
//             "spanText": "port:",
//             "inputAttrs": {
//                 type: "number",
//                 name: "port",
//                 value: values.values != null ? values.values.port : "",
//                 maxlength: "99999",
//                 placeholder: "4567",
//             }
//         }));
//         let button = document.createElement("button");
//         button.type = "submit";
//         button.className = "primary submit-form";
//         let buttonText = document.createElement("span");
//         buttonText.textContent = values.btnText;
//         button.append(buttonText);

//         form.append(formInputs);
//         form.append(button);
//         content.append(title);
//         content.append(form);

//         cameraWindow.append(btnCrossContainer);
//         cameraWindow.append(content);
//         return cameraWindow;
//     }

//     function createDeleteWindow(cameraId) {
//         let deleteWindow = document.createElement("div");
//         deleteWindow.className = "delete-window";

//         let title = document.createElement("p");
//         title.textContent = `Вы точно хотите удалить камеру #${cameraId} ?`;

//         let buttonsBox = document.createElement("div");
//         buttonsBox.className = "buttons-box";

//         let btnClose = document.createElement("button");
//         btnClose.className = "basic close-window";
//         let btnCloseText = document.createElement("span");
//         btnCloseText.textContent = "Закрыть";
//         btnClose.append(btnCloseText);
//         btnClose.addEventListener("click", () => {
//             formsContainer.classList.add("hidden");
//             deleteWindow.remove();
//         });

//         let form = document.createElement("form");
//         form.setAttribute("action", `/cameras/${cameraId}/delete`);
//         form.setAttribute("method", "post");

//         let btnDelete = document.createElement("button");
//         btnDelete.className = "danger delete-camera";
//         btnDelete.type = "submit";
//         let btnDeleteText = document.createElement("span");
//         btnDeleteText.textContent = "Удалить камеру";
//         btnDelete.append(btnDeleteText);

//         form.append(btnDelete);
//         buttonsBox.append(btnClose);
//         buttonsBox.append(form);

//         deleteWindow.append(title);
//         deleteWindow.append(buttonsBox);
//         return deleteWindow;
//     }

//     function showFormsContainer() {
//         if (formsContainer.classList.contains("hidden")) {
//             formsContainer.classList.remove("hidden");
//         }
//     }

//     async function getCameraData(cameraId) {
//         const url = window.location.href + `/${cameraId}`;
//         let result = await fetch(url)
//             .then((response) => {
//                 return response.json();
//             });

//         return result;
//     }




//     const img_look = `http://${window.location.host}/static/images/look.png`;  

//     const btnAddCamera = document.getElementsByClassName("btn-add-camera")[0];
//     const formsContainer = document.getElementsByClassName("forms-container")[0];

//     btnAddCamera.addEventListener("click", () => {
//         showFormsContainer();
//         let cameraWindow = createCameraWindow({
//             "title": "Добавление новой видеокамеры в БД",
//             "formName": "add-camera",
//             "formAction": "/cameras/add",
//             "btnText": "Добавить видеокамеру",
//             "values": null,
//         });

//         formsContainer.append(cameraWindow);
//     });

//     const btnsEditCamera = document.getElementsByClassName("btn-edit-camera");
//     for (let i = 0; i < btnsEditCamera.length; i++) {
//         btnsEditCamera[i].addEventListener("click", (event) => {
            
//             let cameraId = event.target.dataset.id;
            
//             let result = getCameraData(cameraId)
//                 .then((data) => {
//                     showFormsContainer();
//                     let cameraWindow = createCameraWindow({
//                         "title": `Изменение видеокамеры #${cameraId}`,
//                         "formName": "edit-camera",
//                         "formAction": `/cameras/${cameraId}/edit`,
//                         "btnText": "Сохранить",
//                         "values": data,
//                     });
//                     formsContainer.append(cameraWindow);
//                 })
//                 .catch((error) => {
//                     console.log("No access to server");                    
//                 });
//         });
//     }

//     const btnsDeleteCamera = document.getElementsByClassName("btn-delete-camera");
//     for (let i = 0; i < btnsDeleteCamera.length; i++) {
//         btnsDeleteCamera[i].addEventListener("click", (event) => {
//             showFormsContainer();

//             let cameraId = event.target.dataset.id;

//             let deleteWindow = createDeleteWindow(cameraId);
//             formsContainer.append(deleteWindow);
//         });
//     }
// });

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
        }
    },

    methods: {
        showAddCameraForm() {
            this.current_form = 'add';
        },

        closeForm() {
            this.current_form = null;
            this.errors = {};
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
                console.log(data);
                fetch("/cameras/add", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: requestBody
                })
                    .then(r => r.json())
                    .then((r) => {
                        console.log(r);
                        this.cameras.push(r);
                    })
                this.sending = false;
                this.current_form = null;
                this.errors = {};
            }
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
