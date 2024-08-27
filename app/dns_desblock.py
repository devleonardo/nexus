from app.config import *
import os
from flask import Flask, render_template, request, Blueprint, redirect, url_for, session, flash
import subprocess

app = Blueprint('dns_desblock', __name__)

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

def carregar_dominios():
    dominios = []

    with open('anablock.conf', 'r') as arquivo:
        for linha in arquivo:
            if 'local-zone' in linha:
                dominio = linha.split('"')[1]
                dominios.append(dominio)
    return dominios

@app.route('/dns_desblock')
def dns_desblock():
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

    # EXECUTA UM COMANDO SHELL PARA FILTRAR E OBTER DADOS DO ARQUIVO anablock.conf 
    comando_anablock = subprocess.getoutput(f"cut -d : -f 2 anablock.conf | awk '{{print $1}}'")

    # EXECUTA UM COMANDO SHELL PARA FILTRAR E OBTER DADOS DO ARQUIVO sitesbloqueados.conf
    comando_sitesbloqueados = subprocess.getoutput("grep -oP '(?<=name: \")[^\"]+' sitesbloqueados.conf")

    # VERIFICA SE HÁ ALGUM RESULTADO NOS COMANDOS SHELL RETORNADOS
    if comando_anablock:
        # REMOVE ASPAS DUPLAS E DIVIDE A STRING EM UMA LISTA DE PALAVRAS
        comando_anablock = set(comando_anablock.replace('"', '').split())
    else:
        comando_anablock = set()
    
    if comando_sitesbloqueados:
        # DIVIDE A STRING EM UMA LISTA DE PALAVRAS
        comando_sitesbloqueados = set(comando_sitesbloqueados.split())
    else:
        comando_sitesbloqueados = set()

    # FAZ A UNIÃO DOS CONJUNTOS SEM DUPLICATAS
    todos_dominios = list(comando_anablock | comando_sitesbloqueados)

    # ARMAZENA O RESULTADO NA SESSÃO 
    session['comando'] = todos_dominios
    
    # IMPRIME OS TESTES NA PAGINA RENDERIZADA
    return render_template('dns_desblock.html', todos_dominios=todos_dominios)

@app.route('/resolve_url', methods=['GET', 'POST'])
def resolve_url():
    if request.method == 'POST':
        # PEGA O NOME DO USUÁRIO LOGADO NA SESSÃO  
        usernameLST = session.get('usernameLST')
       
        # RECEBE A URL DIGITADO NO INPUT DO FRONT E REMOVE CARACTERES ESPECIAIS
        url = request.form.get('form_url')

         # EXECUTA UM COMANDO SHELL PARA FILTRAR E OBTER DADOS DO ARQUIVO anablock.conf COM BASE NA URL FORNECIDA
        comando_anablock = subprocess.getoutput(f"cut -d : -f 2 anablock.conf | grep {url} | awk '{{print $1}}'")
        comando_anablock = set(comando_anablock.replace('"', '').split()) if comando_anablock else set()

        # EXECUTA UM COMANDO SHELL PARA FILTRAR E OBTER DADOS DO ARQUIVO sitesbloqueados.conf COM BASE NA URL FORNECIDA
        comando_sitesbloqueados = subprocess.getoutput(f"grep -oP '(?<=name: \")[^\"]+' sitesbloqueados.conf | grep {url}")
        comando_sitesbloqueados = set(comando_sitesbloqueados.split()) if comando_sitesbloqueados else set()

        # FAZ A INTERSEÇÃO DOS CONJUNTOS 
        urls_resolvidas = comando_anablock | comando_sitesbloqueados
        # ARMAZENA O RESULTADO NA SESSÃO PARA USO FUTURO
        session['comando'] = urls_resolvidas
        
        # IMPRIME OS TESTE NA PAGINA RENDERIZADA
        return render_template('dns_desblock.html', urls_resolvidas=urls_resolvidas)