from flask import Flask, render_template, request, Blueprint, redirect, url_for, session

app = Blueprint('home', __name__)

# RENDERIZA A HOME
@app.route('/home')
def home():
    # CHECA SE O USUÁRIO ESTÁ LOGADO, CASO CONTRÁRIO, REDIRECIONA PARA A PÁGINA DE LOGIN
    if not session.get('logged_in'):
        return render_template('login.html')
    
    return render_template('home.html')