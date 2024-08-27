// Obtendo valores para utilizar nas funções posteriores
const modalBuscaOrigin = document.getElementById('modalBuscaOrigin');
const cancelBuscaOrigin = document.getElementById('cancelBuscaOrigin');
const openModalBuscaOrigin = document.getElementById('showOriginGroups');

// Função para abrir o modal de buscar usuário de origem
openModalBuscaOrigin.addEventListener('click', () => {
    modalBuscaOrigin.style.display = "block";
});

// Função para cancelar o modal sem enviar o formulário
cancelBuscaOrigin.addEventListener('click', (event) => {
    modalBuscaOrigin.style.display = "none";
    event.preventDefault();
});

// Assync
class FormSubmit {
    constructor(settings) {
        this.settings = settings;
        this.form = document.getElementById('formSearchOrigin');
        this.formButton = document.getElementById('confirmBuscaOrigin');
        if (this.form) {
            this.url = this.form.getAttribute("action");
        }
        this.sendForm = this.sendForm.bind(this);
    }

    displaySuccess() {
        this.form.innerHTML = this.settings.success;
    }

    displayError() {
        this.form.innerHTML = this.settings.error;
    }

    getFormObject() {
        const formObject = {};
        const fields = this.form.querySelectorAll("[name");
        fields.forEach((field) => {
            formObject[field.getAttribute("name")] = field.value;
        });
        return formObject;
    }

    onSubmission(event) {
        event.preventDefault();
        event.target.disabled = true;
        event.target.innerText = "Buscando...";
    }
    
    async sendForm(event) {
        try{
            this.onSubmission(event);

            const response = await fetch(this.url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Accept: "application/json",
                },
                body: JSON.stringify(this.getFormObject()),
            });

            if (response.ok) {
                
                const data = await response.json(); // Captura o retorno do servidor
                
                var div = document.createElement("div");
                var divII = document.createElement("div");
                var divIII = document.createElement("div");
                var divIV = document.createElement("div");
                
                var ul = document.createElement("ul");
                var li = document.createElement("li");
                
                var h2 = document.createElement("h2");
                var strong = document.createElement("strong");
                
                var form = document.getElementById('formGroupClone');
                
                var buttonSubmitCopy = document.createElement("button");
                var buttonCancelCopy = document.createElement("button");
                
                var inpt = document.createElement('input');
                
                div.classList.add("modal");
                div.id = "addGroupsUser";

                div.appendChild(form)

                divII.classList.add("modal-content");
                divII.classList.add("copyGroupModal");
                form.appendChild(divII);

                h2.innerText = "Copiando grupos";
                divII.appendChild(h2);

                divIV.style.display = "flex";
                divIV.style.gap = 5 + "px";
                divIV.style.justifyContent = "center";
                divIV.style.alignItems = "center";

                strong.innerText = "Grupos de:";
                divIV.appendChild(strong);

                inpt.name = "usuarioOrigem";
                inpt.value = data.origem;
                inpt.id = "inptName";
                inpt.innerText = data.origem;
                inpt.readOnly = true;
                inpt.type = "text";

                divIV.appendChild(inpt);

                divII.appendChild(divIV);




                ul.classList.add("item-list");
                ul.id = "copyGroupUl";

                li.id = "copyGroupLi";

                divIII.style.display = "flex";
                divIII.style.gap = 10 + "px";
                divIII.style.justifyContent = "center";
                divIII.style.alignItems = "center";
                
                buttonSubmitCopy.classList.add("btn", "btn-success", "carregar");
                buttonSubmitCopy.id = "saveCopyGroup";
                buttonSubmitCopy.type = "submit";
                buttonSubmitCopy.innerText = "Executar";
                divIII.appendChild(buttonSubmitCopy);

                buttonCancelCopy.classList.add("btn", "btn-danger");
                buttonCancelCopy.id = "cancelCopyGroup";
                buttonCancelCopy.innerText = "Cancelar";
                divIII.appendChild(buttonCancelCopy);
                
                data.grupos.forEach((grupo, indice) => {
                    const input = document.createElement('input');
                    const label = document.createElement('label');
                    
                    input.type = "checkbox";
                    input.checked = true;
                    input.name = "groups_to_copy";
                    input.value = grupo;
                    input.id = "id" + (indice + 1);
                    input.className = "hiddenInputGroup";
                    
                    li.appendChild(input);

                    label.setAttribute('for', 'id' + (indice + 1));
                    label.className = "copyGroupName";
                    label.innerText = grupo;

                    li.appendChild(label)

                    ul.appendChild(li);    
                });

                divII.appendChild(ul);
                
                divII.appendChild(divIII);

                console.log('Dados:', data)

                document.body.appendChild(div);
                
                modalBuscaOrigin.style.display = "none";
                
                div.style.display = "block";

                const cancelCopyGroup = document.getElementById('cancelCopyGroup');
                cancelCopyGroup.addEventListener('click', (event) => {
                    event.preventDefault();
                    const onCancel = document.getElementById('addGroupsUser');
                    onCancel.remove();
                });

                buttonSubmitCopy.addEventListener('click', () => {
                    var loadingOverlay = document.getElementById("carregamento");
                    loadingOverlay.style.display = "block";
                });
                
            } else {
                console.error('Erro ao enviar formulário:', response.statusText);
                this.displayError();
            }

        } catch (error) {
            console.error('Erro ao obter grupos:', error)
            this.displayError();
        } finally {
            event.target.disabled = false;
            event.target.innerText = "Buscar";
        }
    }

    init() {
        if (this.form) this.formButton.addEventListener("click", this.sendForm);
        return this;
    }
}

const formSubmit = new FormSubmit({
    form: "[data-form]",
    button: "[data-button]",
    success: '<div class="alert alert-success alert-dismissible fade show" role="alert">Grupos clonados com sucesso!<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>',
    error: '<div class="alert alert-danger alert-dismissible fade show error" role="alert">Falha ao clonar grupos!<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>'
});

formSubmit.init();
