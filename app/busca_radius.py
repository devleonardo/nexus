import mysql.connector
from flask import render_template, request, Blueprint, session, flash, redirect
from ldap3 import Server, Connection, SIMPLE, ALL
from app.config import *
from app.verificador import group_verification

app = Blueprint('busca_radius', __name__)
# Função para converter bytes para GB
def bytes_to_gb(bytes_value):
    gb = bytes_value / (1024 * 1024 * 1024)
    if gb >= 1:
        return f"{round(gb, 2)} GB"
    else:
        mb = bytes_value / (1024 * 1024)
        return f"{round(mb, 2)} MB"
# Rota para realizar a consulta e renderizar o template
@app.route('/busca_radius', methods=['POST','GET'])
def radiusconsulta():
    # Checa se o usuário está logado, caso contrário, redireciona para a página de login
    result = group_verification()
    if result == True:
        pass
    else:
        return result

    # Obtém os parâmetros do formulário
    cliente = request.form.get('inputmacsearch')
    inicio = request.form.get('datepicker')
    final = request.form.get('datepickerfinal')
    
    if request.method == 'POST':
        try:
            # Tentar conectar ao primeiro banco de dados (Radius1)
            conn1 = mysql.connector.connect(**Radius1)
            if conn1.is_connected():
                cursor1 = conn1.cursor()
                query = """
                SELECT
                    acctstarttime AS Data_Inicio,
                    acctstoptime AS Data_Fim,
                    SUM(acctoutputoctets) AS total_download_gb,
                    SUM(acctinputoctets) AS total_upload_gb,
                    framedipaddress AS ip,
                    callingstationid AS mac
                    
                FROM 
                    radacct
                WHERE 
                    username = %s AND acctstarttime >= %s AND acctstarttime <= %s
                GROUP BY 
                    acctsessionid, acctstarttime, acctstoptime;
                """
                cursor1.execute(query, (cliente, inicio, final))
                results1 = cursor1.fetchall()
                formatted_results1 = []
                for row in results1:
                    formatted_row = list(row)
                    formatted_row[2] = bytes_to_gb(row[2])  # total_download_gb em GB
                    formatted_row[3] = bytes_to_gb(row[3])  # total_upload_gb em GB
                    formatted_results1.append(formatted_row)
                cursor1.close()
                conn1.close()
                # Se precisar buscar no segundo banco de dados (Radius2)
                conn2 = mysql.connector.connect(**Radius2)
                if conn2.is_connected():
                    cursor2 = conn2.cursor()
                    cursor2.execute(query, (cliente, inicio, final))
                    results2 = cursor2.fetchall()
                    formatted_results2 = []
                    for row in results2:
                        formatted_row = list(row)
                        formatted_row[2] = bytes_to_gb(row[2])  # total_download_gb em GB
                        formatted_row[3] = bytes_to_gb(row[3])  # total_upload_gb em GB
                        formatted_results2.append(formatted_row)
                    cursor2.close()
                    conn2.close()
                    # Combinar resultados de ambos os bancos de dados, se necessário
                    combined_results = formatted_results1 + formatted_results2
                    flash('Busca realizada', 'success')
                    return render_template('busca_radius.html', results=combined_results, cliente=cliente)
        except mysql.connector.Error as e:
            print(f'Erro ao conectar ao MySQL: {e}')
            flash('Erro ao conectar ao MySQL', 'error')
        finally:
            if 'conn1' in locals() and conn1.is_connected():
                cursor1.close()
                conn1.close()
            if 'conn2' in locals() and conn2.is_connected():
                cursor2.close()
                conn2.close()

    # Se o usuário pertencer ao grupo, renderiza a página de busca
    return render_template('busca_radius.html')