from flask import Flask, render_template, request, Blueprint, redirect, url_for, session, flash
from ldap3 import Server, Connection, SIMPLE, ALL, SUBTREE, MODIFY_ADD
from ldap3.core.exceptions import LDAPBindError
from app.verificador import group_verification
from app.config import *
import time

app = Blueprint('create_group', __name__)

# RENDERIZA A HOME
@app.route('/create_group', methods=['POST','GET'])
def search_group():
    # CHECA SE O USUÁRIO ESTÁ LOGADO, CASO CONTRÁRIO, REDIRECIONA PARA A PÁGINA DE LOGIN
    result = group_verification()
    if result == True:
        pass
    else:
        return result
    
    # OBTÉM O NOME DE USUÁRIO DA SESSÃO
    usernameLST = session.get('usernameLST')
    passwordLST = session.get('passwordLST')
    
    # CRIANDO A CONEXÃO PARA O LDAP3
    server = Server(LDAP_HOST, use_ssl=True, get_info=ALL)
    conn = Connection(server, user=f"{usernameLST}{INTRANET}", password=passwordLST, authentication=SIMPLE, auto_bind=True)

    # REALIZANDO BUSCA NO AD PARA VERIFICAR AS OUs DISPONÍVEIS
    conn.search(search_base=LDAP_BASE_DN,
        search_filter='(objectClass=organizationalUnit)',
        search_scope=SUBTREE,
        attributes=['ou']
    )

    ou_list = [entry.ou.value for entry in conn.entries]

    # OBTÉM OS GRUPOS DISPONÍVEIS DENTRO DA OU SELECIONADA
    if request.method == 'POST':
        # OBTENDO A OU SELECIONADA
        selected_ou = request.form.get('selected-ou')

        # MONTANDO O DN COMPLETO DA OU
        complete_ou = f"OU={selected_ou},DC=intranet,DC=leste"

        # MONTANDO O FILTRO DE BUSCA PELOS GRUPOS DENTRO DA OU
        search_filter = '(objectClass=group)'

        # ATRIBUTO QUE SERÁ RECUPERADO, NO CASO O DN QUE É O CAMINHO COMPLETO PRO GRUPO
        attributes = ['distinguishedName']

        # REALIZANDO A BUSCA
        conn.search(complete_ou, search_filter, attributes=attributes)

        # ARMAZENANDO OS GRUPOS ENCONTRADOS NA OU SELECIONADA
        groups_list = conn.entries
        
        groups = []

        for entry in groups_list:
            dn = entry.distinguishedName.value
            groups.append(dn)
        


        return render_template('create_group.html', ou_list=selected_ou, groups_list=groups)

    # VERIFICA SE O USUÁRIO PERTENCE AO GRUPO LDAP_GROUP_DN
    server = Server(LDAP_HOST, use_ssl=True, get_info=ALL)
    conn = Connection(server, user=f"{usernameLST}{INTRANET}", password=passwordLST, authentication=SIMPLE, auto_bind=True)

    search_filter = f'(&(sAMAccountName={usernameLST})(memberOf={LDAP_GROUP_DN}))'
    conn.search(LDAP_BASE_DN, search_filter, attributes=['sAMAccountName'])
    
    # SE O USUÁRIO PERTENCER AO GRUPO, RENDERIZA A PÁGINA
    return render_template('create_group.html', ou_list=ou_list)

@app.route('/commitCreate', methods=['GET', 'POST'])
def create_group():
    if request.method == 'POST':
        selected_group = request.form.get('selected-group')
        selected_ou = request.form.get('selected-ou')
        groupName = request.form.get('groupName')
        logger.info(selected_group)

        # OBTENDO USUÁRIO E SENHA DA SESSÃO
        usernameLST = session.get('usernameLST')
        passwordLST = session.get('passwordLST')

        # RENDERIZANDO CONEXÃO DO LDAP
        server = Server(LDAP_HOST, use_ssl=True, get_info=ALL)
        conn = Connection(server, user=f"{usernameLST}{INTRANET}", password=passwordLST, authentication=SIMPLE, auto_bind=True)
        
        # CRIANDO O NOME COMPLETO DA OU
        complete_ou = f"CN={groupName},OU={selected_ou},DC=intranet,DC=leste"

        try:
            # CRIANDO CONNECTOR DO WINRM
            group_attributes = {
            'cn': groupName,
            'objectClass': ['top', 'group'],
            'sAMAccountName': groupName,
            }

            # EXECUTANDO A CRIAÇÃO DO GRUPO
            if conn.add(complete_ou, attributes=group_attributes):
                logger.info(f"O usuário: {usernameLST}, criou o grupo: {groupName}.")
                flash('Grupo criado!', 'success')
                time.sleep(20)
                if selected_group == "nenhum":
                    conn.unbind()
                else:
                    conn.modify(selected_group, {'member': [(MODIFY_ADD, [complete_ou])]})
                    conn.unbind()

                # return render_template('create_group.html', ou_list=ou_list)
                return redirect(url_for('create_group.search_group'))
            else:
                if conn.result['result'] == 68:
                    flash('Grupo já existente!', 'error')
                else:
                    flash(conn.result, 'error')
                return redirect(url_for('create_group.search_group'))
        except Exception as e:
            flash(e, 'error')
            logger.info(e)
            return redirect(url_for('create_group.search_group'))
        finally:
            conn.unbind()



