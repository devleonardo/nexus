// // ELEMENTOS DO MODAL SALVAR
var save = document.getElementById('modalSave');
var openModalBtnSave = document.getElementById('saveNewUser');
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

// Seleciona o input
const input = document.getElementById('cpfUsuario');

// Adiciona um listener para o evento 'input'
input.addEventListener('input', function() {
    // Remove caracteres que não sejam números
    this.value = this.value.replace(/\D/g, '');

    // Limita o comprimento para 11 dígitos
    if (this.value.length > 11) {
        this.value = this.value.slice(0, 11);
    }
});
