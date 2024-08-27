from app.config import *
from flask import Flask, render_template, request, Blueprint, redirect, url_for, session, flash
import os
import logging
import datetime
from app.domain_block import domain_block
from app.dns_revert import dns_revert
from app.att_anablock import att_anablock

app = Blueprint('bloqueio_dns', __name__)

# LOG PARA SER EXIBIDO A SAIDA DO TEMPLATE NA PAGINA DE BLOQUEIO DNS ############################
logger = logging.getLogger('bloqueio_dns')
logger.setLevel(logging.DEBUG)

handler = logging.FileHandler('bloqueio_dns.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)
#################################################################################################

# DESTINO E VALORES DA VARIAVEL QUE ATIVA OU DESATIVA O TERMINAL NO MOMENTO DA EXECUÇÃO DO BLOQUEIO #

# terminal ativo = 1, terminal inativo = 0, redirecionamento pós conclusão = 2
destino_terminal = 'confirmacao_dns_block.txt'
confirmacao_dns_block = '1'
confirmacao_pos_block = '0'
confirmacao_redirect = '2'
################################################################################################

# FUNÇÃO QUE VERIFICA SE HOUVE ALTERAÇÃO NO ARQUIVO PERMITIDOS, SE HOUVER É ATUALIZADO O ACESSO #

# Arquivo permitidos contém os usuários que tem permissão para acessar qualquer página do menu DNS #
caminho_permissao = "permitido.txt"
permitido = []
ultima_modificacao = 0

def carregar_permitido():
    global ultima_modificacao
    ultima_modificacao_arquivo = os.path.getmtime(caminho_permissao)
    if ultima_modificacao_arquivo > ultima_modificacao:
        ultima_modificacao = ultima_modificacao_arquivo
        with open(caminho_permissao, 'r') as arquivo:
            permitido.clear()
            permitido.extend(arquivo.read().splitlines())
###############################################################################################

# FUNÇÃO DOMAIN BLOCK SENDO IMPORTADA ####################################################################################################
# Essa função realiza o bloqueio do domínio especificado
@app.route('/domain_block', methods=['POST', 'GET'])
def domain_block_f(grl02, mrc01, mrc02, rdns01, rdns02, rdns03, rdns04, rdns05, rdns06, sji01, sji02):
   return domain_block(grl02, mrc01, mrc02, rdns01, rdns02, rdns03, rdns04, rdns05, rdns06, sji01, sji02)
############################################################################################################################################

# FUNÇÃO REVERSÃO DE ALTERAÇÃO ##############################################################################################################
# Essa função realiza a reversão da última modificação realizada
@app.route('/dns_revert', methods=['POST', 'GET'])
def dns_revert_f(igrdns01, mrc01, mrc02, rdns01, rdns02, rdns03, rdns04, rdns05, rdns06, sji01, sji02):
   return dns_revert(igrdns01, mrc01, mrc02, rdns01, rdns02, rdns03, rdns04, rdns05, rdns06, sji01, sji02)
#############################################################################################################################################

# FUNÇÃO PARA ATUALIZAR ANABLOCK SENDO IMPORTADA
@app.route('/att_anablock', methods = ['POST'])
def att_anablock_f():
   return att_anablock()


# RENDERIZA A HOME ############################################################################
@app.route('/bloqueio_dns', methods=['POST', 'GET'])
def bloqueio_dns():
    carregar_permitido()
    # CHECA SE O USUÁRIO ESTÁ LOGADO, CASO CONTRÁRIO, REDIRECIONA PARA A PÁGINA DE LOGIN
    if not session.get('logged_in'):
        return render_template('login.html')

    # OBTÉM O NOME DE USUÁRIO DA SESSÃO
    usernameLST = session.get('usernameLST')

    if usernameLST in permitido:
      with open(destino_terminal, 'w') as confirmacao:
          confirmacao.write(confirmacao_pos_block)
#################################################################################################

# SE O VALOR DE REVERT NÃO FOR NONE, EXECUTA REVERSÃO, SE NÃO EXECUTA BLOQUEIO

      if request.method == 'POST':
         revert = request.form.getlist('REVERT')
         anablock = request.form.getlist('anablock')
         if anablock == 'anablock':
            with open(destino_terminal, 'w') as confirmacao:
               confirmacao.write(confirmacao_dns_block)
            att_anablock_f()
         elif not anablock:
            # No momento em que o formulário é acionado a variável do terminal passa para 1 = ativo #
            with open(destino_terminal, 'w') as confirmacao:
               confirmacao.write(confirmacao_dns_block)
      # OBTÉM A DATA NO MOMENTO EM QUE FOR EXECUTADO A AÇÃO PARA O LOG ################################
            agora = datetime.datetime.now()
            agora_formatado = agora.strftime("%d/%m/%Y")
      #################################################################################################

      # OBTÉM O TÍTULO DO E-MAIL QUE ORIGINOU A SOLICITAÇÃO DE BLOQUEIO ##############################
            titulo = request.form.get('titulo')
            titulo_comentado = f"# {titulo}"
            titulo_com_data = f"{agora_formatado} - {titulo}"
      #################################################################################################

      # ESCREVE A DATA E O TITULO DO EMAIL, QUE FOI INSERIDO NA INTERFACE WEB, NO LOG #################
            with open('bloqueio_dns.log', 'a') as log_file:
               log_file.write(titulo_com_data)
      #################################################################################################

      # REALIZA O TRATAMENTO DOS DADOS OBTIDOS NA INTERFACE WEB #######################################
            ip = request.form.get('ip')
            dominio = request.form.get('dominio')
            dominio_array = [line.strip() for line in dominio.split('\n')]

            # Destino das linhas que serão utilizadas no arquivo include para o blqoueio ############
            destino_linhas = "/home/usshd/Ansible/linhas.yml"

            #######################################################################################
            linhas_para = ""
            quebra_linha = "\n"

            # Realiza o tratamento dos dados recebidos e monta as linhas para o arquivo include ###        
            for dom in dominio_array:
                  # local_zone = f'local-zone: "{dom}" redirect'
                  # local_data = f'local-data: "{dom} A {ip}"'
                  # local_data2 = f'local-data: "{dom} AAAA ::1"'

                  local_zone = f'forward-zone:'
                  local_data = f'\t name: "{dom}"'
                  local_data2 = f'\t forward-addr: {ip}'

                  local_zone = f'local-zone: "{dom}" always_nxdomain'

                  linhas_para += local_zone + '\n'
                  # linhas_para += local_data + '\n'
                  # linhas_para += local_data2 + '\n'
                  linhas_para += '\n'
            ########################################################################################

            # Escreve as linhas no arquivo linhas.yml 
            with open(destino_linhas, 'w') as archive:
               archive.write(quebra_linha)
            
            with open(destino_linhas, 'a') as archive:
               archive.write(titulo_comentado) 

            with open(destino_linhas, 'a') as archive:
               archive.write(quebra_linha)

            with open(destino_linhas, 'a') as archive:
               archive.write(quebra_linha)

            with open(destino_linhas, 'a') as archive:
                  archive.write(linhas_para)
      ###################################################################################################
         # OBTÉM OS VALORES CASO O FORMULÁRIO SEJA ENVIADO ##############################################
            grl02 = request.form.getlist('GRL02')
            mrc01 = request.form.getlist('MRC01')
            mrc02 = request.form.getlist('MRC02')
            rdns01 = request.form.getlist('RDNS01')
            rdns02 = request.form.getlist('RDNS02')
            rdns03 = request.form.getlist('RDNS03')
            rdns04 = request.form.getlist('RDNS04')
            rdns05 = request.form.getlist('RDNS05')
            rdns06 = request.form.getlist('RDNS06')
            sji01 = request.form.getlist('SJI01')
            sji02 = request.form.getlist('SJI02')
         # CHAMA A FUNÇÃO DOMAIN BLOCK PARA EXECUTAR O BLOQUEIO
            domain_block(grl02, mrc01, mrc02, rdns01, rdns02, rdns03, rdns04, rdns05, rdns06, sji01, sji02)
         elif revert == 'revert':
         # ATIVA O TERMINAL NA INTERFACE WEB  
            with open(destino_terminal, 'w') as confirmacao:
               confirmacao.write(confirmacao_dns_block)

         # OBTÉM OS VALORES CASO O FORMULÁRIO SEJA ENVIADO ##############################################
            igrdns01 = request.form.getlist('IGRDNS01')
            grl02 = request.form.getlist('GRL02')
            mrc01 = request.form.getlist('MRC01')
            mrc02 = request.form.getlist('MRC02')
            rdns01 = request.form.getlist('RDNS01')
            rdns02 = request.form.getlist('RDNS02')
            rdns03 = request.form.getlist('RDNS03')
            rdns04 = request.form.getlist('RDNS04')
            rdns05 = request.form.getlist('RDNS05')
            rdns06 = request.form.getlist('RDNS06')
            sji01 = request.form.getlist('SJI01')
            sji02 = request.form.getlist('SJI02')

            # CHAMA A FUNÇÃO DNS REVERT PARA EXECUTAR A REVERSÃO
            dns_revert(grl02, mrc01, mrc02, rdns01, rdns02, rdns03, rdns04, rdns05, rdns06, sji01, sji02)

    # Caso não tenha permissão, será redirecionado para uma página de erro #############################################  
    else:
      flash('Você não tem permissão de acesso!', 'error')
      return redirect(request.referrer)
      #FINAL DA ACAO
    return render_template('bloqueio_dns.html')

