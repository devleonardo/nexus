////////////////////////////////////////////////////////////////////
//                    BARRA DE PESQUISA DE LOG                    //
////////////////////////////////////////////////////////////////////
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    const searchButton = document.getElementById('search-button');
    const logList = document.getElementById('log-list');

    function performSearch() {
        const searchTerm = searchInput.value.toLowerCase();
        const logs = logList.getElementsByTagName('li');

        for (let i = 0; i < logs.length; i++) {
            const logText = logs[i].textContent.toLowerCase();
            if (logText.includes(searchTerm)) {
                logs[i].style.display = 'block';
            } else {
                logs[i].style.display = 'none';
            }
        }
    }

    searchButton.addEventListener('click', () => {
        performSearch();
    });

    searchInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
            performSearch();
        }
    });
});

// SELECIONA O FORMULÁRIO
const form = document.querySelector('form');
// ADICIONA UM OUVINTE DE EVENTOS AO EVENTO "SUBMIT" DO FORMULÁRIO
form.addEventListener('submit', function(event) {
    // SELECIONA O CAMPO DE ENTRADA
    const input1 = document.querySelector('input[name="domain"]');
    const input2 = document.querySelector('input[name="username"]');
    // REMOVE OS ESPAÇOS EM BRANCO DO VALOR DO CAMPO DE ENTRADA
    input1.value = input1.value.trim();
    input2.value = input2.value.trim();
});

////////////////////////////////////////////////////////////////////
//               SALVA LOGIN E SENHA NO LOCALSTORAGE              //
////////////////////////////////////////////////////////////////////
function saveLoginData() {
    // OBTEM OS VALORES DOS CAMPO DE LOGIN E SENHA
    var username = document.getElementsByName('username')[0].value;
    var password = document.getElementsByName('password')[0].value;

    // VERIFICA SE O CHECKBOX ESTÁ MARCADO
    var rememberMe = document.getElementById('rememberMe').checked;

    if (rememberMe) {
        // SALVA OS DADOS DE LOGIN NO LOCALSTORAGE
        localStorage.setItem('username', username);
        localStorage.setItem('password', password);
    } else {
        // REMOVE OS DADOS DE LOGIN DO LOCALSTORAGE
        localStorage.removeItem('username');
        localStorage.removeItem('password');
    }
}

// FUNÇÃO PARA CARREGAR OS DADOS DE LOGIN DO localStorage, SE EXISTIREM
function loadLoginData() {
    var username = localStorage.getItem('username');
    var password = localStorage.getItem('password');

    if (username && password) {
        // PREENCHE OS CAMPOS DE LOGIN E SENHA COM OS VALORES DO LOCALSTORAGE
        document.getElementsByName('username')[0].value = username;
        document.getElementsByName('password')[0].value = password;
    }
}

// CHAMA A FUNÇÃO PARA CARREGAR OS DADOS DE LOGIN QUANDO A PAGINA É CARREGADA
window.onload = loadLoginData;

// document.getElementById('editar').onclick = function() {
//     var inputs = document.getElementsByTagName('input');
//     for (var i = 0; i < inputs.length; i++) {
//         inputs[i].disabled = false;
//     }
// }

document.addEventListener("DOMContentLoaded", function() {
    const editarBtn = document.getElementById("editar");

    editarBtn.addEventListener("click", function() {
        document.getElementById("salvar").style.display = "inline";
        document.getElementById("cancelar").style.display = "inline";
        document.getElementById("showOriginGroups").style.display = "inline";
        document.getElementById("user_nome").removeAttribute("disabled");
        document.getElementById("user_sobrenome").removeAttribute("disabled");
        document.getElementById("user_iniciais").removeAttribute("disabled");
        document.getElementById("user_funcao").removeAttribute("disabled");
        document.getElementById("user_email").removeAttribute("disabled");
        document.getElementById("user_cpf").removeAttribute("disabled");
        document.getElementById("user_agente").removeAttribute("disabled");
        document.getElementById("user_login").removeAttribute("disabled");
    });
});

// HABILITA OS INPUTS AO CLICAR EM EDITAR GRUPOS
document.addEventListener("DOMContentLoaded", function() {
    const editarBtnGp = document.getElementById("editar");
    const displayEdit = document.getElementById("conjBtn");

    
    editarBtnGp.addEventListener("click", function() {
        displayEdit.style.display = "grid";
        const checkboxes = document.querySelectorAll(".item-list input[type='checkbox']");
        checkboxes.forEach(function(checkbox) {
            checkbox.removeAttribute("disabled");
        })
    })
})

// CANCELA O ENVIO DO FORMULARIO CASO CANCELAR SEJA PRESSIONADO NA EDIÇÃO DE GRUPOS
document.addEventListener("DOMContentLoaded", function() {
    const cancelarAlteracao = document.getElementById("cancelar");
    
    function cancel() {
        location.reload()
    }

    cancelarAlteracao.addEventListener("click", (event) => {
        event.preventDefault();
        cancel();
    })
});

