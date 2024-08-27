from flask import Flask
import logging
from app.passwd import *

app = Flask(__name__)

# INFORMAÇÕES DE CONEXÃO COM O LDAP
LDAP_HOST = 'ldap://10.1.254.15:389'
AD04 = '10.1.254.15'
LDAP_BASE_DN = 'DC=intranet,DC=leste'

# GRUPOS DE ACESSO AO NEXUS
# GRUPO TI
LDAP_GROUP_DN = 'CN=USERS_STI,OU=SISTEMASTI,DC=intranet,DC=leste'
# GRUPO GERAL
LDAP_GROUP_DN2 = 'CN=AcessoOTRS,OU=OTRS,DC=intranet,DC=leste'
# GRUPO TESTE
LDAP_GROUP_DN3 = 'CN=Users, OU=Usuarios, DC=intranet, DC=leste'
# GRUPO LIDERANÇA COMUNICAÇÃO
LDAP_GROUP_DN4 = 'CN=SUP_COMUNICACAO,OU=SISTEMASTI,DC=intranet,DC=leste'
# GRUPO LIDERANÇA RH
LDAP_GROUP_DN5 = 'CN=STI_RH,OU=SISTEMASTI,DC=intranet,DC=leste'
NX_CALLSUP = 'CN=NX_CALLSUP,OU=SISTEMASTI,DC=intranet,DC=leste'
CORPCallcenter = "CN=CORPCallcenter,OU=CORPORATIVO,DC=intranet,DC=leste"
NX_CALLBACK = 'CN=NX_CALLBACK,OU=SISTEMASTI,DC=intranet,DC=leste'
NX_CALLADM = 'CN=NX_CALLADM,OU=SISTEMASTI,DC=intranet,DC=leste'


source_path = "/home/usshd/Nexus/app/static/wallpaper/wallpaper.jpg"
# Note the use of double backslashes to escape them correctly in Python
# destination_path = "sistemasti@10.1.254.15:/\\\\intranet.leste\\\\wallpaper"
destination_path ="sistemasti@10.1.254.15:/\\\\intranet.leste\\\\sysvol\\\\intranet.leste\\\\wallpaper"

# INFORMAÇÕES DE CONEXÃO PARA API DE CRIAR HOST NO ZABBIX
zUrl = 'https://zabbix.lestetelecom.com.br/'
    
# AD
INTRANET = '@intranet.leste'

#GERAÇÃO DE LOG DO NEXUS
#CONFIGURA O LOGGER PERSONALIZADO
logger = logging.getLogger('nexus')
#DEFINE O NIVEL DO LOGGER
logger.setLevel(logging.DEBUG)
#CRIA UM HANDLER PARA GRAVAR NO ARQUIVO LOG
handler = logging.FileHandler('nexus.log')
#DEFINE O FORMATO DAS MENSAGENS NO LOG
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
#DICIONA O HANDLER AO LOGGER
logger.addHandler(handler)
# logging.basicConfig(filename='nexus.log', level=logging.DEBUG)

#GERAÇÃO DE LOG DO NEXUS-DEBUG
#CONFIGURA O LOGGER PERSONALIZADO
logger_debug = logging.getLogger('nexus_debug')
#DEFINE O NIVEL DO LOGGER
logger_debug.setLevel(logging.DEBUG)
#CRIA UM HANDLER PARA GRAVAR NO ARQUIVO LOG
handler_debug = logging.FileHandler('nexus_debug.log')
#DICIONA O HANDLER AO LOGGER
logger_debug.addHandler(handler_debug)
logging.basicConfig(filename='nexus_debug.log', level=logging.DEBUG)