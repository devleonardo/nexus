from app.busca import *
from app.config import * # IMPORTA AS VARIÁVEIS DE CONEXÃO E ACESSO, E BIBLIOTECA DO ARQUIVO DE CONFIGURAÇÃO
from flask import render_template, request, redirect, url_for, session, flash # WEB
from ldap3 import *
import subprocess # BIBLIOTECA PARA COMANDOS LINUX
from app.user_details import user_details
import subprocess
import winrm
import time

def create_user(username):

  # VERIFICA SE O USUARRIO ESTA LOGADO
  if not session.get('logged_in'):
    return redirect(url_for('login'))
  
  # OBTEM O NOME DE USUARIO DA SESSÃO
  usernameLST = session.get('usernameLST')
  group_to_check = "CN=CREATE_STI,OU=SISTEMASTI,DC=intranet,DC=leste"
  passwordLST = session.get('passwordLST')
  
  # RECUPERA OS DETALHES DO USUARIO DO SERVIDOR LDAP
  server = Server(LDAP_HOST, use_ssl=True, get_info=ALL)
  conn = Connection(server, f"{usernameLST}{INTRANET}", password=passwordLST, authentication=SIMPLE, auto_bind=True)
  # RECUPERA OS DETALHES DO USUARIO DO SERVIDOR LDAP
  search_filter = f'(sAMAccountName={username})'
  username_copy = search_filter.split('=')[1].rstrip(')')

  #TESTE#####################################################################################################################
  conn.search(LDAP_BASE_DN, f'(sAMAccountName={usernameLST})', SUBTREE, attributes=['memberOf'])
  if len(conn.entries) > 0:
    user_entry = conn.entries[0]
      
    # Verifica se o usuário tem atributo 'memberOf' para obter os grupos
    if 'memberOf' in user_entry:
      groups_check = user_entry['memberOf']
            
    if group_to_check in groups_check:
      ###########################################################################################################################
      conn.search(LDAP_BASE_DN, search_filter, attributes=['physicalDeliveryOfficeName', 'ipPhone', 'initials','sn','givenName','ou','cn','name', 'mail', 'displayName', 'description', 'sAMAccountName', 'userPrincipalName', 'memberOf', 'userAccountControl', 'distinguishedName', 'objectCategory', 'whenCreated', 'badPasswordTime', 'badPwdCount', 'lastLogoff', 'lastLogon', 'logonCount', 'pwdLastSet', 'whenCreated', 'whenChanged', 'accountExpires'])

      # LISTA OS GRUPOS DE PERMISSÕES DO USUÁRIO
      group_conn = Connection(server, user=LDAP_USER_CN, password=LDAP_USER_PASSWORD, authentication=SIMPLE, auto_bind=True)
      group_conn.search(LDAP_BASE_DN, '(objectClass=group)', search_scope=SUBTREE, attributes=['cn'])
      
      # RECUPERA OS ATRIBUTOS DOS USUARIOS
      entry = conn.entries[0]
      user_attributes = entry.entry_attributes_as_dict
      
      # EXTRAINDO INFORMAÇÕES DO USUÁRIO / ESTAÇÃO
      username = entry.sAMAccountName.value # NOME DE USUÁRIO
      user_gn = entry.givenName.value # NOME
      user_sn = entry.sn.value # SOBRENOME
      user_init = entry.initials.value # INICIAIS
      description = entry.description.value if 'description' in entry else '' # DESCRIÇÃO DO USUÁRIO / FUNÇÃO
      email = entry.mail.value if 'mail' in entry else '' # EMAIL DO USUÁRIO
      member_of = user_attributes.get('memberOf', ['']) # GRUPO DE PERMISSÕES DO USUÁRIO
    
      # LISTANDO GRUPOS DE PERMISSÕES
      groups = []
      for group in member_of:
          group_name = subprocess.getoutput(f"less {group} | awk -F '=' '{{print $2}}' | awk -F ',' '{{print $1}}'")
          groups.append(group_name)

      sess = winrm.Session(
        AD04,
        auth=(LDAP_USER_CN, LDAP_USER_PASSWORD),
        transport='ntlm',
        server_cert_validation='ignore'
      )

      if request.method == 'POST':

        # PEGANDO NOVOS DADOS DO USUÁRIO PARA ALTERAÇÃO
        new_name = request.form.get('nome')
        new_description = request.form.get('descricao')
        new_email = request.form.get('e_mail')
        new_sn = request.form.get('sn')
        new_init = request.form.get('init')
        new_login = request.form.get('login')
        new_cpf = request.form.get('cpf')

        # VERIFICANDO SE O LOGIN JA EXISTE
        login_verify = f'(sAMAccountName={new_login})'
        conn.search(LDAP_BASE_DN, login_verify, attributes=['sAMAccountName'])
        if len(conn.entries) > 0:
          flash('Nome de usuário em uso!', 'error')
          return render_template('create_user.html', user_gn=user_gn, user_init=user_init, user_sn=user_sn, username=username, description=description, email=email, groups=groups)




        
        # MONTANDO A CRIAÇÃO DE USUARIO COM AS NOVAS INFORMAÇÕES
        comando_ps = f'''
Import-Module ActiveDirectory ;
$FirstName = "{new_name}" ;
$LastName = "{new_sn}" ;
$Name = "{new_name} {new_sn}" ;
$DisplayName = "{new_name} {new_sn}" ;
$Password = "Leste@2024" | ConvertTo-SecureString -AsPlainText -Force ;
$Description = "{new_description}" ;
$Email = "{new_email}" ;
$sAMAccountName = "{new_login}" ;
$UPN = "{new_login}@intranet.leste" ;
$Initials = "{new_init}" ;
$EmployeeId = "{new_cpf}" ;
$State = "present" ;

$UserParams = @{{
    "Name" = $Name 
    "GivenName" = $FirstName 
    "Surname" = $LastName 
    "DisplayName" = $DisplayName 
    "UserPrincipalName" = $UPN
    "Description" = $Description  
    "EmaiLAddress" = $Email 
    "AccountPassword" = $Password 
    "Enabled" = $true 
    "Initials" = $Initials 
    "State" = $State 
    "EmployeeId" = $EmployeeId
    "SamAccountName" = $sAMAccountName
}}

New-ADUser @UserParams ;

$sourceUser = "{username_copy}" ;
$targetUser = "{new_login}" ;
$sourceGroups = Get-ADUser -Identity $sourceUser -Properties MemberOf | Select-Object -ExpandProperty MemberOf ;
foreach ($group in $sourceGroups) {{
    Add-ADGroupMember -Identity $group -Members $targetUser
}}
'''   
        # Executa o comando no PowerShell do AD através do WinRM
        sess.run_ps(comando_ps)

        time.sleep(4)
        # Chama funçaõ externa para provisionar no OTRS
        comando = ["python3", "app/scripts/provisiona_otrs.py", new_login]
        # comando = f"python3 /home/usshd/Sistemas-TI/app/scripts/provisiona_otrs.py {new_login}"
        subprocess.Popen(comando)
        
        flash('Usuário criado!', 'success')

        # LOG DE ALTERAÇÕES DO USUÁRIO
        logger.info(f"Usuário {usernameLST} Criou o usuário {new_login}.")
        # return user_details(new_login)
        return redirect(url_for('busca.show_user_details', username=new_login))



      return render_template('create_user.html', user_gn=user_gn, user_init=user_init, user_sn=user_sn, username=username, description=description, email=email, groups=groups)
    else:
      # CASO CONTRÁRIO, REDIRECIONA PARA A PÁGINA DE LOGIN
      flash('Você não tem permissão de acesso!', 'error')
      return redirect(request.referrer)