////////////////////////////////////////////////////////////////////
//                 MODAL SALVAR DADOS DO USUÁRIO                  //
////////////////////////////////////////////////////////////////////
// // ELEMENTOS DO MODAL SALVAR
var save = document.getElementById('modalSave');
var openModalBtnSave = document.getElementById('salvar');
var confirmBtnSave = document.getElementById('confirmBtnSave');
var cancelBtnSave = document.getElementById('cancelBtnSave');

// FUNÇÃO PARA ABRIR O MODAL
function openSave() {
    save.style.display = 'block';
}

// FUNÇÃO PARA FECHAR O MODAL
function closeSave() {
    save.style.display = 'none';
}

// EVENTO DE CLICK NOS BOTÕES
openModalBtnSave.addEventListener('click', openSave);
confirmBtnSave.addEventListener('click', closeSave);
cancelBtnSave.addEventListener("click", (event) => {
    event.preventDefault(); // EVITA O ENVIO DO FORMULÁRIO
    closeSave();
    // OUTRAS AÇÕES QUE VOCÊ DESEJA EXECUTAR AO CLICAR NO BOTÃO "CANCELAR"
});

////////////////////////////////////////////////////////////////////
//                     MODAL BLOQUEAR USUÁRIO                     //
////////////////////////////////////////////////////////////////////
// // ELEMENTOS DO MODAL BLOQUEAR
var block = document.getElementById('modalBlock');
var openModalBtnBlock = document.getElementById('bloquear');
var confirmBtnBlock = document.getElementById('confirmBtnBlock');
var cancelBtnBlock = document.getElementById('cancelBtnBlock');

// FUNÇÃO PARA ABRIR O MODAL
function openBlock() {
    block.style.display = 'block';
}

// FUNÇÃO PARA FECHAR O MODAL
function closeBlock() {
    block.style.display = 'none';
}

// EVENTO DE CLICK NO BOTÕES
openModalBtnBlock.addEventListener('click', openBlock);
confirmBtnBlock.addEventListener('click', closeBlock);
cancelBtnBlock.addEventListener("click", (event) => {
    event.preventDefault(); // Evita o envio do formulário
    closeBlock();
    // OUTRAS AÇÕES QUE VOCÊ DESEJA EXECUTAR AO CLICAR NO BOTÃO "CANCELAR"
});

////////////////////////////////////////////////////////////////////
//                        MODAL EDITAR SENHA                      //
////////////////////////////////////////////////////////////////////
// // ELEMENTOS DO MODAL EDITAR
var edit = document.getElementById('modalEdit');
var openModalBtnEdit = document.getElementById('editarSenha');
var confirmBtnEdit = document.getElementById('confirmBtnEdit');
var cancelBtnEdit = document.getElementById('cancelBtnEdit');

// FUNÇÃO PARA ABRIR O MODAL
function openEdit() {
    edit.style.display = 'block';
}

// FUNÇÃO PARA FECHAR O MODAL
function closeEdit() {
    edit.style.display = 'none';
}

// EVENTO DE CLICK NO BOTÕES
openModalBtnEdit.addEventListener('click', openEdit);
confirmBtnEdit.addEventListener('click', (event) => {
    event.preventDefault();
} );
cancelBtnEdit.addEventListener("click", (event) => {
    event.preventDefault(); // Evita o envio do formulário
    closeEdit();
    // OUTRAS AÇÕES QUE VOCÊ DESEJA EXECUTAR AO CLICAR NO BOTÃO "CANCELAR"
});

////////////////////////////////////////////////////////////////////
//              MODAL EXECUTAR ALTERAÇÃO DE SENHA                 //
////////////////////////////////////////////////////////////////////
// // ELEMENTOS DO MODAL BLOQUEAR
var reset = document.getElementById('modalReset');
var openModalBtnReset = document.getElementById('confirmBtnEdit');
var confirmBtnReset = document.getElementById('confirmBtnReset');
var cancelBtnReset = document.getElementById('cancelBtnReset');

// FUNÇÃO PARA ABRIR O MODAL
function openReset() {
    reset.style.display = 'block';
}

// FUNÇÃO PARA FECHAR O MODAL
function closeReset() {
    reset.style.display = 'none';
}

// EVENTO DE CLICK NO BOTÕES
openModalBtnReset.addEventListener('click', openReset);
confirmBtnReset.addEventListener('click', closeReset, );
cancelBtnReset.addEventListener("click", (event) => {
    event.preventDefault(); // Evita o envio do formulário
    closeReset();
    // OUTRAS AÇÕES QUE VOCÊ DESEJA EXECUTAR AO CLICAR NO BOTÃO "CANCELAR"
});

// MOSTRA A SENHA OU TORNA INVISIVEL
function togglePasswordVisibility() {
    // Seleciona o ícone
    var icon = document.getElementById("viewPass");
    // Verifica se a classe 'bi-eye-fill' está presente
    if (icon.classList.contains("bi-eye-fill")) {
        // Se estiver presente, remove 'bi-eye-fill' e adiciona 'bi-eye-slash-fill'
        icon.classList.remove("bi-eye-fill");
        icon.classList.add("bi-eye-slash-fill");
        // Altera o tipo do input para texto para exibir a senha
        document.getElementById("inputPassword").type = "text";
    } else {
        // Se não estiver presente, remove 'bi-eye-slash-fill' e adiciona 'bi-eye-fill'
        icon.classList.remove("bi-eye-slash-fill");
        icon.classList.add("bi-eye-fill");
        // Altera o tipo do input para senha para ocultar a senha
        document.getElementById("inputPassword").type = "password";
    }
}


