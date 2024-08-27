from app.config import *
from flask import render_template, session, Blueprint

app = Blueprint('versao', __name__)

# RENDERIZA NOTAS DE VERSÃO
@app.route('/versao')
def versao(): 

    # CHECA SE O USUÁRIO ESTÁ LOGADO, CASO CONTRÁRIO, REDIRECIONA PARA A PÁGINA DE LOGIN
    if not session.get('logged_in'):
        return render_template('login.html')
    
    return render_template('versao.html')