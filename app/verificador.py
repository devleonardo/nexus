from flask import session, flash, render_template, request, redirect, url_for
from ldap3 import Server, Connection, SIMPLE, ALL
from app.config import *
from app.permissoes import *


# Função para verificar se usuário está logado ou se possui o grupo de acesso
def group_verification():

    # Obtém o nome de usuário e senha da sessão
    usernameLST = session.get('usernameLST')
    passwordLST = session.get('passwordLST')

    # Se não houver nome de usuário ou senha redireciona para a página de login
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
    
        # Obtém o nome da página onde o usuário está tentando acessar e armazena na var endpoint
        endpoint = request.endpoint.split('.')[0]

        # Obtém o array de permissão correspondente para o nome da página que está na var endpoint
        permisso_grupo = globals().get(endpoint)

        # Se houver apenas um grupo de permissão, cria o filtro de busca no AD de forma simples
        if len(permisso_grupo) == 1:
            search_filter = f'(&(sAMAccountName={usernameLST})(memberOf={permisso_grupo[0]}))'
        
        # Se houver mais de um grupo, cria o filtro composto
        else:
            group_filter = "".join([f"(memberOf={grupo})" for grupo in permisso_grupo])
            search_filter = f"(&(sAMAccountName={usernameLST})(|{group_filter}))"

            # Tenta executar a verificação dos grupos para o usuário e senha mencionado
        try:
            # VERIFICA SE O USUÁRIO PERTENCE AO GRUPO LDAP_GROUP_DN
            server = Server(LDAP_HOST, use_ssl=True, get_info=ALL)
            conn = Connection(server, user=f"{usernameLST}{INTRANET}", password=passwordLST, authentication=SIMPLE, auto_bind=True)

            conn.search(LDAP_BASE_DN, search_filter, attributes=['sAMAccountName'])

            # SE O USUÁRIO PERTENCER AO GRUPO, RENDERIZA A PÁGINA
            if len(conn.entries) > 0:
                return True
            # CASO CONTRÁRIO, REDIRECIONA PARA A PÁGINA DE ORIGEM DA REQUISIÇÃO
            else:
                flash('Você não tem permissão de acesso!', 'error')
                return redirect(request.referrer)
        except:
            flash('Erro inesperado. Tente novamente mais tarde.', 'error')
            return render_template('login.html')
                