 // Obtém uma referência para o checkbox "Selecionar todos"
 const selectAllCheckbox = document.getElementById('selectAll');

 // Obtém uma lista de IDs que você deseja selecionar
 const idsToSelect = ['grl02', 'sji01', 'sji02', 'itb01', 'itb02', 'mrc01', 'mrc02', 'nit01', 'nit02', 'rdns01', 'rdns02', 'rdns03', 'rdns04', 'rdns05', 'rdns06'];

 // Adiciona um evento de escuta para o checkbox "Selecionar todos"
 selectAllCheckbox.addEventListener('change', function() {
     // Verifica se o "Selecionar todos" está marcado
     if (this.checked) {
         // Marca os checkboxes com os IDs desejados
         idsToSelect.forEach(id => {
             const checkbox = document.getElementById(id);
             if (checkbox) {
                 checkbox.checked = true;
             }
         });
     } else {
         // Desmarca os checkboxes com os IDs desejados
         idsToSelect.forEach(id => {
             const checkbox = document.getElementById(id);
             if (checkbox) {
                 checkbox.checked = false;
             }
         });
     }

     // Atualiza o valor do input oculto com base na seleção dos checkboxes
     updateAtLeastOneSelected();
 });

 // Adiciona um evento de escuta para os checkboxes individuais para chamar a função `updateAtLeastOneSelected` quando qualquer um deles for marcado ou desmarcado
 idsToSelect.forEach(id => {
     const checkbox = document.getElementById(id);
     if (checkbox) {
         checkbox.addEventListener('change', updateAtLeastOneSelected);
     }
 });

 // Função para verificar se pelo menos um dos checkboxes foi selecionado e atualizar o valor do `input` oculto
 function updateAtLeastOneSelected() {
     let atLeastOneSelected = false;
     idsToSelect.forEach(id => {
         const checkbox = document.getElementById(id);
         if (checkbox && checkbox.checked) {
             atLeastOneSelected = true;
         }
     })

     const atLeastOneSelectedInput = document.getElementById('atLeastOneSelected');
     if (atLeastOneSelectedInput) {
         atLeastOneSelectedInput.value = atLeastOneSelected ? 'true' : 'false';
     }
 }

 // Antes de enviar o formulário, verifique o valor do `input` oculto e impeça o envio se nenhum checkbox for selecionado
//  const form = document.getElementById('form-bloqueiodns');
//  if (form) {
//      form.addEventListener('submit', function(event) {
//          const atLeastOneSelectedInput = document.getElementById('atLeastOneSelected');
//          if (atLeastOneSelectedInput && atLeastOneSelectedInput.value === 'false') {
//              // Pelo menos um checkbox deve ser selecionado, caso contrário, impeça o envio do formulário
//              event.preventDefault();
//              alert('Selecione pelo menos um servidor.');
//          }
//      });
//  }

// ENVIO DO FORMULARIO MEDIANTE A CONFIRMAÇÃO NO MODAL
// // ELEMENTOS DO MODAL
var blockdns = document.getElementById('modalBlockdns');
var openModalBtnBlockdns = document.getElementById('bloqueardns');
var confirmBtnBlockdns = document.getElementById('confirmBtnBlockdns');
var cancelBtnBlockdns = document.getElementById('cancelBtnBlockdns');

// FUNÇÃO PARA ABRIR O MODAL
function openBlockdns() {
    blockdns.style.display = 'block';
}

// FUNÇÃO PARA FECHAR O MODAL
function closeBlockdns() {
    blockdns.style.display = 'none';
}

// EVENTO DE CLICK NO BOTÕES
openModalBtnBlockdns.addEventListener('click', function(event) {
    event.preventDefault();
    openBlockdns();
});
confirmBtnBlockdns.addEventListener('click', closeBlockdns);
cancelBtnBlockdns.addEventListener("click", (event) => {
    event.preventDefault(); // Evita o envio do formulário
    closeBlockdns();
});

// // ELEMENTOS DO MODAL ATT ANABLOCK
var blockdns = document.getElementById('modalBlockdns');
var openModalBtnBlockdns = document.getElementById('bloqueardns');
var confirmBtnBlockdns = document.getElementById('confirmBtnBlockdns');
var cancelBtnBlockdns = document.getElementById('cancelBtnBlockdns');

// FUNÇÃO PARA ABRIR O MODAL
function openBlockdns() {
    blockdns.style.display = 'block';
}

// FUNÇÃO PARA FECHAR O MODAL
function closeBlockdns() {
    blockdns.style.display = 'none';
}

// EVENTO DE CLICK NO BOTÕES
openModalBtnBlockdns.addEventListener('click', function(event) {
    event.preventDefault();
    openBlockdns();
});
confirmBtnBlockdns.addEventListener('click', closeBlockdns);
cancelBtnBlockdns.addEventListener("click", (event) => {
    event.preventDefault(); // Evita o envio do formulário
    closeBlockdns();
});



// Selecione o elemento com o ID "REVERT"
var revertCheckbox = document.getElementById("REVERT");

// Selecione os elementos de entrada que deseja desabilitar
var tituloInput = document.getElementById("titulo");
var ipInput = document.getElementById("ip");
var dominioInput = document.getElementById("dominio");

// Adicione um ouvinte de evento para o checkbox "REVERT"
revertCheckbox.addEventListener("change", function() {
    if (revertCheckbox.checked) {
        // Se o checkbox "REVERT" estiver marcado, desabilite os inputs
        tituloInput.disabled = true;
        ipInput.disabled = true;
        dominioInput.disabled = true;
    } else {
        // Caso contrário, habilite os inputs
        tituloInput.disabled = false;
        ipInput.disabled = false;
        dominioInput.disabled = false;
    }
});

// Desabilita todos os checkboxes caso "Atualizar Anablock" esteja marcado
document.getElementById('anablock').addEventListener('change', function() {
    var isChecked = this.checked;
    var inputs = document.querySelectorAll('.form-check-input');
    inputs.forEach(function(input) {
        if (input.id !== 'anablock') {
            input.disabled = isChecked;
        }
    });
    document.getElementById('titulo').disabled = isChecked;
    document.getElementById('ip').disabled = isChecked;
    document.getElementById('dominio').disabled = isChecked;
    // O botão "Executar" não será desabilitado
});