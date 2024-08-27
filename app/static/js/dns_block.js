function verificarValor() {
// Faça uma solicitação para o endpoint '/confirm_form'
fetch('/confirm_form')
    .then(response => response.text())
    .then(data => {
    // Verifica se o valor retornado é diferente de '0'
    if (data.trim() == '1') {
        // Modifica o estilo da div 'log-content'
        document.getElementById('log-content').style.display = 'inline-block';
        document.getElementById('dnsAguardando').style.display = 'none';
    }   
    else if (data.trim() == '0'){
        document.getElementById('log-content').style.display = 'none'
        }   
    else {
        window.location.href = "dns_block_error"
    }
    })
    .catch(error => {
    console.error('Erro na solicitação: ' + error);
    });
}

  // Executa a função verificarValor a cada 1 segundo (1000 milissegundos)
  setInterval(verificarValor, 1000);


// Função para forçar o scroll acompanhar as novas linhas
function scrollToBotton() {
    var logContent = document.getElementById('log-content');
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
                document.getElementById('log-content').innerHTML = data;
                scrollToBotton();

                previousLogContent = data;
            }

                document.getElementById('log-content').style.height = '360px';
        })
        .catch(error => {
            console.error('Error fetching log content:', error);
        });
}

// Atualizando a cada 2 segundos o conteudo de execução
setInterval(updateLogContent, 1000);