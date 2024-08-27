////////////////////////////////////////////////////////////////////
//                      MODAL REMOVER ESTAÇÃO                     //
////////////////////////////////////////////////////////////////////
// // // ELEMENTOS DO MODAL REMOVER
var remove = document.getElementById('modalRemove');
var openModalBtnRemove = document.getElementById('remove');
var confirmBtnRemove = document.getElementById('confirmBtnRemove');
var cancelBtnRemove = document.getElementById('cancelBtnRemove');

// FUNÇÃO PARA ABRIR O MODAL
function openRemove() {
    remove.style.display = 'block';
}

// FUNÇÃO PARA FECHAR O MODAL
function closeRemove() {
    remove.style.display = 'none';
}

// EVENTO DE CLICK NO BOTÕES
openModalBtnRemove.addEventListener('click', openRemove);
confirmBtnRemove.addEventListener('click', closeRemove);
cancelBtnRemove.addEventListener("click", (event) => {
    event.preventDefault(); // EVITA O ENVIO DO FORMULÁRIO
    closeRemove();
    // OUTRAS AÇÕES QUE VOCÊ DESEJA EXECUTAR AO CLICAR NO BOTÃO "CANCELAR"
});

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////

// // // Elementos do modal Remover
var add = document.getElementById('modalAdd');
var openModalBtnAdd = document.getElementById('add');
var confirmBtnAdd = document.getElementById('confirmBtnAdd');
var cancelBtnAdd = document.getElementById('cancelBtnAdd');

// Função para abrir o modal
function openAdd() {
    add.style.display = 'block';
}

// Função para fechar o modal
function closeAdd() {
    add.style.display = 'none';
}

// Eventos de clique nos botões
openModalBtnAdd.addEventListener('click', openAdd);
confirmBtnAdd.addEventListener('click', closeAdd);
cancelBtnAdd.addEventListener("click", (event) => {
    event.preventDefault(); // Evita o envio do formulário
    closeAdd();
    // Outras ações que você deseja executar ao clicar no botão "Cancelar"
});

///////////////////////////////////////////////////////////////////////////////

function adicionarItem() {
    // Obter o elemento select pelo ID
    var listaSuspensa = document.getElementById("listaSuspensa");
  
    // Obter o valor selecionado
    var itemSelecionado = listaSuspensa.value;
  
    // Obter o campo de entrada pelo ID
    var campoInput = document.getElementById("campoInput");
  
    // Definir o valor do campo de entrada com o item selecionado
    campoInput.value = itemSelecionado;
}