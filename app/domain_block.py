from flask import Flask, render_template, request, Blueprint, redirect, url_for, session
import subprocess
from app.config import *

app = Blueprint('domain_block', __name__)

# RENDERIZA A HOME
@app.route('/domain_block', methods=['POST', 'GET'])
def domain_block(grl02, mrc01, mrc02, rdns01, rdns02, rdns03, rdns04, rdns05, rdns06, sji01, sji02):
    
    # OBTEM O NOME DE USUARIO DA SESSÃO
    usernameLST = session.get('usernameLST')

    if request.method == 'POST':
        inventory = "/home/usshd/Ansible/bloqueioDNS/inventory.yml"
        inventory_bkp = "/home/usshd/Ansible/backup-bloqueioDNS"

        destino = "cd /home/usshd/Ansible/bloqueioDNS"
        destino_bkp = "cd /home/usshd/Ansible/backup-bloqueioDNS"

        #RDNS-GRL-02
        if not grl02:
            pass
        else:
            comando_bkp = f"{destino_bkp} && ansible-playbook -i {inventory_bkp} playbook_grl02_bkp.yml"
            comando_att_anablock = f"{destino} && ansible-playbook -i {inventory} update_Nexus_anablock.yml"
            comando = f"{destino} && ansible-playbook -i {inventory} playbook_grl-02.yml"

            try:
                with open('bloqueio_dns.log', 'a') as log_file:
                    subprocess.check_call(comando_bkp, shell=True, stdout=log_file)
                    subprocess.check_call(comando, shell=True, stdout=log_file)
                    subprocess.check_call(comando_att_anablock, shell=True, stdout=log_file)
            except:
                msg_erro = "Erro ao executar bloqueio no RDNS-GRL-02"
                with open('bloqueio_dns.log', 'a') as log_file:
                    log_file.write(msg_erro)
                    pass

        #SJI-01
        if not sji01:
            pass
        else:
            comando_bkp = f"{destino_bkp} && ansible-playbook -i {inventory_bkp} playbook_sji01_bkp.yml"
            comando = f"{destino} && ansible-playbook -i {inventory} playbook_sji-01.yml"

            try:
                with open('bloqueio_dns.log', 'a') as log_file:
                    subprocess.check_call(comando_bkp, shell=True, stdout=log_file)
                    subprocess.check_call(comando, shell=True, stdout=log_file)
            except:
                msg_erro = "Erro ao executar bloqueio no SJI-01"
                with open('bloqueio_dns.log', 'a') as log_file:
                    log_file.write(msg_erro)
                    pass
        
        #SJI-02
        if not sji02:
            pass
        else:
            comando_bkp = f"{destino_bkp} && ansible-playbook -i {inventory_bkp} playbook_sji02_bkp.yml"
            comando = f"{destino} && ansible-playbook -i {inventory} playbook_sji-02.yml"

            try:
                with open('bloqueio_dns.log', 'a') as log_file:
                    subprocess.check_call(comando_bkp, shell=True, stdout=log_file)
                    subprocess.check_call(comando, shell=True, stdout=log_file)
            except:
                msg_erro = "Erro ao executar bloqueio no SJI-02"
                with open('bloqueio_dns.log', 'a') as log_file:
                    log_file.write(msg_erro)
                    pass
        
        #MRC-01
        if not mrc01:
            pass
        else:
            comando_bkp = f"{destino_bkp} && ansible-playbook -i {inventory_bkp} playbook_mrc01_bkp.yml"
            comando = f"{destino} && ansible-playbook -i {inventory} playbook_mrc-01.yml"

            try:
                with open('bloqueio_dns.log', 'a') as log_file:
                    subprocess.check_call(comando_bkp, shell=True, stdout=log_file)
                    subprocess.check_call(comando, shell=True, stdout=log_file)
            except:
                msg_erro = "Erro ao executar bloqueio no MRC-01"
                with open('bloqueio_dns.log', 'a') as log_file:
                    log_file.write(msg_erro)
                    pass
        
        #MRC-02
        if not mrc02:
            pass
        else:
            comando_bkp = f"{destino_bkp} && ansible-playbook -i {inventory_bkp} playbook_mrc02_bkp.yml"
            comando = f"{destino} && ansible-playbook -i {inventory} playbook_mrc-02.yml"

            try:
                with open('bloqueio_dns.log', 'a') as log_file:
                    subprocess.check_call(comando_bkp, shell=True, stdout=log_file)
                    subprocess.check_call(comando, shell=True, stdout=log_file)
            except:
                msg_erro = "Erro ao executar bloqueio no MRC-02"
                with open('bloqueio_dns.log', 'a') as log_file:
                    log_file.write(msg_erro)
                    pass
        
        #RDNS-01
        if not rdns01:
            pass
        else:
            comando_bkp = f"{destino_bkp} && ansible-playbook -i {inventory_bkp} playbook_rdns01_bkp.yml"
            comando = f"{destino} && ansible-playbook -i {inventory} playbook_rdns-01.yml"

            try:
                with open('bloqueio_dns.log', 'a') as log_file:
                    subprocess.check_call(comando_bkp, shell=True, stdout=log_file)
                    subprocess.check_call(comando, shell=True, stdout=log_file)
            except:
                msg_erro = "Erro ao executar bloqueio no RDNS-01"
                with open('bloqueio_dns.log', 'a') as log_file:
                    log_file.write(msg_erro) 
                    pass
        
        #RDNS-02
        if not rdns02:
            pass
        else:
            comando_bkp = f"{destino_bkp} && ansible-playbook -i {inventory_bkp} playbook_rdns02_bkp.yml"
            comando = f"{destino} && ansible-playbook -i {inventory} playbook_rdns-02.yml"

            try:
                with open('bloqueio_dns.log', 'a') as log_file:
                    subprocess.check_call(comando_bkp, shell=True, stdout=log_file)
                    subprocess.check_call(comando, shell=True, stdout=log_file)
            except:
                msg_erro = "Erro ao executar bloqueio no RDNS-02"
                with open('bloqueio_dns.log', 'a') as log_file:
                    log_file.write(msg_erro)
                    pass
        
        #RDNS-03
        if not rdns03:
            pass
        else:
            comando_bkp = f"{destino_bkp} && ansible-playbook -i {inventory_bkp} playbook_rdns03_bkp.yml"
            comando = f"{destino} && ansible-playbook -i {inventory} playbook_rdns-03.yml"

            try:
                with open('bloqueio_dns.log', 'a') as log_file:
                    subprocess.check_call(comando_bkp, shell=True, stdout=log_file)
                    subprocess.check_call(comando, shell=True, stdout=log_file)
            except:
                msg_erro = "Erro ao executar bloqueio no RDNS-03"
                with open('bloqueio_dns.log', 'a') as log_file:
                    log_file.write(msg_erro)
                    pass
        
        #RDNS-04
        if not rdns04:
            pass
        else:
            comando_bkp = f"{destino_bkp} && ansible-playbook -i {inventory_bkp} playbook_rdns04_bkp.yml"
            comando = f"{destino} && ansible-playbook -i {inventory} playbook_rdns-04.yml"
            
            try:
                with open('bloqueio_dns.log', 'a') as log_file:
                    subprocess.check_call(comando_bkp, shell=True, stdout=log_file)
                    subprocess.check_call(comando, shell=True, stdout=log_file)
            except:
                msg_erro = "Erro ao executar bloqueio no RDNS-04"
                with open('bloqueio_dns.log', 'a') as log_file:
                    log_file.write(msg_erro)
                    pass

        #RDNS-05
        if not rdns05:
            pass
        else:
            comando_bkp = f"{destino_bkp} && ansible-playbook -i {inventory_bkp} playbook_rdns05_bkp.yml"
            comando = f"{destino} && ansible-playbook -i {inventory} playbook_rdns-05.yml"

            try:
                with open('bloqueio_dns.log', 'a') as log_file:
                    subprocess.check_call(comando_bkp, shell=True, stdout=log_file)
                    subprocess.check_call(comando, shell=True, stdout=log_file)
            except:
                msg_erro = "Erro ao executar bloqueio no RDNS-05"
                with open('bloqueio_dns.log', 'a') as log_file:
                    log_file.write(msg_erro)
                    pass
        
        #RDNS-06
        confirmacao_redirect = "2"
        destino_terminal = "confirmacao_dns_block.txt"
        comando_bkp = f"{destino_bkp} && ansible-playbook -i {inventory_bkp} playbook_rdns06_bkp.yml"
        comando = f"{destino} && ansible-playbook -i {inventory} playbook_rdns-06.yml"
        if not rdns06:
            with open(destino_terminal, 'w') as confirmacao:
                confirmacao.write(confirmacao_redirect)
                pass
        else:
            try:
                with open('bloqueio_dns.log', 'a') as log_file:
                    subprocess.check_call(comando_bkp, shell=True, stdout=log_file)
                    subprocess.check_call(comando, shell=True, stdout=log_file)
                    logger.info(f"Usuário {usernameLST} realizou bloqueio de domínios.")
                with open(destino_terminal, 'w') as confirmacao:
                    confirmacao.write(confirmacao_redirect)
            except:
                msg_erro = "Erro ao executar bloqueio no RDNS-06"
                with open('bloqueio_dns.log', 'a') as log_file:
                    log_file.write(msg_erro)
                with open(destino_terminal, 'w') as confirmacao:
                    confirmacao.write(confirmacao_redirect)
                    pass

                
    
    return render_template('bloqueio_dns.html')