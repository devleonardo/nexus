from app.config import *
import subprocess
from flask import render_template, request, redirect, url_for, session, flash

def att_anablock():

    # inventário dos hosts para o playbook
    inventory = "/home/usshd/Ansible/anablock/inventory.yml"

    # comando para chamar o playbook master
    comando = f"ansible-playbook -i {inventory} /home/usshd/Ansible/anablock/att_anablock.yml"

    # DESTINO E VALORES DA VARIAVEL QUE ATIVA OU DESATIVA O TERMINAL NO MOMENTO DA EXECUÇÃO DO BLOQUEIO #

    # terminal ativo = 1, terminal inativo = 0, redirecionamento pós conclusão = 2
    destino_terminal = 'confirmacao_dns_block.txt'
    confirmacao_dns_block = '1'
    confirmacao_pos_block = '0'
    confirmacao_redirect = '2'
    ################################################################################################

    if request.method == "POST":
        try:
            with open(destino_terminal, 'w') as confirmacao:
                confirmacao.write(confirmacao_dns_block)
            with open('bloqueio_dns.log', 'a') as log_file:
                subprocess.check_call(comando, shell=True, stdout=log_file)
            flash('Atualização efetuada com sucesso!', 'success')
            return redirect(url_for("/dns_block_error"))
        except:
            msg_erro = "Erro ao executar atualização do Anablock"
            with open('bloqueio_dns.log', 'a') as log_file:
                log_file.write(msg_erro)
            flash('Erro ao executar atualização!', 'error')
            return redirect(url_for("/dns_block_error"))
