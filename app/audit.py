from flask import Flask, render_template, request, redirect, url_for, Blueprint, session, flash
from ldap3 import Server, Connection, SIMPLE, ALL, Attribute, MODIFY_REPLACE, Entry, NTLM
from app.config import *
from app.verificador import group_verification

app = Blueprint('audit', __name__)

@app.route('/audit')
def base():
    result = group_verification()
    if result == True:
        pass
    else:
        return result

    with open('./nexus.log') as log_file:
        return render_template('audit.html', log_file=log_file )