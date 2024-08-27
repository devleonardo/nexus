from flask import render_template, request, Blueprint, session, flash, send_file, redirect
from ldap3 import Server, Connection, SIMPLE, ALL
import subprocess
from app.config import *
from app.verificador import group_verification
from openpyxl import Workbook
import io

app = Blueprint('ponto_grd', __name__)

# RENDERIZA O DASHBOARD
@app.route('/ponto_grd')
def url_busca():
    # CHECA SE O USUÁRIO ESTÁ LOGADO, CASO CONTRÁRIO, REDIRECIONA PARA A PÁGINA DE LOGIN
    result = group_verification()
    if result == True:
        pass
    else:
        return result
    return render_template('ponto_grd.html')
