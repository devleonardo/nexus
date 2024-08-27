from app.config import *
from app.verificador import group_verification
from flask import render_template, request, session, Blueprint, flash, redirect
import subprocess
import os
from PIL import Image

app = Blueprint('adwall', __name__)


# RENDERIZA O MENU E ESTILOS DA APLICAÇÃO
@app.route('/adwall', methods=['POST','GET'])
def ad_wall(): 

    # VERIFICA SE O USUÁRIO PERTENCE A ALGUM GRUPO DE ACESSO PARA A PÁGINA
    result = group_verification()
    if result == True:
        pass
    else:
        return result
    
    # # OBTÉM O NOME DE USUÁRIO DA SESSÃO
    usernameLST = session.get('usernameLST')
    # passwordLST = session.get('passwordLST')
    
    # RECEBE A IMAGEM PELO INPUT NA INTERFACE WEB
    if request.method == 'POST':
        
        try:
            #Caminho onde a imagem será salva
            upload_folder = os.path.join(os.getcwd(), 'app/static/wallpaper')

            # Faz a requisição da imagem
            file = request.files['wallImagem']

            # Monta o formato e nome do arquivo a ser salvo no diretŕoio /wallpaper
            save_path = os.path.join(upload_folder, 'wallpaper.jpg')

            # Abre a imagem e armazena na variavel "image"
            image = Image.open(file)

            # Converte o esquema de cores da imagem para RGB (formato de cores do JPG)
            image = image.convert('RGB')

            # Salva a imagem no diretório de wallpaper
            image.save(save_path)

            # Envia o wallpaper para a pasta Imagens
            comando = f"sshpass -p '{LDAP_USER_PASSWORD}' scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null {source_path} {destination_path}"
            subprocess.check_output(comando, shell=True, text=True)

            logger.info(f"Usuário {usernameLST} alterou o wallpaper do AD.")

            flash('Wallpaper alterado!', 'success')
            return render_template('adwall.html')
        except:
            flash('Erro ao alterar wallpaper!', 'error')
            return render_template('adwall.html')
    return render_template('adwall.html')


# from app.config import *
# from flask import render_template, request, session, Blueprint, flash, redirect
# from ldap3 import Server, Connection, SIMPLE, ALL
# import subprocess
# import os
# from PIL import Image

# app = Blueprint('adwall', __name__)



# # RENDERIZA O MENU E ESTILOS DA APLICAÇÃO
# @app.route('/adwall', methods=['POST','GET'])
# def ad_wall(): 
#     # CHECA SE O USUÁRIO ESTÁ LOGADO, CASO CONTRÁRIO, REDIRECIONA PARA A PÁGINA DE LOGIN
#     if not session.get('logged_in'):
#         return render_template('login.html')

#     # OBTÉM O NOME DE USUÁRIO DA SESSÃO
#     usernameLST = session.get('usernameLST')
#     passwordLST = session.get('passwordLST')

#     # RECEBE A IMAGEM PELO INPUT NA INTERFACE WEB
#     if request.method == 'POST':
        
#         try:
#             #Caminho onde a imagem será salva
#             upload_folder = os.path.join(os.getcwd(), 'app/static/wallpaper')
#             # Faz a requisição da imagem
#             file = request.files['wallImagem']
#             # Monta o formato e nome do arquivo a ser salvo no diretŕoio /wallpaper
#             save_path = os.path.join(upload_folder, 'wallpaper.jpg')
#             # Abre a imagem e armazena na variavel "image"
#             image = Image.open(file)
#             # Converte o esquema de cores da imagem para RGB (formato de cores do JPG)
#             image = image.convert('RGB')
#             # Salva a imagem no diretório de wallpaper
#             image.save(save_path)
#             # Envia o wallpaper para a pasta Imagens
#             comando = f"sshpass -p '{LDAP_USER_PASSWORD}' scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null {source_path} {destination_path}"
#             subprocess.check_output(comando, shell=True, text=True)
#             logger.info(f"Usuário {usernameLST} alterou o wallpaper do AD.")
#             flash('Wallpaper alterado!', 'success')
#             return render_template('adwall.html')
#         except:
#             flash('Erro ao alterar wallpaper!', 'error')
#             return render_template('adwall.html')

#     # VERIFICA SE O USUÁRIO PERTENCE AO GRUPO LDAP_GROUP_DN
#     server = Server(LDAP_HOST, use_ssl=True, get_info=ALL)
#     conn = Connection(server, user=f"{usernameLST}{INTRANET}", password=passwordLST, authentication=SIMPLE, auto_bind=True)

#     search_filter = f'(&(sAMAccountName={usernameLST})(|(memberOf={LDAP_GROUP_DN})(memberOf={LDAP_GROUP_DN4})))'
#     conn.search(LDAP_BASE_DN, search_filter, attributes=['sAMAccountName'])

#     # SE O USUÁRIO PERTENCER AO GRUPO, RENDERIZA A PÁGINA
#     if len(conn.entries) > 0:
#         return render_template('adwall.html')
#     else:
#         # CASO CONTRÁRIO, REDIRECIONA PARA A PÁGINA DE LOGIN

#         flash('Você não tem permissão de acesso!', 'error')
#         return redirect(request.referrer)