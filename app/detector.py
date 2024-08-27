import dns.resolver
from flask import Flask, render_template, request, Blueprint, redirect, url_for, session, jsonify, flash
from app.verificador import group_verification
from ldap3 import Server, Connection, SIMPLE, ALL
import ping3
import subprocess
from app.variavel_dns import *
from app.config import *

app = Blueprint('detector', __name__)

#######################################################
##           LISTA PREDEFINIDA DE DOMINIOS           ##
#######################################################
domains = [
    'sosbeta.lestetelecom.com.br',
    'clicksign.com',
    'web.whatsapp.com',
    'netflix.com',
    'youtube.com.br',
    'globoplay.globo.com',
    'primevideo.com',
    'facebook.com.br',
    'instagram.com.br',
    'bancointer.com.br',
    'nubank.com.br',
    'disneyplus.com',
    'bradesco.com.br',
    'santander.com.br',
    'lombinhosprime.com.br',
]

#######################################################
##        LISTA PREDEFINIDA DE SERVIDORES DNS        ##
#######################################################
dns_servers = {
    # "Google": "8.8.8.8",
    "RDNS-GRL-02": "186.211.32.186",
    "SJI-01": "186.211.32.93",
    "SJI-02": "200.202.111.93",
    "MRC-01": "186.211.32.11",
    "MRC-02": "200.202.111.11",
    "RDNS-01": "186.211.32.58",
    "RDNS-02": "186.211.32.98",
    "RDNS-03": "186.211.32.59",
    "RDNS-04": "186.211.32.56",
    "RDNS-05": "200.202.111.58",
    "RDNS-06": "200.202.111.98",
}

#########################################################################################
## FUNÇÃO DE RESOLUÇÃO DE NOMES DE DOMÍNIOS PARA GERAÇÃO DE DASHBOARD DE MONITORAMENTO ##
#########################################################################################
@app.route('/detector', methods=['POST', 'GET'])
def resolve_domains():
    
    
    # VERIFICA SE O USUÁRIO PERTENCE A ALGUM GRUPO DE ACESSO PARA A PÁGINA
    result = group_verification()
    if result == True:
        pass
    else:
        return result
    
    # ARMAZENA O RESULTADO
    results = {}

    for dns_server_name, dns_server_ip in dns_servers.items():
        dns_server_results = []

        for domain in domains:
            try:
                # RESOLVE O DOMINIO E TEMPO DE RESOLUÇÃO
                resolver = dns.resolver.Resolver()
                resolver.nameservers = [dns_server_ip]
                # TEMPO PARA CADA RESPOSTA
                resolver.timeout = 5
                resolver.lifetime = 5

                try:
                    # ESCREVE AS MENSAGENS DE SUCESSO, FALHA, TIMEOUT E ERRO
                    answer = resolver.query(domain, rdtype='A', rdclass='IN').response.to_text()
                    dns_server_results.append({"domain": domain.split('.')[0], "status": "success"})

                except dns.resolver.NXDOMAIN:
                    dns_server_results.append({"domain": domain.split('.')[0], "status": "error"})
                except dns.exception.Timeout:
                    dns_server_results.append({"domain": domain.split('.')[0], "status": "timeout"})
                except dns.resolver.NoAnswer:
                    dns_server_results.append({"domain": domain.split('.')[0], "status": "error"})
                except dns.exception.DNSException as e:
                    dns_server_results.append({"domain": domain.split('.')[0], "status": "error"})

            ## LIDA COM QUALQUER EXCEÇÃO QUE OCORRA AO LIDAR COM O SERVIDOR DNS
            except Exception as e:
                dns_server_results.append({"domain": domain.split('.')[0], "status": "error"})

        ## ADICIONA OS RESULTADOS DO SERVIDOR DNS ATUAL AO DICIONÁRIO
        results[dns_server_name] = dns_server_results

    # RENDERIZA O DASHBOARD COM O RESULTADO
    return render_template('detector.html', results=results)
   
################################################################################################################
## FUNÇÃO DE RESOLUÇÃO DE NOMES DE DOMÍNIOS PARA GERAÇÃO DE DASHBOARD DE MONITORAMENTO PARA UM DNS ESPECÍFICO ##
################################################################################################################
@app.route('/detector/<dns_server_name>', methods=['GET'])
def view_dns_results(dns_server_name):

    nome = dns_server_name
    resultado = None


    # OBTÉM O NOME DE USUÁRIO DA SESSÃO
    usernameLST = session.get('usernameLST')
    passwordLST = session.get('passwordLST')

    # ARMAZENA O RESULTADO
    dns_server_results = []

    dns_server_ip = dns_servers.get(dns_server_name)
    if not dns_server_ip:
        return "DNS server not found.", 404

    for domain in domains:
        try:
            # RESOLVE O DOMINIO E TEMPO DE RESOLUÇÃO
            resolver = dns.resolver.Resolver()
            resolver.nameservers = [dns_server_ip]
            # TEMPO PARA CADA RESPOSTA
            resolver.timeout = 5
            resolver.lifetime = 5
            ping_time = ping3.ping(dns_server_ip, timeout=3) * 1000 if ping3.ping(dns_server_ip, timeout=3) else None

            try:
                # REALIZA UMA CONSULTA DNS PARA O DOMÍNIO / TIPO 'A' NA INTERNET 'IN'
                answer = resolver.query(domain, rdtype='A', rdclass='IN').response.to_text()
                
                # ESCREVE AS MENSAGENS DE SUCESSO, FALHA, TIMEOUT E ERRO
                dns_server_results.append({"domain": domain.split('.')[0], "status": "success", 'ping_time': round(ping_time, 2) if ping_time else None})

            except dns.resolver.NXDOMAIN:
                dns_server_results.append({"domain": domain.split('.')[0], "status": "danger", 'ping_time': 'N/A'})
            except dns.exception.Timeout:
                dns_server_results.append({"domain": domain.split('.')[0], "status": "warning", 'ping_time': 'N/A'})
            except dns.resolver.NoAnswer:
                dns_server_results.append({"domain": domain.split('.')[0], "status": "danger", 'ping_time': 'N/A'})
            except dns.exception.DNSException as e:
                dns_server_results.append({"domain": domain.split('.')[0], "status": "danger", 'ping_time': 'N/A'})

        ## LIDA COM QUALQUER EXCEÇÃO QUE OCORRA AO LIDAR COM O SERVIDOR DNS
        except Exception as e:
            dns_server_results.append({"domain": domain.split('.')[0], "status": "danger"})

    #COMPARAÇÃO COM OS NOMES DOS DNS PARA EXIBIR A INFORMAÇÃO DE ACORDO COM O NOME DO DNS
    if nome == "SJI-01":
        resultado = rdnssji01
    elif nome == "SJI-02":
        resultado = rdnssji02
    elif nome == "MRC-01":
        resultado = rdnsmrc1
    elif nome == "MRC-02":
        resultado = rdnsmrc2
    elif nome == "NIT-02":
        resultado = rdnsnit2
    elif nome == "RDNS-01":
        resultado = rdns01
    elif nome == "RDNS-02":
        resultado = rdns02
    elif nome == "RDNS-03":
        resultado = rdns03
    elif nome == "RDNS-04":
        resultado = rdns04
    elif nome == "RDNS-05":
        resultado = rdns05
    elif nome == "RDNS-06":
        resultado = rdns06
    
    if resultado is None:
        resultado = "<p>Sem informações</p>"
    
    return render_template('dns_server_results.html', dns_server_name=dns_server_name, results=dns_server_results, dns_server_ip=dns_server_ip, ping_time=ping_time, resultado=resultado)