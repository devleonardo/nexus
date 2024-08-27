from flask import Flask, render_template, request, Blueprint, redirect, url_for, session, flash
import os
import subprocess
import time

app = Blueprint('dns_block', __name__)

# VERIFICA SE HOUVE ALGUMA MODIFICAÇÃO DE PERMISSÃO E CARREGA OS USUÁRIOS PERMITIDOS###########
caminho_confirmacao_form = "confirmacao_dns_block.txt"
caminho_permissao = "permitido.txt"
permitido = []
ultima_modificacao = 0


def carregar_permitido():
    global ultima_modificacao
    ultima_modificacao_arquivo = os.path.getmtime(caminho_permissao)
    if ultima_modificacao_arquivo > ultima_modificacao:
        ultima_modificacao = ultima_modificacao_arquivo
        with open(caminho_permissao, 'r') as arquivo:
            permitido.clear()
            permitido.extend(arquivo.read().splitlines())
###############################################################################################

# RENDERIZA A HOME
@app.route('/dns_block')
def dns_block():
    carregar_permitido()

    # CHECA SE O USUÁRIO ESTÁ LOGADO, CASO CONTRÁRIO, REDIRECIONA PARA A PÁGINA DE LOGIN
    if not session.get('logged_in'):
        return render_template('login.html')
    
    # OBTÉM O NOME DE USUÁRIO DA SESSÃO
    usernameLST = session.get('usernameLST')

    with open(caminho_confirmacao_form, 'r') as confirmacao:
        confirmacao_dns_form = confirmacao.read().strip()

    if usernameLST in permitido:
        pass

    else:
        # CASO CONTRÁRIO, REDIRECIONA PARA A PÁGINA DE LOGIN
        flash('Você não tem permissão de acesso!', 'error')
        return redirect(request.referrer)


    return render_template('dns_block.html')