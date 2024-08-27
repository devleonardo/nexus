from flask import Flask, render_template, request, Blueprint, redirect, url_for, session, flash
from ldap3 import Server, Connection, SIMPLE, ALL, MODIFY_REPLACE, SUBTREE, MODIFY_DELETE
from app.config import *

app = Blueprint('glpi', __name__)

# RENDERIZA A PÁGINA GLPI
@app.route('/glpi')
def glpi():

    # CHECA SE O USUÁRIO ESTÁ LOGADO, CASO CONTRÁRIO, REDIRECIONA PARA A PÁGINA DE LOGIN
    if not session.get('logged_in'):
        return render_template('login.html')
    
    usernameLST = session.get('usernameLST')
    passwordLST = session.get('passwordLST')

    # VERIFICA SE O USUÁRIO PERTENCE AO GRUPO LDAP_GROUP_DN
    server = Server(LDAP_HOST, use_ssl=True, get_info=ALL)
    conn = Connection(server, user=f"{usernameLST}{INTRANET}", password=passwordLST, authentication=SIMPLE, auto_bind=True)

    search_filter = f'(&(sAMAccountName={usernameLST})(memberOf={LDAP_GROUP_DN}))'
    conn.search(LDAP_BASE_DN, search_filter, attributes=['sAMAccountName'])
    
    # SE O USUÁRIO PERTENCER AO GRUPO, RENDERIZA A PÁGINA DE BUSCA
    if len(conn.entries) > 0:
        return render_template('glpi.html')
    else:
        # CASO CONTRÁRIO, REDIRECIONA PARA A PÁGINA DASHBOARD.HTML
        flash('Você não tem permissão de acesso!', 'error')
        return redirect(request.referrer)