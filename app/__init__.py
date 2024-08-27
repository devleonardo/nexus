from app.config import *
from flask import Flask, render_template, request, redirect, Blueprint, session, flash
from ldap3 import Server, Connection, SIMPLE, ALL, Attribute, Entry
from flask_session import Session
import subprocess

# INICIA A APLICAÇÃO
app = Flask(__name__)
app.secret_key = '{LDAP_USER_PASSWORD}'

# CONFIGURA A SESSÃO PARA USAR O ARMAZENAMENTO DO SISTEMA DE ARQUIVOS
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

def ldap_authenticate(username, password):
    # CRIA UM OBJETO DE SERVIDOR COM AS INFORMAÇÕES DE CONEXÃO
    server = Server(LDAP_HOST, use_ssl=True ,get_info=ALL)

    # CRIA UMA CONEXÃO COM O SERVIDOR LDAP
    conn = Connection(server, user=LDAP_USER_CN, password=LDAP_USER_PASSWORD, authentication=SIMPLE, auto_bind=True)

    # FAZ UMA BUSCA NO LDAP PARA ENCONTRAR A ENTRADA DO USUARIO E SE ELE FAZ PARTE DE ACESSO
    search_filter = f'(&(objectClass=user)(sAMAccountName={username})(|(memberOf={LDAP_GROUP_DN})(memberOf={LDAP_GROUP_DN2})))'
    conn.search(LDAP_BASE_DN, search_filter)

    # VERIFICA SE A ENTRADA DO USUARIO FOI ENCONTRADA
    if conn.entries:
        entry = conn.entries[0]

        # TENTA AUTENTICA O USUARIO COM A SENHA FORNECIDA
        conn = Connection(server, user=entry.entry_dn, password=password, authentication=SIMPLE)

        if conn.bind():

            # FAZ UMA BUSCA LDAP PARA OBTER OS ATRIBUTOS DE ENTRADA DO USUÁRIO
            conn.search(entry.entry_dn, '(objectclass=*)', attributes=['cn', 'mail', 'displayName', 'description', 'givenName', 'userPrincipalName', 'memberOf'])
            if conn.entries:
                user_attributes = conn.entries[0].entry_attributes_as_dict

                # LISTA OS ATRIBUTOS DO USUÁRIO QUE ESTA LOGANDO
                first_name = user_attributes.get('givenName', [''])[0]
                user_id = user_attributes.get('userPrincipalName', [''])[0]
                displayName = user_attributes.get('displayName', [''])[0]
                description = user_attributes.get('description', [''])[0]
                mail = user_attributes.get('mail', [''])[0]
                grupo = user_attributes.get('memberOf', [''])

                # FILTRA OS DADOS DOS ATRIBUTOS PARA UMA MELHOR VISUALIZAÇÃO
                userName = user_id.split('@')[0]
                domain = user_id.split('@')[1]
                group = subprocess.getoutput(f"less {grupo} | awk -F '=' '{{print $2}}' | awk -F ',' '{{print $1}}'")
                groupps = group.split()

                # ARMAZENA NA SESSÃO AS INFORMAÇÕES DO USUÁRIO LOGADO
                session['first_name'] = first_name
                session['userName'] = userName
                session['displayName'] = displayName
                session['description'] = description
                session['mail'] = mail
                session['domain'] = domain
                session['groupps'] = groupps

            # A AUTENTICAÇÃO FOI BEM SUCEDIDA
            return True

# TENTA LOGAR COM AS INFORMAÇÕES INFORMADAS NA TELA DE LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        # RECEBE NA TELA DE LOGIN AS INFORMAÇÕES DE ACESSO
        usernameLST = request.form['username']
        passwordLST = request.form['password']

        if ldap_authenticate(usernameLST, passwordLST):
            # ARMAZENA O NOME DE USUÁRIO NA SESSÃO
            session['usernameLST'] = usernameLST
            session['passwordLST'] = passwordLST

            # GUARDA A SESSÃO DO USUÁRIO QUANDO LOGADO
            session['logged_in'] = True

            # LOG DE CONEXÃO DO USUÁRIO
            logger.info(f"Logado como: {usernameLST}")

            # REDIRECIONA PARA A HOME
            return redirect('home')
        else:
            # RETORNA UMA MENSAGEM CASO O USUÁRIO NÃO TENHA ACESSO OU INFORME OS DADOS ERRADOS
            logger.info(f"Erro ao logar como: {usernameLST}")
            error_message = "Verifique se digitou corretamente o nome de usuário e senha ou contate um administrador do sistema."
            flash(error_message, 'error')
            return render_template('login.html')
    else:
        # RENDERIZA A TELA DE LOGIN
	    return render_template('login.html')

# RENDERIZA A PAGINA DE LOGIN EM DUAS ROTAS / E /LOGIN (AO RETORNAR ERRO NO LOGIN, A PÁGINA É REDIRECIONADA PARA /LOGIN)
@app.route('/')
@app.route('/login')
def index():
    if session.get('logged_in'):
        return redirect('/home')
    else:
        return render_template('login.html')

# REMOVE O LOGIN DA SESSÃO DO USUÁRIO
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return render_template('login.html')

# IMPORTA E REGISTRA O BLUEPRINT

# DASHBOARD DE MONITORAMENTO DNS/DOMINIO
from app.detector import app as detector_app
app.register_blueprint(detector_app)

