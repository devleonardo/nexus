from app.config import *
from flask import session, request, Blueprint, redirect, url_for, flash
import winrm

app = Blueprint('clonar_grupos', __name__)

@app.route('/clonar_grupos', methods=['GET', 'POST'])
def clonar_grupos(username):
    # OBTEM O NOME DE USUARIO DA SESSÃO
    usernameLST = session.get('usernameLST')

    if request.method == "POST":
        usuario_origem = request.form.get('usuarioOrigem')
        # grupos_para_clonar = request.form.getlist('groups_to_copy')
        # grupos_to_copy = ",".join([f'"{grupo}"' for grupo in grupos_para_clonar])

        comando = f"""
Import-Module ActiveDirectory ;
$usuarioOrigem = "{usuario_origem}" ;
$usuarioDestino = "{username}" ;
$gruposUsuarioDestino = Get-ADUser $usuarioDestino -Properties MemberOf | Select-Object -ExpandProperty MemberOf ;
$gruposUsuarioOrigem = Get-ADUser $usuarioOrigem -Properties MemberOf | Select-Object -ExpandProperty MemberOf ;
foreach ($grupo in $gruposUsuarioDestino) {{ Remove-ADGroupMember -Identity $grupo -Members $usuarioDestino -Confirm:$false }} ;
foreach ($grupo in $gruposUsuarioOrigem) {{ Add-ADGroupMember -Identity $grupo -Members $usuarioDestino }}
"""
        
        sess = winrm.Session(
            AD04,
            auth=(LDAP_USER_CN, LDAP_USER_PASSWORD),
            transport='ntlm',
            server_cert_validation='ignore'
        )

        sess.run_ps(comando)

        logger.info(f"Usuário {usernameLST} clonou os grupos de {usuario_origem} para {username}.")

        flash('Grupos clonados!', 'success')

        return redirect(url_for('busca.show_user_details', username=username))