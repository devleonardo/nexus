from flask import Flask, render_template, request, redirect, url_for, Blueprint, session, flash
from ldap3 import Server, Connection, SIMPLE, ALL, Attribute, MODIFY_REPLACE, Entry, NTLM
from app.config import *
from flask_session import Session

app = Blueprint('painel', __name__)

@app.route('/painel', methods=['POST', 'GET'])
def painel():

    ## VERIFICA SE O URUÁRIO ESTA LOGADO, CASO CONTRÁRIO, ELE RETORNA PARA A PÁGINA DE LOGIN
    if not session.get('logged_in'):
        return render_template('login.html')
    
    # OBTEM O NOME DE USUARIO DA SESSÃO
    usernameLST = session.get('usernameLST')
    passwordLST = session.get('passwordLST')

    # FAZ A CONEXÃO COM OS DADOS DO USUARIO DA SESSÃO
    server = Server(LDAP_HOST, use_ssl=True, get_info=ALL)
    conn_auth = Connection(server, user=f"{usernameLST}{INTRANET}", password=passwordLST, authentication=SIMPLE, auto_bind=True)

    # VERIFICA SE O USUARIO PERTENCE AO GRUPO DE GERENCIA PARA OBTER AS INFORMAÇÕES
    search_filter = f'(&(sAMAccountName={usernameLST})(memberOf={LDAP_GROUP_DN}))'
    conn_auth.search(LDAP_BASE_DN, search_filter, attributes=['sAMAccountName'])

##############################################################################################
# TOTAL DE USUÁRIO NO AD
##############################################################################################
    conn = Connection(server, user=f"{usernameLST}{INTRANET}", password=passwordLST, authentication=SIMPLE, auto_bind=True)

    # DEFINE O TAMANHO DA PAGINA PARA UM VALOR MAIOR DO QUE O NUMERO TOTAL DE USUARIO
    page_size = 2000

    # REALIZA A BUSCA DOS USUARIOS NO SERVIDOR LDAP COM O TAMANHO DA PAGINA AJUSTADO
    search_filter_user = f'(&(objectClass=Person))'
    conn.search(LDAP_BASE_DN, search_filter_user, attributes=['sAMAccountName'], paged_size=page_size)

    # OBTEM OS RESULTADOS INICIAIS
    entries = conn.entries

    # VERIFICA SE HÁ MAIS PAGINAS DE RESULTADOS
    cookie = conn.result['controls']['1.2.840.113556.1.4.319']['value']['cookie']
    while cookie:
        # OBTEM A PROXIMA PAGINA DE RESULTADOS
        conn.search(LDAP_BASE_DN, search_filter_user, attributes=['sAMAccountName'], paged_size=page_size, paged_cookie=cookie)
        entries.extend(conn.entries)

        # ATUALIZA OS COOKIES PARA A PROXIMA PAGINA
        cookie = conn.result['controls']['1.2.840.113556.1.4.319']['value']['cookie']

    # OBTEM O NUMERO TOTAL DE USUARIO
    numero_usuarios = len(entries)

##############################################################################################
# TOTAL DE ESTAÇÕES
##############################################################################################

    # REALIZA A BUSCA DOS COMPUTADORES NO SERVIDOR
    search_filter_computadores = f'(&(objectClass=computer))'
    conn.search(LDAP_BASE_DN, search_filter_computadores, attributes=['name'])
    # OBTEM O NUMERO DE COMPUTADORES
    numero_computadores = len(conn.entries)

##############################################################################################
# TOTAL DE OUS
##############################################################################################

    # REALIZA A BUSCA DAS UNIDADES ORGANIZACIONAIS NO SERVIDOR
    search_filter_unidades = f'(&(objectClass=organizationalUnit))'
    conn.search(LDAP_BASE_DN, search_filter_unidades, attributes=['name'])
    # OBTEM O NUMERO DE UNIDADES ORGANIZACIONAIS
    numero_unidades = len(conn.entries)

##############################################################################################
# TOTAL DE GRUPOS
##############################################################################################

    # REALIZA A BUSCA DOS GRUPOS NO SERVIDOR
    search_filter_group = f'(&(objectClass=group))'
    conn.search(LDAP_BASE_DN, search_filter_group, attributes=['cn'])
    # OBTEM O NUMERO DE GRUPOS
    numero_grupos = len(conn.entries)

##############################################################################################
# TOTAL DE USUARIO BLOQUEADOS
##############################################################################################

    # REALIZA A BUSCA DOS USUÁRIO BLOQUEADOS
    search_filter_usuarios_bloqueados = f'(&(objectClass=user)(userAccountControl:1.2.840.113556.1.4.803:=2))'
    conn.search(LDAP_BASE_DN, search_filter_usuarios_bloqueados, attributes=['sAMAccountName'])
    # OBTEM O NUMERO DE USUARIO BLOQUEADOS
    numero_usuarios_bloqueados = len(conn.entries)

##############################################################################################
# TOTAL DE USUARIO ATIVOS
##############################################################################################

    # REALIZA A BUSCA DE USUARIO ATIVOS
    search_filter_usuarios_ativos = f'(&(objectClass=user)(!(userAccountControl:1.2.840.113556.1.4.803:=2)))'
    conn.search(LDAP_BASE_DN, search_filter_usuarios_ativos, attributes=['sAMAccountName'])
    # OBTEM O NUMERO DE USUARIO ATIVOS
    numero_usuarios_ativos = len(conn.entries)

##############################################################################################
# TOTAL DE CONTROLADORES DE DOMINIOS
##############################################################################################

    # REALIZA A BUSCA POR CONTRALADORES DE DOMINIOS
    search_filter_domainController = f'(&(objectClass=computer)(primaryGroupID=516))'
    conn.search(LDAP_BASE_DN, search_filter_domainController, attributes=['cn', 'primaryGroupID'])
    # OBTEM O NUMERO DE CONTROLADORES DE DOMINIOS
    numero_controlador_dominio = len(conn.entries)

##############################################################################################
# CONTROLE DE ACESSO AO PAINEL TI
##############################################################################################

    # SE O USUARIO PERTENCER AO GRUPO, RENDERIZA A PAGINA DE BUSCA
    if len(conn_auth.entries) > 0:
        return render_template('painel.html', numero_controlador_dominio=numero_controlador_dominio, numero_usuarios_ativos=numero_usuarios_ativos, numero_usuarios_bloqueados=numero_usuarios_bloqueados, numero_usuarios=numero_usuarios, numero_computadores=numero_computadores, numero_unidades=numero_unidades, numero_grupos=numero_grupos)
    else:
        # CASO CONTRARIO, REDIRECIONA PARA A DE ALERTA
        flash('Você não tem permissão de acesso!', 'error')
        return redirect(request.referrer)