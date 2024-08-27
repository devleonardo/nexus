from flask import render_template, request, Blueprint, session, flash, redirect
from ldap3 import Server, Connection, SIMPLE, ALL
from app.config import *
from app.verificador import group_verification

app = Blueprint('freeipa_servers', __name__)

# Configuração do pool de conexões Do banco de dados 
class ConnectionPool:
    def __init__(self):
        self.pool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name="mypool",
            pool_size=1,  # Número máximo de conexões no pool
            **dbconfig3
        )

    def get_connection(self):
        return self.pool.get_connection()

connection_pool = ConnectionPool()

@app.route('/freeipa_servers', methods=['GET', 'POST'])
def freeipa_servers():
    
    # Checa se o usuário está logado, caso contrário, redireciona para a página de login
    result = group_verification()
    if result == True:
        pass
    else:
        return result
    # Se o usuário pertencer ao grupo, renderiza a página de busca
    results = linstandoservidores()
    return render_template('freeipa_servers.html', results=results)



def linstandoservidores():
            # Conecta ao banco de dados MySQL
        db_conection = connection_pool.get_connection()

        # Cria um cursor para executar consultas SQL
        cursor = db_conection.cursor()
   
        # Executa uma consulta SQL para selecionar
        cursor.execute("SELECT id_server, name_server, addtime FROM servidoresintDB")
        
        # Obtém os resultados da consulta
        results = cursor.fetchall()
            
        # Fecha a conexão com o banco de dados
        db_conection.close()

        return results
    

#Função para listar os usuarios do freeipa
def freeipausers():

    # Conectar ao servidor LDAP
    server = Server(server_url, use_ssl=False)  # Ajuste use_ssl para True se necessário
    conn = Connection(server, user=bind_dn, password=bind_password, auto_bind=True)

    # Fazer a consulta LDAP para listar usuários
    conn.search(search_base, '(objectClass=posixAccount)', attributes=['uid', 'nsAccountLock'])

    results = []

    # Processar os resultados
    if conn.entries:
        for entry in conn.entries:
            if 'uid' in entry and 'nsAccountLock' in entry:
                username = entry['uid'].value
                is_active = not entry['nsAccountLock'].value  # Verifica se a conta não está bloqueada
                results.append({'username': username, 'active': is_active})

    else:
        print("Nenhum usuário encontrado.")

    # Fechar a conexão LDAP
    conn.unbind()

    if results:
        try:
            # Conecte ao banco de dados MySQL
            db_connection = connection_pool.get_connection()
            # Crie um cursor para executar consultas SQL
            cursor = db_connection.cursor()

            # Itere sobre os resultados e insira-os na tabela do banco de dados
            for vm_data in results:
                    sql = 'INSERT INTO user (username, ativo) VALUES (%s, %s)' \
                          'ON DUPLICATE KEY UPDATE username = VALUES(username)'
                    cursor.execute(sql, (vm_data['username'], vm_data['active']))

            # Comita a transação
            db_connection.commit()

        except Exception as e:
            # Em caso de erro, desfaz a transação
            db_connection.rollback()
            print(f"Erro ao inserir dados: {e}")

        finally:
            # Feche o cursor e a conexão com o banco de dados
            cursor.close()
            db_connection.close()


    # Conectar ao servidor LDAP
    server = Server(server_url, use_ssl=True)
    conn = Connection(server, user=bind_dn, password=bind_password, auto_bind=True)

    # Fazer a consulta LDAP para listar hosts
    conn.search(search_base, '(objectClass=ipaHost)', attributes=ALL_ATTRIBUTES)
    servidores = []
    
    # Processar os resultados
    if conn.entries:
        for entry in conn.entries:
            if 'fqdn' in entry:
                fqdn = entry['fqdn'].value
                # Extrair o nome de host até o primeiro ponto
                hostname = fqdn.split('.')[0]  # Pega apenas a primeira parte do FQDN
                servidores.append(hostname)

    else:
        print("Nenhum host encontrado.")

    # Fechar a conexão LDAP
    conn.unbind()

    if servidores:
        try:
            # Conecte ao banco de dados MySQL
            db_connection = connection_pool.get_connection()
            # Crie um cursor para executar consultas SQL
            cursor = db_connection.cursor()
            # Itere sobre os resultados e insira-os na tabela do banco de dados
            for vm_data in servidores:
                sql = '''
                INSERT INTO servidoresintDB(name_server, addtime)
                VALUES (%s, NOW())
                ON DUPLICATE KEY UPDATE name_server = VALUES(name_server)
                '''
                cursor.execute(sql, (vm_data,))

            # Comita a transação
            db_connection.commit()

        except Exception as e:
            # Em caso de erro, desfaz a transação
            db_connection.rollback()
            print(f"Erro ao inserir dados: {e}")

        finally:
            # Feche o cursor e a conexão com o banco de dados
            cursor.close()
            db_connection.close()


    return results, servidores
