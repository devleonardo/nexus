from flask import Flask, render_template, request, Blueprint, redirect, url_for, session, flash
import os
from pyzabbix.api import ZabbixAPI
import logging
from app.config import *

app = Blueprint('host_zabbix', __name__)

# VERIFICA SE HOUVE ALGUMA MODIFICAÇÃO DE PERMISSÃO E CARREGA OS USUÁRIOS PERMITIDOS###########
caminho_permissao = "permitido_zabbix.txt"
permitido = []
ultima_modificacao = 0

# CARREGA O ARQUIVO DE PERMISSÃO PARA ACESSAR A PÁGINA
def carregar_permitido():
    global ultima_modificacao
    ultima_modificacao_arquivo = os.path.getmtime(caminho_permissao)
    if ultima_modificacao_arquivo > ultima_modificacao:
        ultima_modificacao = ultima_modificacao_arquivo
        with open(caminho_permissao, 'r') as arquivo:
            permitido.clear()
            permitido.extend(arquivo.read().splitlines())
###############################################################################################

# LOG CASO HAJA ERRO NA CRIAÇÃO DO HOST, ESSE ERRO É MOSTRADO NA TELA
logging.basicConfig(filename='zabbix.log', level=logging.ERROR, filemode='w')
###############################################################################################

# RENDERIZA A HOME
@app.route('/host_zabbix', methods=['POST', 'GET'])
def host_zabbix():
    carregar_permitido()

    # OBTEM O NOME DE USUARIO DA SESSÃO
    usernameLST = session.get('usernameLST')

    # CHECA SE O USUÁRIO ESTÁ LOGADO, CASO CONTRÁRIO, REDIRECIONA PARA A PÁGINA DE LOGIN
    if not session.get('logged_in'):
        return render_template('login.html')
    
    # OBTÉM O NOME DE USUÁRIO DA SESSÃO
    usernameLST = session.get('usernameLST')

    # VERIFICA SE O USUARIO ESTÁ NA LISTA DE USUÁRIOS PERMITITDOS, CASO ESTEJA ACESSA, DO CONTRARIO EXIBE MENSAGEM DE FALTA DE PERMISSÃO
    if usernameLST in permitido:
       # RENDERIZA A CONEXÃO COM O SERVIDOR DO ZABBIX
       zapi = ZabbixAPI(url=zUrl, user=zUser, password=zPassword)

       # OBTÉM OS TEMPLATES EXISTENTES NO SERVIDOR DO ZABBIX E ARMAZENA EM UMA LISTA 
       templates = zapi.template.get(output='extend', selectInterfaces='extend')
       templates_list = [] 
       for template in templates:
           templates_list.append(f"Template: {template['name']}: {template['templateid']}")

       # OBTÉM OS GRUPOS EXISTENTES NO SERVIDOR DO ZABBIX E ARMAZENA EM UMA LISTA 
       grupos = zapi.hostgroup.get(output='extend') 
       grupos_list = []
       for grupo in grupos:
           grupos_list.append(f"Grupo: {grupo['name']}: {grupo['groupid']}") 
 
       if request.method == 'POST':
          zapi = ZabbixAPI(url=zUrl, user=zUser, password=zPassword)

          #OBTÉM OS VALORES ENVIADOS PELA FORMULARIO  
          novo_host = request.form.get('novo_host')
          novo_ip = request.form.get('novo_ip')
          tipo_conexao = request.form.get('tipo_conexao')
          novo_grupo = request.form.getlist('novo_grupo')
          novos_templates = request.form.getlist('novos_templates')
          descricao = request.form.get('descricao')
          macros = request.form.get('macros')

          # VERIFICA SE EXISTE ALGUM TEXTO NO TEXTAREA, CASO NÃO HAJA, PULA A CONFIGURAÇÃO DA MACRO  
          if not macros:
              pass
          else:
            macros_array = [line.strip() for line in macros.split('\n')]
            macros_list = [{'macro': '{$SNMP_COMMUNITY}', 'value': macro_value} for macro_value in macros_array]

          # VERIFICA QUAL FOI O TIPO DE CONEXÃO SELECIONADO E APÓS ISSO TOMA O CAMINHO BASEADO NA ESCOLHA PARA
          # PREENCHER O TEMPLATE DE CRIAÇÃO DO HOST  
          if tipo_conexao == '2':
              version = 1
          elif tipo_conexao == '21':
              version = 2
          elif tipo_conexao == '22':
              version = 3      
 
          if tipo_conexao == '1':
            new_host = {
                'host': f'{novo_host}',
                'interfaces': [{
                    'type': 1,
                    'main': 1,
                    'useip': 1,
                    'ip': f'{novo_ip}',
                    'dns': '',
                    'port': '10050'
                }],
                'groups': [{'groupid': group_id} for group_id in novo_grupo],
                'templates': [{'templateid': template_id} for template_id in novos_templates],
                'description': f'{descricao}'
            }
              
          elif tipo_conexao in ['2', '21', '22']:
              new_host = {
                'host': f'{novo_host}',
                'interfaces': [{
                    'type': 2,
                    'main': 1,
                    'useip': 1,
                    'ip': f'{novo_ip}',
                    'dns': '',
                    'port': '161',
                    'details': {
                        'version': f'{version}',
                        'community': '{$SNMP_COMMUNITY}'
                    }
                }],
                'groups': [{'groupid': group_id} for group_id in novo_grupo],
                'templates': [{'templateid': template_id} for template_id in novos_templates],
                'description': f'{descricao}',
                'macros': macros_list
            }
          # TENTA REALIZAR A CRIAÇÃO DO HOST COM AS INFORMAÇÕES INSERIDAS, CASO NÃO OCORRA ERRO, EXIBE MENSAGEM DE SUCESSO  
          try:
            zapi.host.create(new_host)
            zapi.user.logout()
            flash('Host criado!', 'success')
            logger.info(f"Usuário {usernameLST} criou o host {novo_host} no Zabbix.")

            return render_template('host_zabbix.html', templates_list=templates_list, grupos_list=grupos_list)
          
          # CASO HAJA ERRO, EXIBE A MENSAGEM DE ERRO NA TELA
          except Exception as e:
            error_message = str(e)

            # FAZ O TRATAMENTO DOS DADOS DO JSON GERADO NO ERRO PARA OBTER SOMENTO O CODIGO E A MENSAGEM
            json_index = error_message.find("'json':")

            if json_index != -1:
               error_message = error_message[:json_index]
            flash(error_message, 'error')
            return render_template('host_zabbix.html', templates_list=templates_list, grupos_list=grupos_list, error_message=error_message)

    # CASO NÃO TENHA PERMISSÃO PARA ACESSAR A PÁGINA, EXIBE MENSAGEM DE PERMISSÃO NEGADA
    else:
      flash('Você não tem permissão de acesso!', 'error')
      return redirect(request.referrer)

    # SE TIVER PERMISSÃO, RENDERIZA A PÁGINA NORMALMENTE
    return render_template('host_zabbix.html', templates_list=templates_list, grupos_list=grupos_list)