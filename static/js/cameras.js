window.addEventListener("DOMContentLoaded", () => {

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

            if (extraParams.values != null) {

            }
        }
    }

    function showFormsContainer() {
        if (formsContainer.classList.contains("hidden")) {
            formsContainer.classList.remove("hidden");
        }
    }

    const btnAddCamera = document.getElementsByClassName("btn-add-camera")[0];
    const formsContainer = document.getElementsByClassName("forms-container")[0];

    btnAddCamera.addEventListener("click", () => {
        showFormsContainer();

        let cameraWindow = formsContainer.getElementsByClassName("camera-window")[0];

        showWindow(cameraWindow, {
            "title": "Добавление новой видеокамеры в БД",
            "formName": "add-camera",
            "formAction": "/cameras/add",
            "buttonSubmit": "Добавить видеокамеру",
            "values": null
        });
    });

    const btnsEditCamera = document.getElementsByClassName("btn-edit-camera");
    for (let i = 0; i < btnsEditCamera.length; i++) {
        btnsEditCamera[i].addEventListener("click", (event) => {
            showFormsContainer();
    
            let cameraWindow = formsContainer.getElementsByClassName("camera-window")[0];
    
            showWindow(cameraWindow, {
                "title": "Изменение видеокамеры #123",
                "formName": "edit-camera",
                "formAction": "/cameras/edit",
                "buttonSubmit": "Сохранить",
                "values": null
            });
        });
    }

    // const btnsDeleteCamera = document.getElementsByClassName("btn-delete-camera");
    // for (let i = 0; i < btnsDeleteCamera.length; i++) {
    //     btnsDeleteCamera[i].addEventListener("click", (event) => {
    //         showFormsContainer();

    //         let deleteWindow = formsContainer.getElementsByClassName("delete-window")[0];
    //         showWindow(deleteWindow);
    //     });
    // }
});