from app.config import *
from flask import render_template, request, redirect, url_for, session, flash
from ldap3 import Server, Connection, SIMPLE, ALL, MODIFY_REPLACE
import mysql.connector
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def block_user(username):
    ######################################## AD ###################################################################################
    # CHECA SE O USUÁRIO ESTÁ LOGADO, CASO CONTRÁRIO, REDIRECIONA PARA A PÁGINA DE LOGIN
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    # OBTEM O NOME DE USUARIO DA SESSÃO
    usernameLST = session.get('usernameLST')
    passwordLST = session.get('passwordLST')

    # RECEBE O COMANDO DE BLOQUEAR OU DESBLOQUEAR NA PÁGINA DO USUÁRIO
    block = request.form.get('block')

    if block == 'true':
        # USUÁRIO QUE ESTA REALIZANDO A ALTERAÇÃO NA BASE DE DADOS DO AD
        logger.info(f"Bloqueio do usuário: {username} realizado por: {usernameLST}")
        user_account_control = 2  # VALOR PARA BLOQUEAR A CONTA
        otrs_value = 2 # VALOR PARA BLOQUEAR CONTA DO OTRS
    else:
        # USUÁRIO QUE ESTA REALIZANDO A ALTERAÇÃO NA BASE DE DADOS DO AD
        logger.info(f"Desbloqueio do usuário: {username} realizado por: {usernameLST}")
        user_account_control = 0  # VALOR PARA DESBLOQUEAR A CONTA
        otrs_value = 1 # VALOR PARA DESBLOQUEAR CONTA DO OTRS

    # REALIZE A CONEXÃO COM O SERVIDOR LDAP E MODIFIQUE O ATRIBUTO USERACCOUNTCONTROL
    server = Server(LDAP_HOST, use_ssl=False, get_info=ALL)
    conn = Connection(server, user=f"{usernameLST}{INTRANET}", password=passwordLST, authentication=SIMPLE, auto_bind=True)
    search_filter = f'(sAMAccountName={username})'
    conn.search(LDAP_BASE_DN, search_filter, attributes=['userAccountControl'])

    # REALIZA O BLOQUEIO OU DESBLOQUEIO A PARTIR DO RESULTADO OBTIDO
    entry = conn.entries[0]
    conn.modify(entry.entry_dn, {'userAccountControl': [(MODIFY_REPLACE, [user_account_control])]})

    ####################### OTRS ############################################################################################
    # Pré configurações de acesso ao DB do OTRS
    config = {
    "host": "186.211.32.27",
    "port": 3306,
    "user": "nexus",
    "password": "D9mCLvr9fg",
    "database": "otrs_db",
    }

    #  Criando a conexão com o DB do OTRS
    cnx = mysql.connector.connect(**config)
    # Criando o cursor da conexão com o DB
    cur = cnx.cursor()
    # Executando a alteração no DB, e utilizando o vakid_id de acordo com a interface web
    cur.execute(f"UPDATE users SET valid_id = {otrs_value} WHERE login = '{username}';")
    # Efetivando as modificações na tabela users do DB OTRS
    cnx.commit()
    # Fechando o cursor da conexão
    cur.close()
    # Fechando a conexão com o DB OTRS
    cnx.close()

    ################### SELENIUM ################################################################################################
    # Parâmetros de acesso do selenium para a interface web do OTRS
    otrs_url = "http://otrs01.lestetelecom.com.br/otrs/index.pl"
    username_otrs = username
    password_otrs = "Leste@2023"

    try:
        # Configuração do driver do navegador via linha de comando
        chrome_options = webdriver.ChromeOptions();
        # Define como linha de comando
        chrome_options.add_argument('--headless');
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
        driver = webdriver.Chrome(options=chrome_options);
        # Abre a interface grãfica através da otrs_url
        driver.get(otrs_url)
        # Aguarda por até 10 segundos caso o navegador demore a carregar a página
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "User")))
        # Encontra o input User para preencher com o login do usuário
        username_field = driver.find_element(By.NAME, "User")
        # Encontra o input Password para preencher com uma senha fictícia
        password_field = driver.find_element(By.NAME, "Password")
        # Envia o login para o campo User no navegador
        username_field.send_keys(username_otrs)
        # Envia a senha para o campo Password no navegador
        password_field.send_keys(password_otrs)
        # Encontra o botão de login ID = "LoginButton"
        login_button = driver.find_element(By.ID, "LoginButton")
        # Efetua um click no botão de login
        login_button.click()
        # Fecha o navegador
        driver.quit()
    # Caso alguma execução dê erro, ẽ tratado nesse except
    except Exception as e:
        # flash(e, 'error')
        print(e)
    # REDIRECIONE DE VOLTA PARA A PÁGINA DE DETALHES DO USUÁRIO
    flash('Bloqueio realizado!', 'success')
    return redirect(url_for('busca.show_user_details', username=username))