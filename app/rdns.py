import dns.resolver
import ping3
from flask import Flask, render_template, request, Blueprint, redirect, url_for, session, jsonify
from app.verificador import group_verification
import subprocess
from os import system
from app.config import *

app = Blueprint('dashboard', __name__)

# RENDERIZA O DASHBOARD
@app.route('/dashboard')
def dashboard():
    # VERIFICA SE O USUÁRIO PERTENCE A ALGUM GRUPO DE ACESSO PARA A PÁGINA
    result = group_verification()
    if result == True:
        pass
    else:
        return result
    return render_template('dashboard.html')

# LITA PREDEFINIDA DE SERVIDORES DNS
dns_servers = {
    # "Google": "8.8.8.8",
    "Cloudflare": "1.1.1.1",
    "OpenDNS": "208.67.222.222",
    "RDNS-GRL-02": "186.211.32.186",
    "SJI-01": "186.211.32.93",
    "SJI-02": "200.202.111.93",
    "RDNS-MRC-01": "186.211.32.11",
    "RDNS-MRC-02": "200.202.111.11",
    "RDNS01": "186.211.32.58",
    "RDNS02": "186.211.32.98",
    "RDNS03": "186.211.32.59",
    "RDNS04": "186.211.32.56",
    "RDNS05": "200.202.111.58",
    "RDNS06": "200.202.111.98",
}
ordemping = []
@app.route('/dashboard', methods=['POST','GET'])
def resolve_domain():
    # VERIFICA SE O USUARIO ESTA LOGADO PARA ACESSAR A ROTA
    if not session.get('logged_in'):
        return redirect(url_for('rdns.login'))
    
    # PEGA O NOME DO USUARIO LOGADO NA SESSÃO PARA LOG APENAS
    usernameLST = session.get('usernameLST')

    # RECEBE O DOMINIO DIGITADO NO INPUT DO FRONT
    domain = request.form['domain']

    # LOG DE QUEM TESTOU E QUAL DOMINIO
    logger.info(f"Usuário: {usernameLST}, realizou um teste para {domain}")

    # ARMAZENA O RESULTADO
    results = []

    for dns_server_name, dns_server_ip in dns_servers.items():
        try:
            # RETORNA O PING
            ping_time = ping3.ping(dns_server_ip, timeout=3)
            if ping_time is not None:
                ping_time *= 1000
            # RESOLVE O DOMINIO E TEMPO DE RESOLUÇÃO
            resolver = dns.resolver.Resolver()
            resolver.nameservers = [dns_server_ip]
            # TEMPO PARA CADA RESPOSTA
            resolver.timeout = 5
            resolver.lifetime = 5

            # REALIZA UMA CONSULTA DNS PARA O DOMÍNIO / TIPO 'A' NA INTERNET 'IN'
            answer = resolver.query(domain, rdtype='A', rdclass='IN').response.to_text()

            # ESCREVE AS MENSAGENS DE SUCESSO, FALHA, TIMEOUT E ERRO
            results.append(f"<div class='alert alert-success' role='alert'><b>{dns_server_name}</b>: {domain}  <br><sucesso>Resolução de DNS bem-sucedida.</sucesso> <br><ping>Tempo de resolução: {round(ping_time)} ms</ping></div>")
        except dns.resolver.NXDOMAIN:
            ping_time_str = f"{round(ping_time)} ms" if ping_time is not None else "N/A"
            results.append(f"<div class='alert alert-danger' role='alert'><b>{dns_server_name}</b>: {domain}  <br><falha>Não foi possível resolver o nome do domínio.</falha> <br><ping>Tempo de resolução: {ping_time_str}</ping></div>")
        except dns.exception.Timeout:
            ping_time_str = f"{round(ping_time)} ms" if ping_time is not None else "N/A"
            results.append(f"<div class='alert alert-warning' role='alert'><b>{dns_server_name}</b>: {domain}  <br><timeout>Tempo limite de consulta atingido.</timeout> <br><ping>Tempo de resolução: {ping_time_str}</ping></div>")
        except dns.resolver.NoAnswer:
            ping_time_str = f"{round(ping_time)} ms" if ping_time is not None else "N/A"
            results.append(f"<div class='alert alert-secondary' role='alert'><b>{dns_server_name}</b>: {domain}  <br><sem>Não foi possível obter uma resposta para a consulta.</sem> <br><ping>Tempo de resolução: {ping_time_str}</ping></div>")
        except dns.exception.DNSException as e:
            results.append(f"<div class='alert alert-danger' role='alert'><b>{dns_server_name}</b>: {domain}  <br><errodns>Ocorreu um erro na consulta DNS</errodns></div>")
        except Exception as e:
            results.append(f"<div class='alert alert-danger' role='alert'><b>{dns_server_name}</b>: {domain}  <br><erro>Erro inesperado: {str(e)}</erro></div>")


    # NÃO EXIBE PING NEM CONVERTE A SAIDA PARA FLOAT AO DAR ERRO
    try:
        # EXPRESSÃO REGULAR PARA RETORNAR A MEDIA DO PING
        output = subprocess.getoutput(f"ping -c 4 {domain} | awk -F '/' '{{print $5}}'")
        # CONVERTE O RESULTADO EM PONTO FLUTUANTE
        convertFloat = float(output)
    except (ValueError, TypeError):
        # RETORNA O VALOR 0.0, CASO HAJA ERRO NO TESTE DE PING DEVIDO A TIMEOUTR OU BLOQUEIOS
        convertFloat = 0.0

    # RETORNA A LISTA ORDENADA EM HTML
    ordered_list = '<ul class="container row">' + ''.join([f'<li class="col-4">{result}</li>' for result in results]) + '</ul>'
    # RETORNA O TESTE DE PING NO TOPO DA PÁGINA
    ordemPing = '<div class="ping container">' + 'Latência média ' +'<vfinal>'+ ''.join([f'{round(convertFloat, 1)}']) +'</vfinal>'+ ' ms' + '</div>'
    # IMPRIME OS TESTE NA PAGINA RENDERIZADA
    return f"{dashboard()}{ordemPing}{ordered_list}"
