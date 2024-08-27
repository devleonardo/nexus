from app.config import *
from flask import render_template, request, redirect, flash, url_for, Blueprint, session
from ldap3 import Server, Connection, SIMPLE, ALL, MODIFY_REPLACE, ALL_ATTRIBUTES
import subprocess
from app.verificador import group_verification
from app.user_details import user_details
from app.block_user import block_user
from app.ad_remove import ad_remove
from app.reset_password import reset_password
from app.create_user import create_user
from app.edit_groups import edit_groups
from app.mostrar_funcoes import mostrar_funcoes
from app.clonar_grupos import clonar_grupos

app = Blueprint('busca', __name__)

# ROTA DE BUSCA PARA USUARIO DESLOGADO, RETORNA A PAGINA DE LOGIN
@app.route('/busca')
def searchPage():
    # CHECA SE O USUÁRIO ESTÁ LOGADO, CASO CONTRÁRIO, REDIRECIONA PARA A PÁGINA DE LOGIN
    result = group_verification()
    if result == True:
        pass
    else:
        return result

    return render_template('busca.html')

# REALIZA A BUSCA DO USUÁRIO OU ESTAÇÃO
@app.route('/busca', methods=['GET', 'POST'])
def search_users():

    # CHECA SE O USUÁRIO ESTÁ LOGADO, CASO CONTRÁRIO, REDIRECIONA PARA A PÁGINA DE LOGIN
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    # OBTÉM O NOME DE USUÁRIO DA SESSÃO
    usernameLST = session.get('usernameLST')
    passwordLST = session.get('passwordLST')

    if request.method == 'POST':
        # RECEBE A REQUISIÇÃO DO FORMULÁRIO
        search_query = request.form['search_query']
        
        # REALIZAR A BUSCA DO USUÁRIO NO SERVIDOR
        server = Server(LDAP_HOST, use_ssl=False, get_info=ALL)
        conn = Connection(server, user=LDAP_USER_CN, password=LDAP_USER_PASSWORD, authentication=SIMPLE, auto_bind=True)
        search_filter = f'(&(objectClass=user)(|(sAMAccountName=*{search_query}*)(displayName=*{search_query}*)(mail=*{search_query}*)(memberOf=*{search_query}*)))'
        conn.search(LDAP_BASE_DN, search_filter, attributes=['displayName', 'objectCategory', 'description', 'sAMAccountName', 'userPrincipalName','userAccountControl'])

        # USUÁRIO QUE ESTA REALIZANDO A PESQUISA NA BASE DE DADOS DO AD
        logger.info(f"{usernameLST} pesquisou por: {search_query}")

        # ARMAZENA OS RESULTADOS DA PESQUISA EM UMA LISTA
        search_results = []
        for entry in conn.entries:
            user_attributes = conn.entries[0].entry_attributes_as_dict

            # LISTA OS TIPOS
            type = entry.objectCategory.value

            # REMOVE OS SEPARADORES 
            types = subprocess.getoutput(f"less {type} | awk -F '=' '{{print $2}}' | awk -F ',' '{{print $1}}'")

            # NOME DE USUÁRIO
            username = entry.sAMAccountName.value

            # NOME COMPLETO
            display_name = entry.displayName.value if 'displayName' in entry else ''

            # CARGO
            description = entry.description.value if 'description' in entry else ''

            # STATUS DA CONTA = ATIVADO OU DESATIVADO
            account_status = entry.userAccountControl.value if 'userAccountControl' in entry else ''

            # VERIFICA O VALOR DA CONTA E RETORNA O STATUS
            if account_status == 514:
                statusAccount = "DESATIVADO"
            elif account_status == 66050:
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
        return render_template('busca.html', search_results=search_results)
    
    # RENDERIZA A PÁGINA DE BUSCA
    return render_template('busca.html')

# FUNÇÃO CRIAR USUÁRIO SENDO CHAMADA EXTERAMENTE
@app.route('/<username>/create_user', methods=['GET', 'POST'])
def create_user_f(username):
    return create_user(username)

# FUNÇÃO USER DETAILS SENDO CHAMADA EXTERNAMENTE
@app.route('/busca/<username>', methods=['GET', 'POST'])
def show_user_details(username):
    return user_details(username)

# MOSTRAR FUNCOES DO USUARIO QUE SERÁ TERÁ PERMISSOES CLONADAS
@app.route('/<username>/mostrar_funcoes', methods=['POST', 'GET'])
def mostrar_funcoes_f(username):
    return mostrar_funcoes(username)

# FUNÇÃO APRA CLONAR GRUPOS DO USUARIO
@app.route('/<username>/clonar_grupos', methods=['POST', 'GET'])
def clonar_grupos_f(username):
    return clonar_grupos(username)

# FUNÇÃO BLOCK USER SENDO CHAMADA EXTERNAMENTE
@app.route('/<username>/block', methods=['POST'])
def block_user_f(username):
    return block_user(username)

# FUNÇÃO AD REMOVE SENDO CHAMADA EXTERNAMENTE
@app.route('/<username>/remove', methods=['POST'])
def ad_remove_f(username):
    return ad_remove(username)

#####################################################################
#                             EM TESTE                              #
#####################################################################
######### FUNÇÃO RESET PASSWORD SENDO CHAMADA EXTERNAMENTE ##########
@app.route('/<username>/reset', methods=['POST'])
def reset_password_f(username):
    return reset_password(username)

# Função para editar grupos do usuário
@app.route('/<username>/edit_group', methods=['POST'])
def edit_groups_f(username):
    return edit_groups(username)