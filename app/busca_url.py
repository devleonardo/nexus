from flask import Flask, render_template, request, redirect, url_for, Blueprint, session, flash, send_file
from ldap3 import Server, Connection, SIMPLE, ALL, Attribute, MODIFY_REPLACE, Entry, NTLM
import subprocess
from app.config import *
from openpyxl import Workbook
import io
from app.verificador import group_verification

app = Blueprint('busca_url', __name__)

# RENDERIZA O DASHBOARD
@app.route('/busca_url')
def url_busca():
    # VERIFICA SE O USUÁRIO PERTENCE A ALGUM GRUPO DE ACESSO PARA A PÁGINA
    result = group_verification()
    if result == True:
        pass
    else:
        return result
    return render_template('busca_url.html')

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
        return render_template('busca_url.html', comando=urls_resolvidas)

@app.route('/buscar_todos', methods=['GET', 'POST'])
def buscar_todos():
    if request.method == 'POST':
        # PEGA O NOME DO USUÁRIO LOGADO NA SESSÃO  
        usernameLST = session.get('usernameLST')

        # EXECUTA UM COMANDO SHELL PARA FILTRAR E OBTER DADOS DO ARQUIVO anablock.conf 
        comando_anablock = subprocess.getoutput(f"cut -d : -f 2 anablock.conf | awk '{{print $1}}'")

        # EXECUTA UM COMANDO SHELL PARA FILTRAR E OBTER DADOS DO ARQUIVO sistemasbloqueados.conf
        comando_sitesbloqueados = subprocess.getoutput("grep -oP '(?<=name: \")[^\"]+' sitesbloqueados.conf")

        # VERIFICA SE HÁ ALGUM RESULTADO NOS COMANDOS SHELL RETORNADOS
        if comando_anablock:
            # REMOVE ASPAS DUPLAS E DIVIDE A STRING EM UMA LISTA DE PALAVRAS
            comando_anablock = set(comando_anablock.replace('"', '').split())
        
        if comando_sitesbloqueados:
            # DIVIDE A STRING EM UMA LISTA DE PALAVRAS
            comando_sitesbloqueados = set(comando_sitesbloqueados.split())

        # FAZ A UNIÃO DOS CONJUNTOS SEM DUPLICATAS
        todos_dominios = comando_anablock | comando_sitesbloqueados

        # ARMAZENA O RESULTADO NA SESSÃO 
        session['comando'] = list(todos_dominios)
        
        # IMPRIME OS TESTE NA PAGINA RENDERIZADA
        return render_template('busca_url.html', comando=todos_dominios)

@app.route('/criar_planilha', methods=['GET', 'POST'])
def criar_planilha():
    # OBTÉM OS DADOS DA SESSÃO
    comando = session.get('comando')
    
    # CRIA UM NOVO WORKBOOK E WORKSHEET
    wb = Workbook()
    ws = wb.active
    
    # DEFINE O TÍTULO DA PLANILHA
    ws.title = "Dados"
    
    # ADICIONA UM CABEÇALHO NA PRIMEIRA LINHA
    ws.append(["Resultado"])
    
    # ITERA SOBRE OS ELEMENTOS EM 'COMANDO' E ADICIONA CADA UM COMO UMA LINHA NA PLANILHA
    for elemento in comando:
        ws.append([elemento])
    
    # CRIA UM BUFFER DE BYTESIO PARA ARMAZENAR A PLANILHA
    buffer = io.BytesIO()
    
    # SALVA O WORKBOOK NO BUFFER
    wb.save(buffer)
    
    # REPOSICIONA O CURSOR DO BUFFER PARA O INÍCIO
    buffer.seek(0)

    # RETORNA O ARQUIVO EXCEL COMO UM ANEXO PARA DOWNLOAD
    return send_file(buffer, as_attachment=True, download_name='resultado.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')