from flask import Flask, render_template, request, Blueprint, redirect, url_for, session, flash
from ldap3 import Server, Connection, SIMPLE, ALL, MODIFY_REPLACE, SUBTREE, MODIFY_DELETE
from app.verificador import group_verification
import logging
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from app.config import *

app = Blueprint('statusIX', __name__)

# RENDERIZA A HOME
@app.route('/statusIX')
def consulta_IX():

    result = group_verification()
    if result == True:
        pass
    else:
        return result
    

    #CONFIGURA INFORMAÇÕES DE LOGGING
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        handlers=[logging.FileHandler("selenium_log.log"),
                                logging.StreamHandler()])
    logging.info("Iniciando registro de log.")
    # Configuração do driver do navegador via linha de comando
    chrome_options = webdriver.ChromeOptions();
    # Define como linha de comando
    chrome_options.add_argument('--headless');
    logging.info("Navegador configurado para modo headless.")
    # Abre em segundo plano
    chrome_options.add_argument('--no-sandbox');
    # Não capta nenhum áudio emitido pelo navegador
    chrome_options.add_argument('--mute-audio');
    # Local do webdriver do navegador
    chromedriver_path = "/usr/bin/chromedriver"
    # Caminho da aplicação do navegador Chromium
    chrome_path = "/usr/bin/chromium-browser"
    # Adiciona qual navegador será utilizado
    chrome_options.binary_location = chrome_path
    # Define o webdriver com os parâmetros acima
    navegador = webdriver.Chrome(options=chrome_options);
    # DEFINE A URL A SER CONSULTADA
    url = 'https://status.ix.br/'


    # VERIFICA SE O ELEMENTO BUSCADO EXISTE E ARMAZENA AS INFORMAÇÕES DESEJADAS
    try:
        #CONSULTA A PÁGINA E DEFINIE TIMEOUT DE 3 SEGUNDOS
        navegador.get(url)
        logging.info(f"Navegador inicializado. Consultando a página {url}")
        #BUSCA OS ELEMENTOS QUE ABREM OS MENUS REGIONAIS
        base_ix_SaoPaulo = navegador.find_element(By.XPATH, "(//i[contains(@class, 'group-toggle') and contains(@class, 'ion-ios-plus-outline')])[1]")
        base_ix_Rio = navegador.find_element(By.XPATH, "(//i[contains(@class, 'group-toggle') and contains(@class, 'ion-ios-plus-outline')])[2]")
        base_ix_SaoPaulo.click()
        base_ix_Rio.click()
        #RECUPERA TODOS OS GRUPOS REGIONAIS
        status = navegador.find_elements(By.CSS_SELECTOR,'div > ul')
        #SEPARA A INFORMAÇÃO EM UMA LISTA DE LISTAS REGIONAIS
        data = [element.text for element in status]
        #SEPARA TODAS AS LOCALIDADES E STATUS DE SÃO PAULO E RIO
        base_ix_SaoPaulo = data[0].split('\n')
        base_ix_Rio = data[1].split('\n')
    except:
        logging.info("Elemento não encontrado.")
    
    logging.info("Consulta finalizada")
    navegador.quit()

    # Constante usada como parametro de comparação no html
    if base_ix_Rio[2] and base_ix_Rio[4] and base_ix_Rio[6] == 'Operacional':
        statusRio = 'ok'
    else:
        statusRio = 'Error'

    if base_ix_SaoPaulo[2] and base_ix_SaoPaulo[4] and base_ix_SaoPaulo[6] == 'Operacional':
        statusSP = 'ok'
    else:
        statusSP = 'Error'

    dataConsulta = datetime.now().strftime("%H:%M")
    return render_template('statusIX.html', dataConsulta=dataConsulta, base_ix_Rio=base_ix_Rio, base_ix_SaoPaulo=base_ix_SaoPaulo, statusRio=statusRio, statusSP=statusSP)