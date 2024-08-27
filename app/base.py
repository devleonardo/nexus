from app.config import *
from flask import render_template, request, redirect, url_for, session
from ldap3 import Server, Connection, SIMPLE, ALL, MODIFY_REPLACE, SUBTREE, MODIFY_DELETE
import subprocess
import pytz
app = Flask(__name__)

# RENDERIZA O MENU E ESTILOS DA APLICAÇÃO
@app.route('/base')
def base():
    return render_template('base.html')