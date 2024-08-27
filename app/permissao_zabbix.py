from flask import Flask, render_template, request, Blueprint, redirect, url_for, session, jsonify, flash
from app.config import *

app = Blueprint('permissao_zabbix', __name__)

# ABRE O ARQUIVO permitido.txt E ARMAZENA O CONTEUDO DENTRO DE UM ARRAY
caminho_permissao = "permitido_zabbix.txt"
permitido = []

with open(caminho_permissao, 'r') as arquivo: # type: ignore
    permitido = arquivo.read().splitlines()

# FUNÇÃO PARA ESCREVER AS ALTERAÇÕES REALIZADAS NO ARQUIVO permitidos.txt
def salvar_permissao(permitido):
    with open(caminho_permissao, "w") as file: # type: ignore
        for item in permitido:
            file.write(item + "\n")

# RENDERIZA A HOME
@app.route('/permissao_zabbix', methods=['POST', 'GET'])
def permissao_zabbix():

    # CHECA SE O USUÁRIO ESTÁ LOGADO, CASO CONTRÁRIO, REDIRECIONA PARA A PÁGINA DE LOGIN
    if not session.get('logged_in'):
        return render_template('login.html')
    
    # OBTÉM O NOME DE USUÁRIO DA SESSÃO
    usernameLST = session.get('usernameLST')
    #finalizar posteriormente

    # VERIFICA SE O USUARIO TEM PERMISSAO PARA ACESSAR A PÁGINA
    if usernameLST in permissao_azabbix:

        # REMOVE O USUÁRIO SELECIONADO DO ARRAY PERMITIDO
        if request.method == 'POST':
            negar = request.form.get('negar')
            if negar is not None:
                permitido.remove(negar)
                salvar_permissao(permitido)
                return redirect('/permissao_zabbix')

        #ADICIONA O USUARIO DIGITADO NO ARRAY PERMITIDO
        if request.method == 'POST':
            conceder = request.form.get('conceder')
            if conceder is not None:
                permitido.append(conceder)
                salvar_permissao(permitido)
                return redirect('/permissao_zabbix')
                
    # SE O USUÁRIO NÃO ESTIVER NO ARRAY NEGA A ENTRADA
    else:
        flash('Você não tem permissão de acesso!', 'error')
        return redirect(request.referrer)

    
    return render_template('permissao_zabbix.html', PERMITIDO=permitido)
