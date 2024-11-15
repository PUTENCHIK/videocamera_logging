window.addEventListener("DOMContentLoaded", () => {

    function createLabelInput(params) {
        let label = document.createElement("label");
        label.className = params.labelClasses;

        let span = document.createElement("span");
        span.className = "label-bold";
        span.textContent = params.spanText;
        label.append(span);

        let input = document.createElement("input");
        for (key in params.inputAttrs) {
            input.setAttribute(key, params.inputAttrs[key]);
        }
        if (params.labelClasses.includes("password")) {
            let inputBox = document.createElement("div");
            inputBox.className = "input-box";
            let img = document.createElement("img");
            img.className = "icon-button show-password";
            img.src = img_look;
            img.alt = "show";
            img.addEventListener("click", () => {                
                let oldType = input.getAttribute("type");
                input.setAttribute("type", oldType === "password" ? "text": "password");
            });

            inputBox.append(input);
            inputBox.append(img);
            label.append(inputBox);
        } else {
            label.append(input);
        }
        
        return label
    }

    function createCameraWindow(values) {
        let cameraWindow = document.createElement("div");
        cameraWindow.className = "camera-window";
        
        let btnCrossContainer = document.createElement("div");
        btnCrossContainer.className = "row-right-container";
        let btnCross = document.createElement("div");
        btnCross.className = "button-cross";
        btnCross.addEventListener("click", () => {
            formsContainer.classList.add("hidden");
            cameraWindow.remove();
        });
        btnCrossContainer.append(btnCross);

        let content = document.createElement("div");
        content.className = "container__content";
        let title = document.createElement("h2");
        title.textContent = values["title"];
        let form = document.createElement("form");
        form.setAttribute("name", values.formName);
        form.setAttribute("action", values.formAction);
        form.setAttribute("method", "post");
        let formInputs = document.createElement("div");
        formInputs.className = "form-inputs";

        formInputs.append(createLabelInput({
            "labelClasses": "filled",
            "spanText": "login:",
            "inputAttrs": {
                type: "text",
                name: "login",
                value: values.values != null ? values.values.login : "",
                maxlength: "100",
                placeholder: "camera123",
            }
        }));
        formInputs.append(createLabelInput({
            "labelClasses": "filled password",
            "spanText": "password:",
            "inputAttrs": {
                type: "password",
                name: "password",
                value: values.values != null ? values.values.password : "",
                maxlength: "100",
                placeholder: "verydifficultpassword",
            }
        }));
        formInputs.append(createLabelInput({
            "labelClasses": "filled",
            "spanText": "ip:",
            "inputAttrs": {
                type: "text",
                name: "ip",
                value: values.values != null ? values.values.ip : "",
                maxlength: "20",
                placeholder: "220.110.120.13",
            }
        }));
        formInputs.append(createLabelInput({
            "labelClasses": "filled",
            "spanText": "port:",
            "inputAttrs": {
                type: "number",
                name: "port",
                value: values.values != null ? values.values.port : "",
                maxlength: "99999",
                placeholder: "4567",
            }
        }));
        let button = document.createElement("button");
        button.type = "submit";
        button.className = "primary submit-form";
        let buttonText = document.createElement("span");
        buttonText.textContent = values.btnText;
        button.append(buttonText);

        form.append(formInputs);
        form.append(button);
        content.append(title);
        content.append(form);

        cameraWindow.append(btnCrossContainer);
        cameraWindow.append(content);
        return cameraWindow;
    }

    function createDeleteWindow(cameraId) {
        let deleteWindow = document.createElement("div");
        deleteWindow.className = "delete-window";

        let title = document.createElement("p");
        title.textContent = `Вы точно хотите удалить камеру #${cameraId} ?`;

        let buttonsBox = document.createElement("div");
        buttonsBox.className = "buttons-box";

        let btnClose = document.createElement("button");
        btnClose.className = "basic close-window";
        let btnCloseText = document.createElement("span");
        btnCloseText.textContent = "Закрыть";
        btnClose.append(btnCloseText);
        btnClose.addEventListener("click", () => {
            formsContainer.classList.add("hidden");
            deleteWindow.remove();
        });

        let form = document.createElement("form");
        form.setAttribute("action", `/cameras/${cameraId}/delete`);
        form.setAttribute("method", "post");

        let btnDelete = document.createElement("button");
        btnDelete.className = "danger delete-camera";
        btnDelete.type = "submit";
        let btnDeleteText = document.createElement("span");
        btnDeleteText.textContent = "Удалить камеру";
        btnDelete.append(btnDeleteText);

        form.append(btnDelete);
        buttonsBox.append(btnClose);
        buttonsBox.append(form);

        deleteWindow.append(title);
        deleteWindow.append(buttonsBox);
        return deleteWindow;
    }

    function addEventListeners(formWindow) {
        let btnCross = formWindow.getElementsByClassName("button-cross");
        if (btnCross.length) {
            btnCross[0].addEventListener("click", () => {
                formWindow.classList.add("hidden");
                formsContainer.classList.add("hidden");
            });
        }

        let btnShowPassword = formWindow.getElementsByClassName("show-password");
        if (btnShowPassword.length) {
            btnShowPassword[0].addEventListener("click", (event) => {
                let btnContainer = event.target.parentElement;
                let inputPassword = btnContainer.getElementsByTagName("input")[0];
                let oldType = inputPassword.getAttribute("type");
                inputPassword.setAttribute("type", oldType === "password" ? "text": "password");
            });
        }
    }

    function setFormValues(form, values) {
        form.login.value = values['login'];
        form.password.value = values['password'];
        form.ip.value = values['ip'];
        form.port.value = values['port'];
    }

    function showWindow(formWindow, extraParams) {
        if (formWindow.classList.contains("hidden")) {
            formWindow.classList.remove("hidden");
        }

        addEventListeners(formWindow);

        if (extraParams != null) {
            let title = formWindow.getElementsByTagName("h2")[0];
            title.textContent = extraParams.title;

            let form = formWindow.getElementsByTagName("form")[0];
            form.setAttribute("name", extraParams.formName);
            form.setAttribute("action", extraParams.formAction);

            let btnSubmit = formWindow.getElementsByClassName("submit-form")[0];
            let btnText = btnSubmit.getElementsByTagName("span")[0];
            btnText.textContent = extraParams.buttonSubmit;

            setFormValues(form, extraParams.values == null ?
                {"login": "", "password": "", "ip": "", "port": ""} :
                {
                    "login": extraParams.values["login"],
                    "password": extraParams.values["password"],
                    "ip": extraParams.values["ip"],
                    "port": extraParams.values["port"]
                }
            )
        }
    }

    function showFormsContainer() {
        if (formsContainer.classList.contains("hidden")) {
            formsContainer.classList.remove("hidden");
        }
    }

    async function getCameraData(cameraId) {
        const url = window.location.href + `/${cameraId}`;
        let result = await fetch(url)
            .then((response) => {
                return response.json();
            });

        return result;
    }




    const img_look = `http://${window.location.host}/static/images/look.png`;  

    const btnAddCamera = document.getElementsByClassName("btn-add-camera")[0];
    const formsContainer = document.getElementsByClassName("forms-container")[0];

    btnAddCamera.addEventListener("click", () => {
        showFormsContainer();
        let cameraWindow = createCameraWindow({
            "title": "Добавление новой видеокамеры в БД",
            "formName": "add-camera",
            "formAction": "/cameras/add",
            "btnText": "Добавить видеокамеру",
            "values": null,
        });

        formsContainer.append(cameraWindow);
    });

    const btnsEditCamera = document.getElementsByClassName("btn-edit-camera");
    for (let i = 0; i < btnsEditCamera.length; i++) {
        btnsEditCamera[i].addEventListener("click", (event) => {
            showFormsContainer();
    
            let cameraId = event.target.dataset.id;
            
            let result = getCameraData(cameraId)
                .then((data) => {
                    let cameraWindow = createCameraWindow({
                        "title": `Изменение видеокамеры #${cameraId}`,
                        "formName": "edit-camera",
                        "formAction": `/cameras/${cameraId}/edit`,
                        "btnText": "Сохранить",
                        "values": data,
                    });
                    formsContainer.append(cameraWindow);
                });
        });
    }

    const btnsDeleteCamera = document.getElementsByClassName("btn-delete-camera");
    for (let i = 0; i < btnsDeleteCamera.length; i++) {
        btnsDeleteCamera[i].addEventListener("click", (event) => {
            showFormsContainer();

            let cameraId = event.target.dataset.id;

            let deleteWindow = createDeleteWindow(cameraId);
            formsContainer.append(deleteWindow);
        });
    }
});