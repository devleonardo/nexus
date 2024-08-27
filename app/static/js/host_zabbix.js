// FUNÇÃO PARA BUSCAR NOS TEMPLATES
function searchInList() {
    var input, filter, ul, li, label, i, txtValue;
    input = document.getElementById('searchInput'); // Seletor do input de busca
    filter = input.value.toUpperCase();
    ul = document.querySelector('.list-templates ul'); // Seletor da lista de templates

    li = ul.getElementsByTagName('li');
    for (i = 0; i < li.length; i++) {
        label = li[i].getElementsByClassName('template-name')[0]; // Classe que contém o texto a ser pesquisado
        txtValue = label.textContent || label.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = '';
        } else {
            li[i].style.display = 'none';
        }
    }
}

// FUNÇÃO PARA BUSCAR NO GRUPO DE HOSTS
function searchInListII() {
    var input, filter, ul, li, label, i, txtValue;
    input = document.getElementById('searchInputII'); // O ID do seu input de busca
    filter = input.value.toUpperCase();
    ul = document.querySelector('.list-templatesII ul'); // O seletor da sua lista de templates

    li = ul.getElementsByTagName('li');
    for (i = 0; i < li.length; i++) {
        label = li[i].getElementsByClassName('template-nameII')[0]; // Classe que contém o texto a ser pesquisado
        txtValue = label.textContent || label.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = '';
        } else {
            li[i].style.display = 'none';
        }
    }
}

// Habilita o botão para enviar o formulário caso todos os inputs estejam preenchidos e pelo menos um checkbox marcado
document.addEventListener('DOMContentLoaded', function () {
    const criarHostBtn = document.getElementById('criar_host');
    const inputs = document.querySelectorAll('.novo-host input:not(#macros, #searchInput, #searchInputII)');
    const checkboxes = document.querySelectorAll('input[type=checkbox]');
    
    const updateButtonState = () => {
        const allInputsFilled = Array.from(inputs).every(input => input.value.trim() !== '');
        const atLeastOneCheckboxChecked = Array.from(checkboxes).some(checkbox => checkbox.checked);
        
        if (allInputsFilled && atLeastOneCheckboxChecked) {
            criarHostBtn.removeAttribute('disabled');
        } else {
            criarHostBtn.setAttribute('disabled', 'disabled');
        }
    };
    
    inputs.forEach(input => {
        input.addEventListener('input', updateButtonState);
    });
    
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', updateButtonState);
    });
});

        // MODAL PARA CONFIRMAR CRIAÇÃO DE HOST
        var criar = document.getElementById('modalCriarHost');
        var openModalBtnCriarHost = document.getElementById('criar_host');
        var confirmBtnCriarHost = document.getElementById('confirmBtnCriarHost');
        var cancelBtnCriarHost = document.getElementById('cancelBtnCriarHost');
        
        // FUNÇÃO PARA ABRIR O MODAL
        function openCriarHost() {
            criar.style.display = 'block';
        };
        
        // FUNÇÃO PARA FECHAR O MODAL
        function closeCriarHost() {
            criar.style.display = 'none';
        };
        
        // EVENTO DE CLICK NO BOTÕES
        openModalBtnCriarHost.addEventListener('click', openCriarHost);
        confirmBtnCriarHost.addEventListener('click', closeCriarHost, );
        cancelBtnCriarHost.addEventListener("click", (event) => {
            event.preventDefault(); // Evita o envio do formulário
            closeCriarHost();
        });
        
        // FUNÇÃO PARA HABILITAR O CAMPO DE MACROS APENAS SE O TIPO DE CONEXÃO FOR SNMP V1, 2 OU 3
        document.addEventListener("DOMContentLoaded", function () {
            const selectConexao = document.getElementById("conexao");
            const macrosField = document.getElementById("macros");
        
            // Desabilita o campo de macros inicialmente
            macrosField.disabled = true;
        
            // Adiciona um evento de mudança ao select de tipo de conexão
            selectConexao.addEventListener("change", function () {
                const selectedValue = selectConexao.value;
        
                // Se o valor selecionado for SNMPv1, SNMPv2 ou SNMPv3, habilita o campo de macros
                if (selectedValue === '2' || selectedValue === '21' || selectedValue === '22') {
                    macrosField.disabled = false;
                } else {
                    macrosField.disabled = true;
                }
            });
        });
        
        // Quando o alerta for fechado os botões tornam a ser clicáveis
        var alertStyle = document.getElementById('overlay');
        var closeAlert = document.getElementById('closeAlert');
        
        // Quando o botão de fechar for pressionado, a tela escura sairá e os botões voltarão a ser interativo
        closeAlert.addEventListener('click',() => {
            alertStyle.style.display = 'none'
        });