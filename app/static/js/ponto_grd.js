// Obtém a data atual
let data = new Date();
let ano = data.getFullYear();
let funcionario; // Variável para armazenar o nome do funcionário

// Função para determinar o último dia do mês com base no ano atual
function ultimo_dia() {
    let mes = document.getElementById("mes").value;
    // Verifica o número de dias para cada mês, considerando anos bissextos
    if (mes == 1 || mes == 3 || mes == 5 || mes == 7 || mes == 8 || mes == 10 || mes == 12) return 31;
    if (mes == 4 || mes == 6 || mes == 9 || mes == 11) return 30;
    if (mes == 2) if (ano % 400 == 0) return 29;
    if (mes == 2) if (ano % 100 == 0) return 28;
    if (mes == 2) if (ano % 4 == 0) return 29;
    else return 28;
}

// Função principal para criar a tabela da folha de ponto
function criartabela(funcionario, setorfuncionario, controle, empresa) {
    let mes = document.getElementById("mes").value;
    let ultimoDia = ultimo_dia();
    // Definições das empresas com seus detalhes de endereço e contato
    let empresa_group = "LESTE GROUP TELECOMUNICACOES DO BRASIL LTDA";
    let empresa_multi = "MULTI SERVICE SERVIÇO DE TECNOLOGIA E REDES LTDA";
    let empresa_tecnolab = "TECNOLAB CONSULTORIA E REDE LTDA";
    let empresa_solucoes = "LESTE SOLUCOES EM TI E SUPORTE TECNICO LTDA";
    let empresa_flu = "LESTE FLU SERVICOS DE TELECOM LTDA";
    
    let semana = ["Domingo", "Segunda-Feira", "Terça-Feira", "Quarta-Feira", "Quinta-Feira", "Sexta-Feira", "Sábado"];

    let mes_texto;
    if (mes == 1) { mes_texto = "Janeiro" } if (mes == 2) { mes_texto = "Fevereiro" } if (mes == 3) { mes_texto = "Março" }
    if (mes == 4) { mes_texto = "Abril" } if (mes == 5) { mes_texto = "Maio" } if (mes == 6) { mes_texto = "Junho" }
    if (mes == 7) { mes_texto = "Julho" } if (mes == 8) { mes_texto = "Agosto" } if (mes == 9) { mes_texto = "Setembro" }
    if (mes == 10) { mes_texto = "Outubro" } if (mes == 11) { mes_texto = "Novembro" } if (mes == 12) { mes_texto = "Dezembro" }

    // Abre uma nova janela para exibir a folha de ponto
    let novaJanela = window.open('', '_blank');

    novaJanela.document.write('<center>');

    // Função para gerar o cabeçalho da folha de ponto com informações da empresa
    function gerarFolhaDePonto(empresa, empresaNome, endereco, cep, atendimento, site, email, backgroundImg) {
        novaJanela.document.write('<center id="cabecalho"><p>' + empresaNome + '</p>');
        novaJanela.document.write('<p>' + endereco + '</p>');
        novaJanela.document.write('<p>CEP: ' + cep + '</p>');
        novaJanela.document.write('<p>Atendimento: ' + atendimento + '</p>');
        novaJanela.document.write('<p><u>' + site + '</u></p>');
        novaJanela.document.write('<p>e-mail: ' + email + '</p></center>');
        novaJanela.document.write('<style>#cabecalho{font-size: 14px; line-height: 0.5;}</style>');
        novaJanela.document.write('<center><p>_________________________________________________________________________</p></center>');
    }

    // Seleciona e exibe o cabeçalho correspondente à empresa selecionada
    if (empresa == "lestegroup") {
        gerarFolhaDePonto(empresa, empresa_group, "Rua Acacio Campos dos Santos S/N Quadra 4 Lote 17 18 19 e 20, Centro - Itaboraí - RJ", "24800-021", "(21) 2006-0967 ", "www.lestetelecom.com.br", "sac@lestetelecom.com.br", "leste.png");
    }
    if (empresa == "lestemulti") {
        gerarFolhaDePonto(empresa, empresa_multi, "Rua Valdemiro Jose Viana 361 Quadra 16 Lote 02, Aracatiba - Maricá - RJ", "24901-835", "(21) 2639-1338", "www.lestetelecom.com.br", "sac@lestetelecom.com.br");
    }
    if (empresa == "lestetecno") {
        gerarFolhaDePonto(empresa, empresa_tecnolab, "Avenida Vinte e Dois de Maio 4845 Sala 605, Rio Varzea - Itaboraí - RJ", "24812-086", "(21) 2006-0967", "www.lestetelecom.com.br", "sac@lestetelecom.com.br", "giga.jpg");
    }
    if (empresa == "lestesolucoes") {
        gerarFolhaDePonto(empresa, empresa_solucoes, "Rua Acacio Campos dos Santos S/N Quadra 12 Lote 01 02 e 22, Centro - Itaboraí - RJ", "24800-021", "(21) 2639-1338", "www.lestetelecom.com.br", "sac@lestetelecom.com.br");
    }
    if (empresa == "lesteflu") {
        gerarFolhaDePonto(empresa, empresa_flu, "Rua Joao Feliciano da Costa 207, Centro - Itaboraí, RJ", "24800-017", "(21) 2006-0967", "www.lestetelecom.com.br", "sac@lestetelecom.com.br");
    }
    
    // Escreve informações gerais na nova janela
    novaJanela.document.write('<p align="center">Nome: <b>' + funcionario + '</b></p>');
    novaJanela.document.write('<p align="center">Setor: <b>' + setorfuncionario + '</b></p>');
    novaJanela.document.write('<p align="center">Mês/Ano: <b>' + mes_texto + '/' + ano + '</b></p>');
    novaJanela.document.write('<style>h1{text-align: right; font-size: 45px;}</style>');
    novaJanela.document.write('<style>table{border-collapse: collapse;text-align: center;}table, td, th{border: 1px solid #000;}</style>');
    novaJanela.document.write('<table border="1" class="tabelaEditavel">');
    novaJanela.document.write('<td width="10">Dia</td>');
    novaJanela.document.write('<td width="150">Entrada</td>');
    novaJanela.document.write('<td width="300">Assinatura</td>');
    novaJanela.document.write('<td width="150">Saida</td>');
    novaJanela.document.write('<td width="300">Assinatura</td>');
    // Loop para preencher os dias do mês na tabela
    for (let x = 1; x <= ultimoDia; x++) {
        let data_corrente = x + "/" + mes + "/" + ano;
        let arr = data_corrente.split("/").reverse();
        let teste = new Date(arr[0], arr[1] - 1, arr[2]);
        let dia = teste.getDay();

        novaJanela.document.write('<tr>');
        novaJanela.document.write('<td>' + x + '</td>');

        if ((dia == 0 || dia == 6) && controle == "true") {
            novaJanela.document.write('<td bgcolor="#C0C0C0"></td>');
            novaJanela.document.write('<td bgcolor="#C0C0C0">' + semana[dia] + '</td>');//Primeiro campo assinatura
        } else {
            novaJanela.document.write('<td></td>');
            novaJanela.document.write('<td></td>');
        }

        if ((dia == 0 || dia == 6) && controle == "true") {
            novaJanela.document.write('<td bgcolor="#C0C0C0"></td>');
            novaJanela.document.write('<font color="red"><td bgcolor="#C0C0C0"' + semana[dia] + '</td></font>');//Primeiro campo assinatura
        } else {
            novaJanela.document.write('<td></td>')
            novaJanela.document.write('<td></td>');
        }
        novaJanela.document.write('</tr>')
    }
    novaJanela.document.write('</table>')
    novaJanela.document.write('</center>');
    // Configuração para impressão automática da folha de ponto após 1 segundo
    let delayMillis = 1000; //1 second

    setTimeout(function () {
        novaJanela.print();
    }, delayMillis);
    // Fecha a janela após a impressão
    novaJanela.onafterprint = function () {
        novaJanela.close();
    }
}

// Função para validar o formulário antes de gerar a folha de ponto
function gerar() {
    if (!validarFormulario()) {
        return;
    }

    let campo = document.getElementById('nome');
    let setor_funcionario = document.getElementById('setor');
    let empresa = document.querySelector('input[name="empresa"]:checked').value;
    let funcionario = campo.value;
    let setorfuncionario = setor_funcionario.value;
    let controle = document.querySelector('input[name="tipo"]').checked ? "true" : "false";
    criartabela(funcionario, setorfuncionario, controle, empresa);
}

// Função para validar se todos os campos do formulário estão preenchidos
function validarFormulario() {
    let nome = document.getElementById('nome').value.trim();
    let setor = document.getElementById('setor').value.trim();
    let mes = document.getElementById('mes').value;
    let empresaSelecionada = document.querySelector('input[name="empresa"]:checked');

    if (!nome || !setor || mes === "" || !empresaSelecionada) {
        alert("Por favor, preencha todos os campos antes de enviar.");
        return false;
    }

    return true;
}
