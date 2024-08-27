from flask import Flask, render_template, request, Blueprint, redirect, url_for, session
import subprocess
from app.config import *

app = Blueprint('dns_revert', __name__)

# RENDERIZA A HOME
@app.route('/dns_revert', methods=['POST', 'GET'])
def dns_revert(grl02, mrc01, mrc02, rdns01, rdns02, rdns03, rdns04, rdns05, rdns06, sji01, sji02):
    
    # OBTEM O NOME DE USUARIO DA SESSÃO
    usernameLST = session.get('usernameLST')
    
    if request.method == 'POST':
        destino = "cd /home/usshd/Ansible/reversao-bloqueioDNS/"

        #GRL-02
        if not grl02:
            pass
        else:
            comando = f"{destino} && ansible-playbook apontamento_grl02_revert.yml"

            try:
                with open('bloqueio_dns.log', 'a') as log_file:
                    subprocess.check_call(comando, shell=True, stdout=log_file)
            except:
                msg_erro = "Erro ao executar reversão no RDNS-GRL-02"
                with open('bloqueio_dns.log', 'a') as log_file:
                    log_file.write(msg_erro)
                    pass

        #SJI-01
        if not sji01:
            pass
        else:
            comando = f"{destino} && ansible-playbook playbook_sji01_revert.yml"

            try:
                with open('bloqueio_dns.log', 'a') as log_file:
                    subprocess.check_call(comando, shell=True, stdout=log_file)
            except:
                msg_erro = "Erro ao executar reversão no SJI-01"
                with open('bloqueio_dns.log', 'a') as log_file:
                    log_file.write(msg_erro)
                    pass

        #SJI-02
        if not sji02:
            pass
        else:
            comando = f"{destino} && ansible-playbook playbook_sji02_revert.yml"

            try:
                with open('bloqueio_dns.log', 'a') as log_file:
                    subprocess.check_call(comando, shell=True, stdout=log_file)
            except:
                msg_erro = "Erro ao executar reversão no SJI-02"
                with open('bloqueio_dns.log', 'a') as log_file:
                    log_file.write(msg_erro)
                    pass

        #MRC-01
        if not mrc01:
            pass
        else:
            comando = f"{destino} && ansible-playbook playbook_mrc01_revert.yml"

            try:
                with open('bloqueio_dns.log', 'a') as log_file:
                    subprocess.check_call(comando, shell=True, stdout=log_file)
            except:
                msg_erro = "Erro ao executar reversão no MRC-01"
                with open('bloqueio_dns.log', 'a') as log_file:
                    log_file.write(msg_erro)
                    pass

        #MRC-02
        if not mrc02:
            pass
        else:
            comando = f"{destino} && ansible-playbook playbook_mrc02_revert.yml"

            try:
                with open('bloqueio_dns.log', 'a') as log_file:
                    subprocess.check_call(comando, shell=True, stdout=log_file)
            except:
                msg_erro = "Erro ao executar reversão no MRC-02"
                with open('bloqueio_dns.log', 'a') as log_file:
                    log_file.write(msg_erro)
                    pass

        #RDNS-01
        if not rdns01:
            pass
        else:
            comando = f"{destino} && ansible-playbook playbook_rdns01_revert.yml"

            try:
                with open('bloqueio_dns.log', 'a') as log_file:
                    subprocess.check_call(comando, shell=True, stdout=log_file)
            except:
                msg_erro = "Erro ao executar reversão no RDNS-01"
                with open('bloqueio_dns.log', 'a') as log_file:
                    log_file.write(msg_erro)
                    pass

        #RDNS-02
        if not rdns02:
            pass
        else:
            comando = f"{destino} && ansible-playbook playbook_rdns02_revert.yml"

            try:
                with open('bloqueio_dns.log', 'a') as log_file:
                    subprocess.check_call(comando, shell=True, stdout=log_file)
            except:
                msg_erro = "Erro ao executar reversão no RDNS-02"
                with open('bloqueio_dns.log', 'a') as log_file:
                    log_file.write(msg_erro)
                    pass

        #RDNS-03
        if not rdns03:
            pass
        else:
            comando = f"{destino} && ansible-playbook playbook_rdns03_revert.yml"
            
            try:
                with open('bloqueio_dns.log', 'a') as log_file:
                    subprocess.check_call(comando, shell=True, stdout=log_file)
            except:
                msg_erro = "Erro ao executar reversão no RDNS-03"
                with open('bloqueio_dns.log', 'a') as log_file:
                    log_file.write(msg_erro)
                    pass

        #RDNS-04
        if not rdns04:
            pass
        else:
            comando = f"{destino} && ansible-playbook playbook_rdns04_revert.yml"

            try:
                with open('bloqueio_dns.log', 'a') as log_file:
                    subprocess.check_call(comando, shell=True, stdout=log_file)
            except:
                msg_erro = "Erro ao executar reversão no RDNS-04"
                with open('bloqueio_dns.log', 'a') as log_file:
                    log_file.write(msg_erro)
                    pass

        #RDNS-05
        if not rdns05:
            pass
        else:
            comando = f"{destino} && ansible-playbook playbook_rdns05_revert.yml"

            try:
                with open('bloqueio_dns.log', 'a') as log_file:
                    subprocess.check_call(comando, shell=True, stdout=log_file)
            except:
                msg_erro = "Erro ao executar reversão no RDNS-05"
                with open('bloqueio_dns.log', 'a') as log_file:
                    log_file.write(msg_erro)
                    pass

        #RDNS-06
        confirmacao_redirect = "2"
        destino_terminal = "confirmacao_dns_block.txt"
        comando = f"{destino} && ansible-playbook playbook_rdns06_revert.yml"
        if not rdns06:
            with open(destino_terminal, 'w') as confirmacao:
                confirmacao.write(confirmacao_redirect)
                pass
        else:
            try:
                with open('bloqueio_dns.log', 'a') as log_file:
                    subprocess.check_call(comando, shell=True, stdout=log_file)
                    logger.info(f"Usuário {usernameLST} reverteu o último bloqueio de domínios realizado.")
                with open(destino_terminal, 'w') as confirmacao:
                    confirmacao.write(confirmacao_redirect)
            except:
                msg_erro = "Erro ao executar reversão no RDNS-06"
                with open('bloqueio_dns.log', 'a') as log_file:
                    log_file.write(msg_erro)
                with open(destino_terminal, 'w') as confirmacao:
                    confirmacao.write(confirmacao_redirect)
                    pass

    return render_template('bloqueio_dns.html')