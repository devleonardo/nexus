from flask import render_template, request, Blueprint, session, flash
import requests
import re
from app.config import *
import ipaddress
from app.verificador import group_verification


app = Blueprint('subnet', __name__)

# RENDERIZA O DASHBOARD
@app.route('/subnet', methods=['GET','POST'])
def subnet():
    # VERIFICA SE O USUÁRIO PERTENCE A ALGUM GRUPO DE ACESSO PARA A PÁGINA
    result = group_verification()
    if result == True:
        pass
    else:
        return result
    
    # CASO LOGADO, RENDERIZA A PAGINA DASHBOARD
    if request.method == 'POST':
        ip = request.form.get('ip')
        mascara = request.form.get('cidr')
        return calcular_subnet(ip, mascara)
    return render_template('subnet.html')

def calcular_subnet(ip, mascara):
    
    # OBTENDO USUÁRIO DA SESSÃO
    usernameLST = session.get('usernameLST')
    
    try: 
        rede = ipaddress.ip_network(f'{ip}/{mascara}', strict=False)
    except ValueError:
        flash('Ip inválido!', 'error')
        return render_template('subnet.html')
    
    # Criando objeto da rede com IP e mascara fornecidos.
    
    network = rede.network_address
    broadcast = rede.broadcast_address
    mascara_rede = rede.netmask 

    if rede.num_addresses > 2:
        primeiro_host = network + 1
        ultimo_host = broadcast - 1
    else:
        primeiro_host = network
        ultimo_host = broadcast

    total_host = rede.num_addresses - 2 if rede.num_addresses > 2 else rede.num_addresses

    # Verifica se a rede é privada ou pública
    eh_privado = rede.is_private

    if eh_privado == True:
        eh_privado = "Privado"
    elif eh_privado == False:
        eh_privado = "Público"
    else:
        eh_privado = " N/A"


    logger.info(f'O usuário: {usernameLST}, realizou um calculo para: {ip}/{mascara}')

    flash('Calculo efetuado!', 'success')
        
    # IMPRIME OS TESTE NA PAGINA RENDERIZADA
    return render_template('subnet.html', ip=ip, total_host=total_host, network=network, mascara_rede=mascara_rede, broadcast=broadcast, primeiro_host=primeiro_host, ultimo_host=ultimo_host, eh_privado=eh_privado)