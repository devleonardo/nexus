from app.config import *
from flask import Blueprint

app = Blueprint('confirm_form', __name__)

destino_confirm_dns_block = 'confirmacao_dns_block.txt'
# FUNÇÃO PARA LER O ARQUIVO DE LOG DO BLOQUEIO DNS EM TEMPO REAL E RETORNAR PRO JAVASCRIPT
@app.route('/confirm_form')
def confirm_form():
    with open(destino_confirm_dns_block, 'r') as confirm_file:
        confirm_data = confirm_file.read()
    return confirm_data

