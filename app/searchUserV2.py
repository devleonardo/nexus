from app.config import *
from flask import render_template, request, redirect, url_for, Blueprint, session
from ldap3 import Server, Connection, SIMPLE, ALL, MODIFY_REPLACE, ALL_ATTRIBUTES
import subprocess

def searchUserV2():

    # CHECA SE O USUÁRIO ESTÁ LOGADO, CASO CONTRÁRIO, REDIRECIONA PARA A PÁGINA DE LOGIN
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    # VERIFICA SE É NECESSÁIRO O BOTÃO SCROLL UP
    upScroll = '1'

    # OBTÉM O NOME DE USUÁRIO DA SESSÃO
    usernameLST = session.get('usernameLST')
    passwordLST = session.get('passwordLST')
    CORPCallcenter = "CN=CORPCallcenter,OU=CORPORATIVO,DC=intranet,DC=leste"


    if request.method == 'POST':
        # CONFIRMA A ROTA SELECIONADA NA PÁGINA DE BUSCA, COM BASE NO GRUPO DO USUÁRIO NX_CALLSUP OU USERS_STI
        routeII = "confirmed"
        
        # RECEBE A REQUISIÇÃO DO FORMULÁRIO
        search_query = request.form['search_query']
        
        # REALIZAR A BUSCA DO USUÁRIO NO SERVIDOR
        server = Server(LDAP_HOST, use_ssl=False, get_info=ALL)
        conn = Connection(server, user=LDAP_USER_CN, password=LDAP_USER_PASSWORD, authentication=SIMPLE, auto_bind=True)
        search_filter = f'(&(objectClass=user)(memberOf={CORPCallcenter})(|(sAMAccountName=*{search_query}*)(displayName=*{search_query}*)(mail=*{search_query}*)))'
        conn.search(LDAP_BASE_DN, search_filter, attributes=['displayName', 'objectCategory', 'description', 'sAMAccountName', 'userPrincipalName','userAccountControl'])

        # USUÁRIO QUE ESTA REALIZANDO A PESQUISA NA BASE DE DADOS DO AD
        logger.info(f"{usernameLST}, pesquisou por: {search_query}.")

        # ARMAZENA OS RESULTADOS DA PESQUISA EM UMA LISTA
        search_results = []
        for entry in conn.entries:
            user_attributes = entry.entry_attributes_as_dict

            # LISTA OS TIPOS
            type = user_attributes.get('objectCategory', [''])[0]

            # REMOVE OS SEPARADORES 
            types = subprocess.getoutput(f"less {type} | awk -F '=' '{{print $2}}' | awk -F ',' '{{print $1}}'")

            # NOME DE USUÁRIO
            username = user_attributes.get('sAMAccountName', [''])[0]

            # NOME COMPLETO
            display_name = user_attributes.get('displayName', [''])[0]

            # CARGO
            description = user_attributes.get('description', [''])[0]

            # STATUS DA CONTA = ATIVADO OU DESATIVADO
            account_status = user_attributes.get('userAccountControl', [0])[0]

            # VERIFICA O VALOR DA CONTA E RETORNA O STATUS
            if account_status == 514 or account_status == 66050:
                statusAccount = "DESATIVADO"
            else:
                statusAccount = "ATIVO"

            # VERIFICA O TIPO DE CONTA
            if types == 'Person':
                typesAccount = "Usuário"
                check_type  = "1"
            else:
                typesAccount = "Estação"
                check_type = "0"

            # ACRESCENTA AS INFORMAÇÕES BUSCADAS
            search_results.append((username, display_name, description, statusAccount, typesAccount))
        # RENDERIZA A PAGINA DE BUSCA COM AS INFORMAÇÕES LISTADAS ACIMA
        return render_template('busca.html', search_results=search_results, routeII=routeII, upScroll=upScroll)
    
    # RENDERIZA A PÁGINA DE BUSCA
    return render_template('busca.html')