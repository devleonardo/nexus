from app.config import *
from flask import Flask, render_template, request, Blueprint, redirect, url_for, session
import os
import subprocess
import time
import logging

app = Blueprint('bloqueio_dns_log', __name__)

# FUNÇAÕI PARA LER O ARQUIVO DE LOG DO BLOQUEIO DNS EM TEMPO REAL E RETORNAR PRO JAVASCRIPT
@app.route('/bloqueio_dns_log')
def get_log():
    with open('bloqueio_dns.log', 'r') as log_file:
        log_data = log_file.read()
    return log_data
