import mysql.connector
from flask import render_template, request, Blueprint, session, flash, redirect
from app.verificador import group_verification
from ldap3 import Server, Connection, SIMPLE, ALL
from app.config import *


app = Blueprint('busca_radiusIP', __name__)

@app.route('/busca_radiusIP', methods=['POST', 'GET'])
def radiusconsulta2():
    result = group_verification()
    if result == True:
        pass
    else:
        return result
    

    # Obter lista de tabelas que começam com 'radacct' do banco de dados Radius1
    try:
        conn = mysql.connector.connect(**Radius1)
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute("SHOW TABLES LIKE 'radacct%'")
            results = cursor.fetchall()
            table_list = [table[0] for table in results]
            cursor.close()
            conn.close()
    except mysql.connector.Error as e:
        print(f'Erro ao conectar ao MySQL: {e}')

    tabela = request.form.get('table')
    inicio = request.form.get('datepicker')
    final = request.form.get('datepickerfinal')
    ip = request.form.get('ip')

    if request.method == 'POST':
        combined_results = []
        try:
            # Função para buscar resultados em todas as tabelas 'radacct' de um banco de dados
            def fetch_results_from_db(conn_config, table_list):
                results = []
                try:
                    conn = mysql.connector.connect(**conn_config)
                    if conn.is_connected():
                        for table in table_list:
                            cursor = conn.cursor()
                            query = f"""
                            SELECT username, acctstarttime, acctstoptime, framedipaddress, callingstationid
                            FROM {table}
                            WHERE acctstarttime BETWEEN %s AND %s
                            AND framedipaddress LIKE %s 
                            ORDER BY inet_aton(framedipaddress);
                            """
                            cursor.execute(query, (inicio, final, ip))
                            results.extend(cursor.fetchall())
                            cursor.close()
                        conn.close()
                except mysql.connector.Error as e:
                    flash('Busca realizada', 'success')
                return results

            # Buscar resultados nos dois bancos de dados
            results1 = fetch_results_from_db(Radius1, table_list)
            results2 = fetch_results_from_db(Radius2, table_list)

            combined_results = results1 + results2
            return render_template('buscaRadiusIP.html', results=combined_results, table_list=table_list )

        except mysql.connector.Error as e:
            flash('Erro ao conectar ao MySQL', 'error')

    return render_template('buscaRadiusIP.html', table_list=table_list)