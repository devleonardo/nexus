from flask import Flask
import mysql.connector.pooling

app = Flask(__name__)

## LDAP
LDAP_USER_CN = 'sistemasti'
LDAP_USER_PASSWORD = 'Leste@2023'

## ZABBIX
zUser = 'sistemasti'
zPassword = 'Leste@2023'

# PERMISSÃO PARA ACESSAR A PÁGINA DE PERMISSÃO DO MENU DNS
permissao = [
    "tiago_arruda",
    "gabriel_reis",
    "leonardo_martins",
    "leonardo_barchilon"
]

# PERMISSÃO PARA ACESSAR A PÁGINA DE PERMISSÃO DO MENU ZABBIX
permissao_azabbix = [
    "tiago_arruda",
    "gabriel_reis",
    "leonardo_martins",
    "leonardo_barchilon"
]

Radius1 = {
    'user': 'sistemas',
    'password': 'vYJy21!EY[a1',
    'host': '10.1.254.7',
    'database': 'radius',
    'raise_on_warnings': True
}
Radius2 = {
    'user': 'sistemas',
    'password': 'vYJy21!EY[a1',
    'host': '186.211.32.37',
    'database': 'radius',
    'raise_on_warnings': True
}

# Configuração do pool de conexões Do banco de dados 
dbconfig3= {
    "host": "192.168.100.168",
    "user": "proxmox",
    "password": "Leste@2023",
    "database": "sistemas"
}