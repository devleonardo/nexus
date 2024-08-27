from app.config import * # IMPORTA AS VARIÁVEIS DE CONEXÃO E ACESSO, E BIBLIOTECA DO ARQUIVO DE CONFIGURAÇÃO
from flask import render_template, request, redirect, url_for, session, flash # WEB
from ldap3 import Server, Connection, SIMPLE, ALL, MODIFY_REPLACE, SUBTREE, MODIFY_DELETE # BIBLIOTECA DE CONEXÃO LDAP
import subprocess # BIBLIOTECA PARA COMANDOS LINUX
import pytz # MANIPULAÇÃO DE DATAS E HORAS
from app.edit_groups import edit_groups # FUNÇÃO PARA EDITAR GRUPOS


def user_details(username):

    # VERIFICA SE O USUARRIO ESTA LOGADO
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    # OBTEM O NOME DE USUARIO DA SESSÃO
    usernameLST = session.get('usernameLST')
    passwordLST = session.get('passwordLST')
    
    # RECUPERA OS DETALHES DO USUARIO DO SERVIDOR LDAP
    server = Server(LDAP_HOST, use_ssl=True, get_info=ALL)
    conn = Connection(server, f"{usernameLST}{INTRANET}", password=passwordLST, authentication=SIMPLE, auto_bind=True)
    
    # RECUPERA OS DETALHES DO USUARIO DO SERVIDOR LDAP
    search_filter = f'(sAMAccountName={username})'
    conn.search(LDAP_BASE_DN, search_filter, attributes=['physicalDeliveryOfficeName','employeeID', 'ipPhone', 'initials','sn','givenName','ou','cn','name', 'mail', 'displayName', 'description', 'sAMAccountName', 'userPrincipalName', 'memberOf', 'userAccountControl', 'distinguishedName', 'objectCategory', 'whenCreated', 'badPasswordTime', 'badPwdCount', 'lastLogoff', 'lastLogon', 'logonCount', 'pwdLastSet', 'whenCreated', 'whenChanged', 'accountExpires'])

    # LISTA OS GRUPOS DE PERMISSÕES DO USUÁRIO
    group_conn = Connection(server, user=LDAP_USER_CN, password=LDAP_USER_PASSWORD, authentication=SIMPLE, auto_bind=True)
    group_conn.search(LDAP_BASE_DN, '(objectClass=group)', search_scope=SUBTREE, attributes=['cn'])

    # TESTE
    grupos_ad = []
    for entry in group_conn.entries:
        grupo_ad = entry.entry_dn
        if 'OU=Frota' not in grupo_ad:
            grupos_ad.append(grupo_ad)


    # LISTA AS OUS DISPONÍVEIS PARA MOVIMENTAÇÃO DE ESTAÇÕES
    ou_conn = Connection(server, f"{usernameLST}{INTRANET}", password=passwordLST, authentication=SIMPLE, auto_bind=True)
    ou_conn.search(LDAP_BASE_DN, '(objectClass=organizationalUnit)', search_scope=SUBTREE, attributes=['ou'])

    # ADICIONA AS OUS DENTRO DE UM ARRAY
    ous = []
    for entry in ou_conn.entries:
        ou_named = entry.ou.value
        ous.append(ou_named)

    # LISTA AS OUS A SEREM REMOVIDAS DA VISUALIZAÇÃO
    ous_para_remover = ['Domain Controllers', 'SURICATA', 'VMWARE', 'WANGUARD', 'CAMERAS', 'OTRS', 'GRAFANA', 'GRAYLOG', 'RSYSLOG', 'ZABBIX', 'GERENCIA', 'CORPORATIVO', 'CACTI', 'OCS', 'LESTEVPN', 'GESTIOIP', 'FIREWALL', 'ELETRICA', 'Frota', 'IMPRESSAO', 'ATIVIDADES', 'HOMOLOGACAO', 'PABX', 'WIKI', 'RADIUS', 'BLOQUEIO', 'MIKROTIK', 'DATACOM', 'JUNIPER', 'HUAWEI', 'FIBERHOME', '3COM', 'HP', 'DELL', 'CLIENTES', 'DESBLOQUEIA', 'DESBLOQUEIO', 'CISCO', 'TPLINK', 'VMCLUSTERS', 'Local_admin', 'SYSPASS', 'GLPI', 'TELA', 'WIKITIC', 'SISTEMASTI', 'CALLCENTER TESTE', 'LAB', 'GLPIAgent', 'OU_TESTE_ADD']

    # REMOVE DA INTERFACE AS OUS LISTADAS ACIMA
    for ou in ous_para_remover: 
        if ou in ous:
            ous.remove(ou)
    
    # RECUPERA OS ATRIBUTOS DOS USUARIOS
    entry = conn.entries[0]
    user_attributes = entry.entry_attributes_as_dict
    
    # EXTRAINDO INFORMAÇÕES DO USUÁRIO / ESTAÇÃO
    username = entry.sAMAccountName.value # NOME DE USUÁRIO
    user_gn = entry.givenName.value # NOME
    user_sn = entry.sn.value # SOBRENOME
    user_init = entry.initials.value # INICIAIS
    agente_ip = entry.ipPhone.value # AGENTE IP
    cpf = entry.employeeID.value #CPF
    errou_senha = entry.badPasswordTime.value # ERRO DE SENHA
    ultimo_logon = entry.lastLogon.value # ULTIMO LOGON
    ultima_troca_sn = entry.pwdLastSet.value # ULTIMA TROCA DE SENHA
    data_criacao_user = entry.whenCreated.value # DATA DE CRIAÇÃO DO USUÁRIO
    data_modificacao_user = entry.whenChanged.value # ULTIMA MODIFICAÇÃO DO USUÁRIO
    data_expiracao_user = entry.accountExpires.value # EXPIRAÇÃO DO USUÁRIO
    description = entry.description.value if 'description' in entry else '' # DESCRIÇÃO DO USUÁRIO / FUNÇÃO
    email = entry.mail.value if 'mail' in entry else '' # EMAIL DO USUÁRIO
    member_of = user_attributes.get('memberOf', ['']) # GRUPO DE PERMISSÕES DO USUÁRIO

    # RECUPERA A OU ATUAL DA ESTAÇÃO
    atual_ou = entry.distinguishedName.value # OU ATUAL DA ESTAÇÃO

    # FILTA O NOME DA OU
    atual_ou_filtered = subprocess.getoutput(f"less {atual_ou} | awk -F '=' '{{print $3}}' | awk -F ',' '{{print $1}}'")

    # CHECANDO O STATUS DA CONTA
    user_account_control = int(user_attributes.get('userAccountControl', [0])[0]) # type: ignore
    is_account_enabled = not bool(user_account_control & 2) # type: ignore

    # LISTANDO GRUPOS DE PERMISSÕES
    groups = []
    for group in member_of:
        # group_name = subprocess.getoutput(f"less {group} | awk -F '=' '{{print $2}}' | awk -F ',' '{{print $1}}'")
        groups.append(group)
    
    connUserGroups = Connection(server, user=f"{usernameLST}{INTRANET}", password=passwordLST, authentication=SIMPLE, auto_bind=True)

    search_filter_TI = f'(sAMAccountName={usernameLST})'

    connUserGroups.search(LDAP_BASE_DN, search_filter_TI, attributes=['memberOf'])

    userGroups = []

    if connUserGroups.entries:
        user_entry = connUserGroups.entries[0]
        if 'memberOf' in user_entry:
            userGroups = user_entry['memberOf']
        if LDAP_GROUP_DN in userGroups:
            CCorTI = "ti"
        elif NX_CALLSUP in userGroups:
            CCorTI = "cc"

    if request.method == 'POST':
        # PEGANDO NOVOS DADOS DO USUÁRIO PARA ALTERAÇÃO
        new_name = request.form.get('nome')
        new_description = request.form.get('descricao')
        new_email = request.form.get('e_mail')
        new_sn = request.form.get('sn')
        new_init = request.form.get('init')
        new_agent = request.form.get('agente')
        new_cpf = request.form.get('cpf')
        new_login = request.form.get('userLogin')

        # NOVA OU PARA MOVER A ESTAÇÃO
        new_ou_cn = request.form.get('selected_ou')
        dn_ou = f"OU={new_ou_cn},DC=intranet,DC=leste"
        new_username = username.split("$")[0]
        new_ou = f"CN={new_username},{dn_ou}"

        # LOG DE ALTERAÇÕES DO USUÁRIO
        logger.info('--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
        logger.info(f"Usuário {usernameLST} realizou alteração em {username}.")
        logger.info(f"Nome: {user_gn} - Para {new_name}")
        logger.info(f"Sobrenome: {user_sn} - Para {new_sn}")
        logger.info(f"Iniciais: {user_init} - Para {new_init}")
        logger.info(f"Função: {description} - Para {new_description}")
        logger.info(f"Email: {email} - Para {new_email}")
        logger.info(f"Estação da OU: {atual_ou} - Para {new_ou}")
        logger.info(f"Novo Agente Ip Associado: {new_agent}")
        logger.info(f"CPF Associado: {new_cpf}")
        logger.info(f"Novo username: {new_login}")
        logger.info('--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
        
        # PREPARA AS MODIFICAÇÕES A SEREM FEITAS NA ENTRADA DO USUARIO
        modifications = {}
        if new_name is not None:
            modifications['givenName'] = [(MODIFY_REPLACE, [new_name])]
        if new_description is not None:
            modifications['description'] = [(MODIFY_REPLACE, [new_description])]
        if new_email is not None:
            modifications['mail'] = [(MODIFY_REPLACE, [new_email])]
        if new_sn is not None:
            modifications['sn'] = [(MODIFY_REPLACE, [new_sn])]
        if new_init is not None:
            modifications['initials'] = [(MODIFY_REPLACE, [new_init])]
        if new_agent is not None:
            modifications['ipPhone'] = [(MODIFY_REPLACE, [new_agent])]
        if new_cpf is not None:
            modifications['employeeID'] = [(MODIFY_REPLACE, [new_cpf])]
        if new_username is not None:
            modifications['sAMAccountName'] = [(MODIFY_REPLACE, [new_login])]

        # MODIFICA A ENTRADA DO USUARIO NO SERVIDOR LDAP
        if not "OU=None" in new_ou:
            atual_ou = new_ou
            conn.modify_dn(entry.entry_dn, f'cn={new_username}', new_superior=dn_ou)
            atual_ou_filtered = new_ou_cn
            pass
        else:
            conn.modify(entry.entry_dn, modifications)
            # ATUALIZA OS ATRIBUTOS COM OS NOVOS VALORES
            if new_email is not None:
                email = new_email
            if new_description is not None:
                description = new_description
            if new_name:
                user_gn = new_name
            if new_sn is not None:
                user_sn = new_sn
            if new_init is not None:
                user_init = new_init
            # if new_ou:
            #     atual_ou = new_ou
            if new_agent is not None:
                agente_ip = new_agent
            if new_cpf is not None:
                cpf = new_cpf
            if new_login is not None:
                username = new_login

        # TRANSFERE UMA ESTAÇÃO DE UMA UNIDADE ORGANIZACIONAL PARA OUTRA
        conn.modify_dn(entry.entry_dn, f'cn={new_username}', new_superior=dn_ou)
        atual_ou_filtered = new_ou_cn

        edit_groups(username)
        flash('Realizações efetuadas!', 'success')
        return redirect(url_for('busca.show_user_details', username=username))

    # LISTA OS TIPOS BUSCADOS
    type = entry.objectCategory.value

    # REMOVE OS SEPARADORES
    types = subprocess.getoutput(f"less {type} | awk -F '=' '{{print $2}}' | awk -F ',' '{{print $1}}'")   

    # FILTRO PARA RESULTADOS DE LOG ATRÁS DE CONDICIONAIS
    nunca_f = '31/12/1600'
    nunca_h = 'nada'
    nunca_b = '31/12/9999'

    # ORGANIZA A EXIBIÇÃO DE LOG DO USUÁRIO
    if types == 'Person':
        def f_data_hora(dt, f_data="%d/%m/%Y", f_hora= "%H:%M:%S"):
            utc = pytz.timezone('Etc/GMT+3')
            dt_f = dt.astimezone(utc)
            data_f = dt_f.strftime(f_data)
            hora_f = dt_f.strftime(f_hora)
            return data_f, hora_f
          
    try:
        # CONVERSÃO DE FUSO HORÁRIO
        data_modificacao_user_f, data_modificacao_user_h = f_data_hora(data_modificacao_user)
        data_criacao_user_f, data_criacao_user_h = f_data_hora(data_criacao_user)
        ultima_troca_sn_f, ultima_troca_sn_h = f_data_hora(ultima_troca_sn)
        ultimo_logon_f, ultimo_logon_h = f_data_hora(ultimo_logon)
        errou_senha_f, errou_senha_h = f_data_hora(errou_senha)
        data_expiracao_user_f, data_expiracao_user_h = f_data_hora(data_expiracao_user)
    except:
        data_modificacao_user_f = nunca_h
        data_modificacao_user_h = nunca_h
        data_criacao_user_f = nunca_h
        data_criacao_user_h = nunca_h
        ultima_troca_sn_f = nunca_h
        ultima_troca_sn_h = nunca_h
        ultimo_logon_f = nunca_h
        ultimo_logon_h = nunca_h
        errou_senha_f = nunca_h
        errou_senha_h = nunca_h
        data_expiracao_user_f = nunca_h
        data_expiracao_user_h = nunca_h

    # RENDERIA A PAGINA ESPECÍFICA PARA CADA ITEM BUSCADO, USUARIO OU ESTAÇÃO
    if types == 'Computer':
        return render_template('computer.html', username=username, ous=ous, atual_ou_filtered=atual_ou_filtered)
    else:
        return render_template('usuario.html', agente_ip=agente_ip, cpf=cpf, nunca_h=nunca_h, nunca_b=nunca_b, errou_senha_f=errou_senha_f, errou_senha_h=errou_senha_h, ultimo_logon_f=ultimo_logon_f, ultimo_logon_h=ultimo_logon_h, ultima_troca_sn_f=ultima_troca_sn_f, ultima_troca_sn_h=ultima_troca_sn_h, data_criacao_user_f=data_criacao_user_f, data_criacao_user_h=data_criacao_user_h, data_modificacao_user_f=data_modificacao_user_f, data_modificacao_user_h=data_modificacao_user_h,  data_expiracao_user_f=data_expiracao_user_f, data_expiracao_user_h=data_expiracao_user_h, nunca_f=nunca_f, user_gn=user_gn, user_init=user_init, user_sn=user_sn, username=username, description=description, email=email, groups=groups, is_account_enabled=is_account_enabled, grupos_ad=grupos_ad, CCorTI=CCorTI)