# TESTE DE DOMÍNIO ESPECIFICO
from app.rdns import app as rdns_app
app.register_blueprint(rdns_app)

# BUSCA DE USUÁRIOS E ESTAÇÕES
from app.busca import app as busca_app
app.register_blueprint(busca_app)

# DASHBOARD PAINEL TIC (DADOS DO AD)
from app.painel import app as painel_app
app.register_blueprint(painel_app)

# PAGINA DE ENTRADA
from app.home import app as home_app
app.register_blueprint(home_app)

# PÁGINA DE LOG
from app.audit import app as audit_app
app.register_blueprint(audit_app)

# PÁGINA DE VERSÃO
from app.versao import app as versao_app
app.register_blueprint(versao_app)

#  BLOQUEIO DNS
from app.bloqueio_dns import app as bloqueio_dns_app
app.register_blueprint(bloqueio_dns_app)

# PERMISSÃO DNS
from app.permissao_dns import app as permissao_dns_app
app.register_blueprint(permissao_dns_app)

# LOG DO BLOQUEIO_DNS
from app.bloqueio_dns_log import app as bloqueio_dns_log_app
app.register_blueprint(bloqueio_dns_log_app)

# CONFIRMAR ENVIO DE FORMULARIO PARA TORNAR O TERMINAL DE LOG ATIVO
from app.confirm_form import app as confirm_form_app
app.register_blueprint(confirm_form_app)

# PÁGINA DE ERRO E REVERSÃO DE CONFIGURAÇÃO DO BLOQUEIO DNS
from app.dns_block_error import app as dns_block_error_app
app.register_blueprint(dns_block_error_app)

# PÁGINA DE APONTAMENTO DNS
from app.apontamento_dns import app as apontamento_dns_app
app.register_blueprint(apontamento_dns_app)

# FUNÇÃO EXTERNA REVERSÃO DE ALTERAÇÃO EM DNS
from app.dns_revert import app as dns_revert_app
app.register_blueprint(dns_revert_app)

# FUNÇÃO EXTERNA DOMAIN BLOCK
from app.domain_block import app as domain_block_app
app.register_blueprint(domain_block_app)

# FUNÇÃO EXTERNA DOMAIN FORWARD
from app.domain_forward import app as domain_forward_app
app.register_blueprint(domain_forward_app)

# FUNÇÃO EXTERNA FORWARD REVERT
from app.forward_revert import app as forward_revert_app
app.register_blueprint(forward_revert_app)

# PÁGINA QUE CRIA HOST NO ZABBIX
from app.host_zabbix import app as host_zabbix_app
app.register_blueprint(host_zabbix_app)

# PAGINA DO GERADOR SE SENHAS
from app.gerador_senhas import app as gerador_senhas_app
app.register_blueprint(gerador_senhas_app)

# PÁGINA DE PERMISSÃO PARA ACESSAR O MENU ZABBIX
from app.permissao_zabbix import app as permissao_zabbix_app
app.register_blueprint(permissao_zabbix_app)

# PÁGINA PARA MUDAR WALLPAPER DOS ADS
from app.adwall import app as adwall_app
app.register_blueprint(adwall_app)

# PÁGINA PARA ACESSAR O GLPI
from app.glpi import app as glpi_app
app.register_blueprint(glpi_app)

#CONSULTA DE FABRICANTE DE MAC ADDRESS
from app.busca_mac import app as busca_mac_app
app.register_blueprint(busca_mac_app)

# RETORNA OS GRUPOS DO USUÁRIO
from app.mostrar_funcoes import app as mostrar_funcoes_app
app.register_blueprint(mostrar_funcoes_app)

# CLONA OS GRUPOS DE UM USUÁRIO PARA O OUTRO
from app.clonar_grupos import app as clonar_grupos_app
app.register_blueprint(clonar_grupos_app)

#CÁLCULO DE SUBREDES
from app.subnet import app as subnet_app
app.register_blueprint(subnet_app)

# PÁGINA DE CRIAÇÃO DE GRUPOS
from app.create_group import app as create_group_app
app.register_blueprint(create_group_app)

# PÁGINA DE BUSCA DE URL BLOQUEADO
from app.busca_url import app as busca_url_app
app.register_blueprint(busca_url_app)

# PÁGINA DE RELATÓRIO DE PONTO 
from app.ponto_grd import app as ponto_grd_app
app.register_blueprint(ponto_grd_app)

# PÁGINA DE busca no radius
from app.busca_radius import app as busca_radius_app
app.register_blueprint(busca_radius_app)

#PÃGINA DE BUSCA POR IP NO RADIUS
from app.busca_radiusIP import app as busca_radiusIP_app
app.register_blueprint(busca_radiusIP_app)

# PÁGINA DE busca DO FREEIPA
from app.freeipa_servers import app as freeipa_servers_app
app.register_blueprint(freeipa_servers_app)

# PÁGINA DE CONSULTA DE STATUS IX.BR 
from app.statusIX import app as statusIX_app
app.register_blueprint(statusIX_app)

# PÁGINA DE CONSULTA DE STATUS IX.BR 
from app.statusCS import app as statusCS_app
app.register_blueprint(statusCS_app)

# PAGINA DE DESBLOQUIO DE DOMINIOS
from app.dns_desblock import app as dns_desblock_app
app.register_blueprint(dns_desblock_app)