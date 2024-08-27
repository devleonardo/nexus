from app.config import *
from flask import Flask, render_template, request, Blueprint, redirect, url_for, session, flash
import os

app = Blueprint('dns_block_error', __name__)

# VERIFICA SE HOUVE ALGUMA MODIFICAÇÃO DE PERMISSÃO E CARREGA OS USUÁRIOS PERMITIDOS###########
caminho_permissao = "permitido.txt"
permitido = []
ultima_modificacao = 0

def carregar_permitido():
    global ultima_modificacao
    ultima_modificacao_arquivo = os.path.getmtime(caminho_permissao)
    if ultima_modificacao_arquivo > ultima_modificacao:
        ultima_modificacao = ultima_modificacao_arquivo
        with open(caminho_permissao, 'r') as arquivo: # type: ignore
            permitido.clear()
            permitido.extend(arquivo.read().splitlines())


# RENDERIZA A HOME
@app.route('/dns_block_error')
def dns_block_error():
    carregar_permitido()

    # CHECA SE O USUÁRIO ESTÁ LOGADO, CASO CONTRÁRIO, REDIRECIONA PARA A PÁGINA DE LOGIN
    if not session.get('logged_in'):
        return render_template('login.html')
    
     # OBTÉM O NOME DE USUÁRIO DA SESSÃO
    usernameLST = session.get('usernameLST')

    if usernameLST in permitido:
        pass

    else:
       flash('Você não tem permissão de acesso!', 'error')
       return redirect(request.referrer)
      #FINAL DA ACAO
    return render_template('dns_block_error.html')
