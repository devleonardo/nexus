from flask import Flask, render_template, request, Blueprint, redirect, url_for, session, flash
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

app = Blueprint('statusCS', __name__)

# RENDERIZA A HOME
@app.route('/statusCS')
def consulta_CS():

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
    url = 'https://status.clicksign.com/'
    status = ''
    logging.info(f"Navegador inicializado. Consultando a página {url}")
    navegador.get(url)
    appCS = "Clicksign (app.clicksign.com) "
    deskCS = " Clicksign Classic (desk.clicksign.com) "
    appStatus = ""
    deskStatus = ""


    # VERIFICA SE O ELEMENTO BUSCADO EXISTE E ARMAZENA AS INFORMAÇÕES DESEJADAS
    try:
        logging.info("Tentativa de leitura do status.")
        appStatus = navegador.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/span[2]").text
        deskStatus = navegador.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/span[2]").text
        logging.info("Consulta finalizada")
    except: 
        logging.info(f"Erro na consulta à página. App {appStatus}, Desk {deskStatus}")
    
    navegador.quit()

    if (appStatus != 'Operational'):
        appStatus = "Problemas relatados"
    if (deskStatus != 'Operational'):
        deskStatus = "Problemas relatados"

    # # Constante usada como parametro de comparação no html
    # if status != "All Systems Operational":
    #     status = 'Error'

    dataConsulta = datetime.now().strftime("%H:%M")
    return render_template('statusCS.html', dataConsulta=dataConsulta, appCS=appCS, appStatus=appStatus, deskCS=deskCS, deskStatus=deskStatus)