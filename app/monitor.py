from flask import render_template, Blueprint, session, redirect, url_for

app = Blueprint('monitor', __name__)

#Renderiza a página HTML
@app.route('/monitor')
def home():
    # CHECA SE O USUÁRIO ESTÁ LOGADO, CASO CONTRÁRIO, REDIRECIONA PARA A PÁGINA DE LOGIN
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    return render_template('monitor.html')