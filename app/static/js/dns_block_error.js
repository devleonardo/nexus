// Função para forçar o scroll acompanhar as novas linhas
function scrollToBotton() {
    var logContent = document.getElementById('terminal_dns_error');
    logContent.scrollTop = logContent.scrollHeight;
}

var previousLogContent = '';
// Função para obter a saída do terminal durante a execução dos bloqueios
function updateLogContent() {
    // Utilizando o AJAX para obter os dados
    fetch('/bloqueio_dns_log')
        .then(response => response.text())
        .then(data => {
            data = data.replace(/\n/g, '<br>');
            // Atualizando o conteudo do log no HTML
            // Veirifica se teve alteração no conteudo do log, caso tenha, cola o scroll em baixo para acompanhar as novas linhas
            if (data !== previousLogContent) {
                document.getElementById('terminal_dns_error').innerHTML = data;
                scrollToBotton();

                previousLogContent = data;
            }

                document.getElementById('terminal_dns_error').style.height = '550px';
        })
        .catch(error => {
            console.error('Erro ao obter retorno do terminal:', error);
        });
}

// Atualizando a cada 1 segundo o conteudo de execução
setInterval(updateLogContent, 1000);
