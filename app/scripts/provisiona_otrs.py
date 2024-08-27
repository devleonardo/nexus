from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys

def provisiona_otrs(username):
    otrs_url = "http://otrs01.lestetelecom.com.br/otrs/index.pl"
    username_otrs = username
    password_otrs = "Leste@2024"

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
    WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.NAME, "User")))
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
    # Aguarda até que o primeiro login seja feito
    WebDriverWait(driver, 50).until(EC.visibility_of_element_located((By.ID, "Navigation")))
    # Fecha o navegador
    driver.quit()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        username = sys.argv[1]
        provisiona_otrs(username)
    else:
        print("Erro ao executar provisionamento no OTRS")