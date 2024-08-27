from flask import Flask, render_template, request, redirect, url_for, Blueprint, session, flash
from app.verificador import group_verification

import requests
import re
from app.config import *

app = Blueprint('busca_mac', __name__)

# RENDERIZA O DASHBOARD
@app.route('/busca_mac')
def mac_busca():
    # VERIFICA SE O USUÁRIO PERTENCE A ALGUM GRUPO DE ACESSO PARA A PÁGINA
    result = group_verification()
    if result == True:
        pass
    else:
        return result

    return render_template('busca_mac.html')
@app.route('/busca_mac', methods=['GET', 'POST'])
def resolve_mac():

    if request.method == 'POST':
        # PEGA O NOME DO USUÁRIO LOGADO NA SESSÃO  
        usernameLST = session.get('usernameLST')
       
        # RECEBE O MAC DIGITADO NO INPUT DO FRONT E REMOVE CARACTERES ESPECIAIS
        mac = request.form.get('mac_addr')
        mac_addr = re.sub('[!@#$%&><()+*:._@#$-]', '', mac)
        # CONSULTA O FABRICANTE DO MAC FORNECIDO E FORMATA MENSAGEM
        vendorsURL = f'https://api.macvendors.com/{mac_addr.upper()}'
        response = requests.get(vendorsURL)
        manufacturer = response.text

        # VERIFICA SE O TAMANHO DO MAC DIGITADO ESTÁ CORRETO
        if( len(mac_addr) < 12):
            manufacturer = "Tamanho inválido. Verifique o MAC digitado e tente novamente."
            flash(manufacturer, 'error')

        # VERIFICA SE O RESULTADO DA CONSULTA FOI 404
        elif("errors" in manufacturer):
            manufacturer = "Não encontrado. Certifique-se de buscar um MAC válido."
            flash(manufacturer, 'error')

        # GERANDO LOG DE AÇÃO
        logger.info(f'O usuário: {usernameLST}, realizou uma busca pelo MAC-Address: {mac_addr}')

        # IMPRIME OS TESTE NA PAGINA RENDERIZADA
        return render_template('busca_mac.html', manufacturer=manufacturer)
