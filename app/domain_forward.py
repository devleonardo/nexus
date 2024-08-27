from flask import Flask, render_template, request, Blueprint, redirect, url_for, session
import subprocess
from app.config import *

app = Blueprint('domain_forward', __name__)

# RENDERIZA A HOME
@app.route('/domain_forward', methods=['POST', 'GET'])
def domain_forward(grl02, itb02, mrc01, mrc02, nit01, rdns01, rdns02, rdns03, rdns04, rdns05, rdns06, sji01, sji02):
    
    # OBTEM O NOME DE USUARIO DA SESSÃO
    usernameLST = session.get('usernameLST')
    
    if request.method == 'POST':
        destino = "cd /home/usshd/Ansible/apontamentoDNS"
        destino_bkp = "cd /home/usshd/Ansible/backup-apontamentoDNS"
        
        #RDNS-GRL-02
        if not grl02:
            pass
        else:
            comando_bkp = f"{destino_bkp} && ansible-playbook apontamento_grl02_bkp.yml"
            comando = f"{destino} && ansible-playbook apontamento_grl-02.yml"

            try:
                with open('bloqueio_dns.log', 'a') as log_file:
                    subprocess.check_call(comando_bkp, shell=True, stdout=log_file)
                    subprocess.check_call(comando, shell=True, stdout=log_file)
            except:
                msg_erro = "Erro ao executar apontamento no RDNS-GRL-02"
                with open('bloqueio_dns.log', 'a') as log_file:
                    log_file.write(msg_erro)
                    pass

        #SJI-01
        if not sji01:
            pass
        else:
            comando_bkp = f"{destino_bkp} && ansible-playbook apontamento_sji01_bkp.yml"
            comando = f"{destino} && ansible-playbook apontamento_sji-01.yml"

            try:
                with open('bloqueio_dns.log', 'a') as log_file:
                    subprocess.check_call(comando_bkp, shell=True, stdout=log_file)
                    subprocess.check_call(comando, shell=True, stdout=log_file)
            except:
                msg_erro = "Erro ao executar apontamento no SJI-01"
                with open('bloqueio_dns.log', 'a') as log_file:
                    log_file.write(msg_erro)
                    pass
        
        #SJI-02
        if not sji02:
            pass
        else:
            comando_bkp = f"{destino_bkp} && ansible-playbook apontamento_sji02_bkp.yml"
            comando = f"{destino} && ansible-playbook apontamento_sji-02.yml"

            try:
                with open('bloqueio_dns.log', 'a') as log_file:
                    subprocess.check_call(comando_bkp, shell=True, stdout=log_file)
                    subprocess.check_call(comando, shell=True, stdout=log_file)
            except:
                msg_erro = "Erro ao executar apontamento no SJI-02"
                with open('bloqueio_dns.log', 'a') as log_file:
                    log_file.write(msg_erro)
                    pass
        
        #MRC-01
        if not mrc01:
            pass
        else:
            comando_bkp = f"{destino_bkp} && ansible-playbook apontamento_mrc01_bkp.yml"
            comando = f"{destino} && ansible-playbook apontamento_mrc-01.yml"

            try:
                with open('bloqueio_dns.log', 'a') as log_file:
                    subprocess.check_call(comando_bkp, shell=True, stdout=log_file)
                    subprocess.check_call(comando, shell=True, stdout=log_file)
            except:
                msg_erro = "Erro ao executar apontamento no MRC-01"
                with open('bloqueio_dns.log', 'a') as log_file:
                    log_file.write(msg_erro)
                    pass
        
        #MRC-02
        if not mrc02:
            pass
        else:
            comando_bkp = f"{destino_bkp} && ansible-playbook apontamento_mrc02_bkp.yml"
            comando = f"{destino} && ansible-playbook apontamento_mrc-02.yml"

            try:
                with open('bloqueio_dns.log', 'a') as log_file:
                    subprocess.check_call(comando_bkp, shell=True, stdout=log_file)
                    subprocess.check_call(comando, shell=True, stdout=log_file)
            except:
                msg_erro = "Erro ao executar apontamento no MRC-02"
                with open('bloqueio_dns.log', 'a') as log_file:
                    log_file.write(msg_erro)
                    pass
                
        #RDNS-01
        if not rdns01:
            pass
        else:
            comando_bkp = f"{destino_bkp} && ansible-playbook apontamento_rdns01_bkp.yml"
            comando = f"{destino} && ansible-playbook apontamento_rdns-01.yml"

            try:
                with open('bloqueio_dns.log', 'a') as log_file:
                    subprocess.check_call(comando_bkp, shell=True, stdout=log_file)
                    subprocess.check_call(comando, shell=True, stdout=log_file)
            except:
                msg_erro = "Erro ao executar apontamento no RDNS-01"
                with open('bloqueio_dns.log', 'a') as log_file:
                    log_file.write(msg_erro) 
                    pass
        
        #RDNS-02
        if not rdns02:
            pass
        else:
            comando_bkp = f"{destino_bkp} && ansible-playbook apontamento_rdns02_bkp.yml"
            comando = f"{destino} && ansible-playbook apontamento_rdns-02.yml"

            try:
                with open('bloqueio_dns.log', 'a') as log_file:
                    subprocess.check_call(comando_bkp, shell=True, stdout=log_file)
                    subprocess.check_call(comando, shell=True, stdout=log_file)
            except:
                msg_erro = "Erro ao executar apontamento no RDNS-02"
                with open('bloqueio_dns.log', 'a') as log_file:
                    log_file.write(msg_erro)
                    pass
        
        #RDNS-03
        if not rdns03:
            pass
        else:
            comando_bkp = f"{destino_bkp} && ansible-playbook apontamento_rdns03_bkp.yml"
            comando = f"{destino} && ansible-playbook apontamento_rdns-03.yml"

            try:
                with open('bloqueio_dns.log', 'a') as log_file:
                    subprocess.check_call(comando_bkp, shell=True, stdout=log_file)
                    subprocess.check_call(comando, shell=True, stdout=log_file)
            except:
                msg_erro = "Erro ao executar apontamento no RDNS-03"
                with open('bloqueio_dns.log', 'a') as log_file:
                    log_file.write(msg_erro)
                    pass
        
        #RDNS-04
        if not rdns04:
            pass
        else:
            comando_bkp = f"{destino_bkp} && ansible-playbook apontamento_rdns04_bkp.yml"
            comando = f"{destino} && ansible-playbook apontamento_rdns-04.yml"
            
            try:
                with open('bloqueio_dns.log', 'a') as log_file:
                    subprocess.check_call(comando_bkp, shell=True, stdout=log_file)
                    subprocess.check_call(comando, shell=True, stdout=log_file)
            except:
                msg_erro = "Erro ao executar apontamento no RDNS-04"
                with open('bloqueio_dns.log', 'a') as log_file:
                    log_file.write(msg_erro)
                    pass

        #RDNS-05
        if not rdns05:
            pass
        else:
            comando_bkp = f"{destino_bkp} && ansible-playbook apontamento_rdns05_bkp.yml"
            comando = f"{destino} && ansible-playbook apontamento_rdns-05.yml"

            try:
                with open('bloqueio_dns.log', 'a') as log_file:
                    subprocess.check_call(comando_bkp, shell=True, stdout=log_file)
                    subprocess.check_call(comando, shell=True, stdout=log_file)
            except:
                msg_erro = "Erro ao executar apontamento no RDNS-05"
                with open('bloqueio_dns.log', 'a') as log_file:
                    log_file.write(msg_erro)
                    pass
        
        #RDNS-06
        confirmacao_redirect = "2"
        destino_terminal = "confirmacao_dns_block.txt"
        comando_bkp = f"{destino_bkp} && ansible-playbook apontamento_rdns06_bkp.yml"
        comando = f"{destino} && ansible-playbook apontamento_rdns-06.yml"
        if not rdns06:
            with open(destino_terminal, 'w') as confirmacao:
                confirmacao.write(confirmacao_redirect)
                pass
        else:
            try:
                with open('bloqueio_dns.log', 'a') as log_file:
                    subprocess.check_call(comando_bkp, shell=True, stdout=log_file)
                    subprocess.check_call(comando, shell=True, stdout=log_file)
                    logger.info(f"Usuário {usernameLST} realizou apontamento de domínios.")
                with open(destino_terminal, 'w') as confirmacao:
                    confirmacao.write(confirmacao_redirect)
            except:
                msg_erro = "Erro ao executar apontamento no RDNS-06"
                with open('bloqueio_dns.log', 'a') as log_file:
                    log_file.write(msg_erro)
                with open(destino_terminal, 'w') as confirmacao:
                    confirmacao.write(confirmacao_redirect)
                    pass

                
    
    return render_template('apontamento_dns.html')