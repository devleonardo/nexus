from app.config import *
from flask import redirect, url_for, session
from ldap3 import Server, Connection, SIMPLE, ALL

def ad_remove(username):

    # VERIFICAR SE O URUARIO ESTA LOGADO
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    # OBTEM O NOME DE USUARIO DA SESSÃO
    usernameLST = session.get('usernameLST')
    passwordLST = session.get('passwordLST')
    
    # RECUPERA OS DETALHES DO USUARIO DO SERVIDOR LDAP
    server = Server(LDAP_HOST, use_ssl=False, get_info=ALL)
    conn = Connection(server, f"{usernameLST}{INTRANET}", password=passwordLST, authentication=SIMPLE, auto_bind=True)
    
    # FAZ UMA BUSCA LDAP PARA OBTER OS ATRIBUTOS DA ESTAÇÃO
    search_filter = f'(sAMAccountName={username})'
    conn.search(LDAP_BASE_DN, search_filter, attributes=['displayName', 'whenCreated'])
    
    # OBTEM O DN DA ESTAÇÃO PARA REMOVER
    entry_dn = conn.entries[0].entry_dn

    # REMOVE A ESTAÇÃO
    if conn.delete(entry_dn):
        # QUEM REMOVEU A ESTAÇÃO
        logger.info(f"Estação: {username} removida por: {usernameLST}")
    else:
        # A REMOÇÃO FALHOU
        logger.info(f"A estação: {username} não foi removida.")

    # RETORNA PARA A PÁGINA DE BUSCA, APÓS REMOVER A ESTAÇÃO
    return redirect(url_for('busca.search_users'))