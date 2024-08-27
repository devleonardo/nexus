// Função que não permite o submit caso não tenha nada escrito no input
const campoBusca = document.getElementById("floatingInputValue");
const botaoBuscarAD = document.getElementById("buscarURL");

campoBusca.addEventListener('input', () => {
    if (campoBusca.value.trim() !== '') {
        botaoBuscarAD.removeAttribute('disabled');
    } else {
        botaoBuscarAD.setAttribute('disabled', 'disabled');
    }
});

//FUNÇÂO PARA COPIAR TODOS OS SITES BLOQUEADOS PARA A ÁREA DE TRABALHO
function copiarSites() {
    var tabela = document.getElementById("searchResult");
    
    var sitesBloqueados = "";

    for (var i = 0, row; row = tabela.rows[i]; i++) {
        for (var j = 0, col; col = row.cells[j]; j++) {
            sitesBloqueados += col.innerText + "\n";
        }
    }

    navigator.clipboard.writeText(sitesBloqueados).then(function() {

        // Cria o elemento principal <div class="notification-{{category}} active" id="notificationDiv">
        var notificationDiv = document.createElement('div');
        notificationDiv.classList.add('notification-success', 'active');
        notificationDiv.id = 'notificationDiv';

        // Cria o elemento <div class="notification-content">
        var notificationContent = document.createElement('div');
        notificationContent.classList.add('notification-content');
        
        // Cria o elemento <i class="bi bi-check-circle-fill notificationCheck-{{category}}"></i>
        var icon = document.createElement('i');
        icon.classList.add('bi', 'bi-check-circle-fill', 'notificationCheck-success');

        // Cria o elemento <div class="message">
        var messageDiv = document.createElement('div');
        messageDiv.classList.add('message');

        // Cria os elementos <span class="text text-1">{{ "Sucesso" if category == "success" else "Erro"}}</span>
        var text1 = document.createElement('span');
        text1.classList.add('text', 'text-1');
        text1.textContent = "Sucesso";

        // Cria o elemento <span class="text text-2">{{ message }}</span>
        var text2 = document.createElement('span');
        text2.classList.add('text', 'text-2');
        text2.textContent = "Domínios copiados!";

        // Adiciona os elementos de texto ao <div class="message">
        messageDiv.appendChild(text1);
        messageDiv.appendChild(text2);

        // Adiciona o ícone e a mensagem ao <div class="notification-content">
        notificationContent.appendChild(icon);
        notificationContent.appendChild(messageDiv);

        // Cria o ícone de fechar <i class="bi bi-x close" id="closeNotification"></i>
        var closeIcon = document.createElement('i');
        closeIcon.classList.add('bi', 'bi-x', 'close');
        closeIcon.id = 'closeNotification';

        // Cria o elemento <div class="progress active"></div>
        var progressDiv = document.createElement('div');
        progressDiv.classList.add('progress', 'active');

        // Adiciona todos os elementos ao <div class="notification-{{category}} active" id="notificationDiv">
        notificationDiv.appendChild(notificationContent);
        notificationDiv.appendChild(closeIcon);
        notificationDiv.appendChild(progressDiv);

        // Adiciona a <div class="notification-content"> ao footer
        var footer = document.getElementById('version');
        footer.appendChild(notificationDiv);
        
    }, function() {
        // Cria o elemento principal <div class="notification-{{category}} active" id="notificationDiv">
        var notificationDiv = document.createElement('div');
        notificationDiv.classList.add('notification-error', 'active');
        notificationDiv.id = 'notificationDiv';

        // Cria o elemento <div class="notification-content">
        var notificationContent = document.createElement('div');
        notificationContent.classList.add('notification-content');
        
        // Cria o elemento <i class="bi bi-check-circle-fill notificationCheck-{{category}}"></i>
        var icon = document.createElement('i');
        icon.classList.add('bi', 'bi-check-circle-fill', 'notificationCheck-error');

        // Cria o elemento <div class="message">
        var messageDiv = document.createElement('div');
        messageDiv.classList.add('message');

        // Cria os elementos <span class="text text-1">{{ "Sucesso" if category == "success" else "Erro"}}</span>
        var text1 = document.createElement('span');
        text1.classList.add('text', 'text-1');
        text1.textContent = "Erro";

        // Cria o elemento <span class="text text-2">{{ message }}</span>
        var text2 = document.createElement('span');
        text2.classList.add('text', 'text-2');
        text2.textContent = "Erro ao copiar domínios!";

        // Adiciona os elementos de texto ao <div class="message">
        messageDiv.appendChild(text1);
        messageDiv.appendChild(text2);

        // Adiciona o ícone e a mensagem ao <div class="notification-content">
        notificationContent.appendChild(icon);
        notificationContent.appendChild(messageDiv);

        // Cria o ícone de fechar <i class="bi bi-x close" id="closeNotification"></i>
        var closeIcon = document.createElement('i');
        closeIcon.classList.add('bi', 'bi-x', 'close');
        closeIcon.id = 'closeNotification';

        // Cria o elemento <div class="progress active"></div>
        var progressDiv = document.createElement('div');
        progressDiv.classList.add('progress', 'active');

        // Adiciona todos os elementos ao <div class="notification-{{category}} active" id="notificationDiv">
        notificationDiv.appendChild(notificationContent);
        notificationDiv.appendChild(closeIcon);
        notificationDiv.appendChild(progressDiv);

        // Adiciona a <div class="notification-content"> ao footer
        var footer = document.getElementById('version');
        footer.appendChild(notificationDiv);
    });
}
