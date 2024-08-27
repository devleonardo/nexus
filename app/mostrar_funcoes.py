from app.config import *
from flask import session, request, Blueprint, jsonify
from ldap3 import Server, Connection, SIMPLE, ALL, SUBTREE

app = Blueprint('mostrar_funcoes', __name__)

@app.route('/mostrar_funcoes', methods=['GET', 'POST'])
def mostrar_funcoes(username):
    # OBTEM O NOME DE USUARIO DA SESSÃO
    usernameLST = session.get('usernameLST')
    passwordLST = session.get('passwordLST')

    if request.method == 'POST':
        
        # Otém o usuário de origem para copiar funções
        data = request.get_json()
        originUser = data.get('usuarioOrigem')

        # RECUPERA OS DETALHES DO USUARIO DO SERVIDOR LDAP
        server = Server(LDAP_HOST, use_ssl=True, get_info=ALL)
        conn = Connection(server, f"{usernameLST}{INTRANET}", password=passwordLST, authentication=SIMPLE, auto_bind=True)
        
        # RECUPERA OS DETALHES DO USUARIO DO SERVIDOR LDAP
        search_filter = f'(sAMAccountName={originUser})'
        conn.search(LDAP_BASE_DN, search_filter, attributes=['physicalDeliveryOfficeName','employeeID', 'ipPhone', 'initials','sn','givenName','ou','cn','name', 'mail', 'displayName', 'description', 'sAMAccountName', 'userPrincipalName', 'memberOf', 'userAccountControl', 'distinguishedName', 'objectCategory', 'whenCreated', 'badPasswordTime', 'badPwdCount', 'lastLogoff', 'lastLogon', 'logonCount', 'pwdLastSet', 'whenCreated', 'whenChanged', 'accountExpires'])

        # LISTA OS GRUPOS DE PERMISSÕES DO USUÁRIO
        group_conn = Connection(server, user=LDAP_USER_CN, password=LDAP_USER_PASSWORD, authentication=SIMPLE, auto_bind=True)
        group_conn.search(LDAP_BASE_DN, '(objectClass=group)', search_scope=SUBTREE, attributes=['cn'])

        # RECUPERA OS ATRIBUTOS DOS USUARIOS
        entry = conn.entries[0]
        user_attributes = entry.entry_attributes_as_dict

        member_of = user_attributes.get('memberOf', ['']) # GRUPO DE PERMISSÕES DO USUÁRIO

        # LISTANDO GRUPOS DE PERMISSÕES
        originGroups = []
        for group in member_of:
            group_name = group.split(',')[0]
            originGroups.append(group_name.split('=')[1])

        return jsonify({"grupos": originGroups, "origem": originUser})