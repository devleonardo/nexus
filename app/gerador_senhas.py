from flask import Flask, render_template, request, Blueprint, redirect, url_for, session

app = Blueprint('gerador_senhas', __name__)

# RENDERIZA A HOME
@app.route('/gerador_senhas')
def gerador_senhas():

    # CHECA SE O USUÁRIO ESTÁ LOGADO, CASO CONTRÁRIO, REDIRECIONA PARA A PÁGINA DE LOGIN
    if not session.get('logged_in'):
        return render_template('login.html')
    
    return render_template('gerador_senhas.html')