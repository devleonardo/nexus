from app.config import *
from flask import redirect, url_for, session, request, flash
from ldap3 import Server, Connection, SIMPLE, ALL, MODIFY_REPLACE, SUBTREE, MODIFY_DELETE # BIBLIOTECA DE CONEXÃO LDAP
import winrm

def edit_groups(username):
  # OBTEM O NOME DE USUARIO DA SESSÃO
  usernameLST = session.get('usernameLST')
  passwordLST = session.get('passwordLST')

  server = Server(LDAP_HOST, use_ssl=True, get_info=ALL)
  conn = Connection(server, user=f"{usernameLST}{INTRANET}", password=passwordLST, authentication=SIMPLE, auto_bind=True)
  

  # CASO A CONEXÃO ENTRE SERA CAPTADO O USERNAME E O DN DO USUARIO
  if conn.bind():
      search_filter = f'(sAMAccountName={username})'
      conn.search(LDAP_BASE_DN, search_filter, attributes=['distinguishedName'])
      group_conn = Connection(server, user=LDAP_USER_CN, password=LDAP_USER_PASSWORD, authentication=SIMPLE, auto_bind=True)
      group_conn.search(LDAP_BASE_DN, '(objectClass=group)', search_scope=SUBTREE, attributes=['cn'])

      # Obtém os grupos disponíveis no AD
      grupos_ad = []
      for entry in group_conn.entries:
          grupo_ad = entry.entry_dn
          if 'OU=Frota' not in grupo_ad: #Não exibe carros que pertencem a OU=Frota
              grupos_ad.append(grupo_ad)
      
      if request.method == 'POST':

          # Obtém as informações dos inputs na interface web
          grupos_para_adicionar = request.form.getlist('grupos_para_adicionar')
          grupos_para_remover = request.form.getlist('grupos_para_remover')
          
          # Se houver grupos para remover, será formatado e incluído em grupos_absent
          grupos_absent = ",".join([f'"{grupo}"' for grupo in grupos_para_remover])

          # Se não houver grupo no formulario obtido, pula a execução
          if not grupos_para_remover:
              pass
          # Se houver, executa a remoção dos grupos
          else:
            comando_ps = f'''
Import-Module ActiveDirectory ;
$usuario = "{username}" ;
$grupos = {grupos_absent} ;

foreach ($grupo in $grupos) {{
  Remove-ADGroupMember -Identity $grupo -Members $usuario -Confirm:$false
}}
'''
            
            logger.info(f"Usuário {usernameLST} removeu grupo(s) de {username}.")

            sess = winrm.Session(
              AD04,
              auth=(LDAP_USER_CN, LDAP_USER_PASSWORD),
              transport='ntlm',
              server_cert_validation='ignore'
            )
            
            result = sess.run_ps(comando_ps)

          # Se não houver grupos para adicionar, pula a execução
          if not grupos_para_adicionar:
            pass
          # Se houver, executa as instruções abaixo
          else:
            # Grupos para adicionar sendo separados por "," 
            grupos_para_add = ",".join([f'"{grupo}"' for grupo in grupos_para_adicionar])

            # Comando para adicioanr grupos
            comando_ps = f'''
Import-Module ActiveDirectory ;
$usuario = "{username}" ;
$grupos = {grupos_para_add} ;sudo pacman -Rns ferdium-bin


foreach ($grupo in $grupos) {{
    Add-ADGroupMember -Identity $grupo -Members $usuario -Confirm:$false
}}
'''


            sess = winrm.Session(
              AD04,
              auth=(LDAP_USER_CN, LDAP_USER_PASSWORD),
              transport='ntlm',
              server_cert_validation='ignore'
            )
            
            sess.run_ps(comando_ps)

            logger.info(f"O usuário: {usernameLST}, Adicionou grupo(s) em: {username}.")


