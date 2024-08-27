from app.config import *
from flask import redirect, url_for, session, request, flash
from ldap3 import Server, Connection, SIMPLE, ALL, MODIFY_REPLACE
import winrm

def reset_password(username):

    # OBTEM O NOME DE USUARIO DA SESSÃO
    usernameLST = session.get('usernameLST')
    passwordLST = session.get('passwordLST')

    server = Server(LDAP_HOST, use_ssl=True, get_info=ALL)
    conn = Connection(server, user=f"{usernameLST}{INTRANET}", password=passwordLST, authentication=SIMPLE, auto_bind=True)

    # CASO A CONEXÃO ENTRE SERA CAPTADO O USERNAME E O DN DO USUARIO
    if conn.bind():
        search_filter = f'(sAMAccountName={username})'
        conn.search(LDAP_BASE_DN, search_filter, attributes=['distinguishedName'])

        # Renderizando a conexão do WINRM
        
        sess = winrm.Session(
          AD04,
          auth=(LDAP_USER_CN, LDAP_USER_PASSWORD),
          transport='ntlm',
          server_cert_validation='ignore'
        )

        # OBTÉM OS DADOS DO FORMULARIO E REALIZA UMA VERIFICAÇÃO DE VALORES
        # SE A SENHA FOR TROCADA NO PROXIMO LOGON ENTÃO: ALT_PRX = TRUE, DO CONTRARIO ALT_PRX = NONE, PORTANTO CONFIRM RECEBE FALSE COMO VALOR
        # PWD_NEVER DEFINE SE A SENHA EXPIRA OU NUNCA EXPIRA. CASO A SENHA DEVA SER TROCADA NO PROXIMO LOGON, PWD_NEVER ASSUME TRUE, DO CONTRARIO, FALSE
        if request.method == 'POST':
          new_pwd = request.form.get('nova_senha')
          alt_prx = request.form.get('alt_senha')
          nalt_pwd = request.form.get('nalt_senha')
          fix_pwd = request.form.get('fix_senha')

          if nalt_pwd == 'true':
            nalt = '$True'
          else:
            nalt = '$False'

          if fix_pwd == 'true':
            fixPwd = '$True'
          else:
            fixPwd = '$False'

          if alt_prx == 'true':
            confirm = '$True'
            comando_ps = f'''
Import-Module ActiveDirectory ;
$usuario = Get-ADUser -Identity "{username}" ;
Set-AdUser -Identity $usuario -PasswordNeverExpires $false ;
Set-AdUser -Identity $usuario -CannotChangePassword $false ;
$password = ConvertTo-SecureString -String "{new_pwd}" -AsPlainText -Force ;
Set-ADAccountPassword -Identity $usuario -NewPassword $password -Reset ;
Set-ADUser -Identity $usuario -ChangePasswordAtLogon {confirm}
'''
          else:
            confirm = '$False'
            comando_ps = f'''
Import-Module ActiveDirectory ;
$usuario = Get-ADUser -Identity "{username}" ;
Set-AdUser -Identity $usuario -PasswordNeverExpires $false ;
Set-AdUser -Identity $usuario -CannotChangePassword $false ;
$password = ConvertTo-SecureString -String "{new_pwd}" -AsPlainText -Force ;
Set-ADAccountPassword -Identity $usuario -NewPassword $password -Reset ;
Set-ADUser -Identity $user -ChangePasswordAtLogon {confirm} ;
Set-ADUser -Identity $user -CannotChangePassword {nalt} ;
Set-ADUser -Identity $user -PasswordNeverExpires {fixPwd}
'''
        
        sess.run_ps(comando_ps)
        ok = True

        if ok:
          flash('Senha alterada com sucesso!', 'success')
        else:
          flash('Erro ao alterar senha!', 'error')

        logger.info(f"O usuário: {usernameLST}, alterou a senha de {username}.")

    # Redirecione para a página de detalhes do usuário após a redefinição da senha
    return redirect(url_for('busca.show_user_details', username=username))