// DESMARCA A SENHA FIXA CASO A ALTERAÇÃO DE SEJA NO PROXIMO LOGON ESTEJA MARCADA E VICE E VERSA
document.addEventListener('DOMContentLoaded', function() {
    var altSenha = document.getElementById('altSenha');
    var fixSenha = document.getElementById('fixSenha');
    var nAltSenha = document.getElementById('nAltSenha');

    altSenha.addEventListener('change', function() {
        if (this.checked) {
            fixSenha.disabled = true;
            nAltSenha.disabled = true;
        } else {
            fixSenha.disabled = false;
            nAltSenha.disabled = false;
        }
    });

    fixSenha.addEventListener('change', function() {
        if (this.checked) {
            altSenha.disabled = true;
        } else {
            altSenha.disabled = false;
        }
    });
});

// SE MARCAR QUE O USUARIO NÃO PODE ALTERAR SENHA, AUTOMATICAMENTE MARCA A SENHA FIXA
const naoPodeAlterarSenhaCheckbox = document.getElementById('nAltSenha');
const senhaNuncaExpiraCheckbox = document.getElementById('fixSenha');

// Adicionar um ouvinte de evento para o checkbox "Usuário não pode alterar a senha"
naoPodeAlterarSenhaCheckbox.addEventListener('change', function() {
    // Se o checkbox for marcado
    if (this.checked) {
        // Marcar automaticamente o checkbox "Senha nunca expira"
        senhaNuncaExpiraCheckbox.checked = true;
    } else {
        // Se desmarcar o checkbox "Usuário não pode alterar a senha", desmarcar também "Senha nunca expira"
        senhaNuncaExpiraCheckbox.checked = false;
    }
});

// FUNÇÃO RESPONSÁVEL PELA BUSCA DO GRUPO NO INPUT
function searchInGrupo() {
    var input, filter, ul, li, label, i, txtValue;
    input = document.getElementById('searchGrupo'); // Seletor do input de busca
    filter = input.value.toUpperCase();
    ul = document.querySelector('.list-grupos ul'); // Seletor da lista de templates

    li = ul.getElementsByTagName('li');
    for (i = 0; i < li.length; i++) {
        label = li[i].getElementsByClassName('grupo-name')[0]; // Classe que contém o texto a ser pesquisado
        txtValue = label.textContent || label.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = '';
        } else {
            li[i].style.display = 'none';
        }
    }
}

// FUNÇÃO PARA ABRIR LABEL DE BUSCAR GRUPOS AO CLICAR NA BARRA DE BUSCA
function exibirLabelGp() {
    var exibirGp = document.getElementById('org-grupo');

    exibirGp.style.display = 'block'
    window.scrollTo({
        top: document.body.scrollHeight,
        behavior: 'smooth' // Isso fará com que a rolagem seja suave, se suportado pelo navegador
    });
      
}

// LISTENER PARA FECHAR A DIV AO CLICAR FORA DELA

document.addEventListener('click', function(event) {
    var orgGrupoDiv = document.getElementById('org-grupo');
    var searchGrupoInput = document.getElementById('searchGrupo');
    if (!orgGrupoDiv.contains(event.target) && event.target !== searchGrupoInput) {
        orgGrupoDiv.style.display = 'none';
    }
});

// Exibe os grupos marcados para serem adicionados ao usuário e se forem desmarcados a exibição é removida
document.addEventListener('DOMContentLoaded', function() {
    const checkboxes = document.querySelectorAll('.checkgp');
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const value = this.value;
            const label = this.nextElementSibling.textContent;
            const existingItems = document.querySelectorAll('.item-list input[value="' + value + '"]');
            
            if (this.checked) {
                // Adicionar item se estiver marcado
                if (existingItems.length === 0) {
                    const newItem = document.createElement('li');
                    newItem.innerHTML = `<input type="checkbox" id="adicionado" class="chequebox" value="${value}" disabled><label id="labelAdicionado" for="adicionado">${label}</label>`;
                    document.querySelector('.item-list').appendChild(newItem);
                }
            } else {
                // Remover item se estiver desmarcado
                existingItems.forEach(item => {
                    item.parentNode.remove();
                });
            }
        });
    });
});

var telaCompleta = document.getElementById('telaCompleta');
var btnFechar = document.getElementById('btnFechar');

btnFechar.addEventListener('click', function() {
    telaCompleta.style.display = "none";
});


// NOTIFICATION CLOSE
var closeNotification = document.getElementById('closeNotification');
var notificationDiv = document.getElementById('notificationDiv');
closeNotification.addEventListener('click', () => {
    notificationDiv.style.display = 'none';
});