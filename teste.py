import requests

# Configurações de conexão
ipa_server = 'https://freeipa01.lestetelecom.com.br'
ipa_user = 'sistemas'
ipa_password = '8gcCDrh!LDr'

# Endpoint da API REST do FreeIPA para autenticação
auth_url = f'{ipa_server}/session/login_password'

# Dados de autenticação
auth_data = {
    'user': ipa_user,
    'password': ipa_password,
    'otp': '',  # Se você utiliza OTP para autenticação, adicione aqui
}

try:
    # Autenticar no servidor FreeIPA
    auth_response = requests.post(auth_url, data=auth_data, verify=False)
    auth_response.raise_for_status()  # Lança um erro se a requisição não for bem-sucedida

    # Extrair o token de autenticação do cabeçalho da resposta
    session_token = auth_response.headers.get('Set-Cookie')

    # Se o token não for encontrado, falha na autenticação
    if not session_token:
        raise Exception('Falha na autenticação. Token não encontrado.')

    # Configurar cabeçalhos para requisições subsequentes com o token de sessão
    headers = {
        'Content-Type': 'application/json',
        'Cookie': session_token,
    }

    # Endpoint da API REST do FreeIPA para listar grupos
    groups_url = f'{ipa_server}/ipa/session/json'

    # Parâmetros da requisição para listar grupos
    groups_params = {
        'method': 'group_find',
        'params': [],
        'id': 0,
    }

    # Fazer requisição para listar grupos
    groups_response = requests.post(groups_url, headers=headers, json=groups_params, verify=False)
    groups_response.raise_for_status()  # Lança um erro se a requisição não for bem-sucedida

    # Extrair os grupos da resposta
    groups_data = groups_response.json()['result']

    # Iterar pelos grupos e obter informações de sudo
    for group in groups_data:
        group_name = group['cn'][0]
        print(f"Grupo: {group_name}")

        # Endpoint da API REST do FreeIPA para obter informações de sudo
        sudo_url = f'{ipa_server}/ipa/session/json'

        # Parâmetros da requisição para obter informações de sudo
        sudo_params = {
            'method': 'sudorule_show',
            'params': [[group_name]],
            'id': 0,
        }

        # Fazer requisição para obter informações de sudo para o grupo
        sudo_response = requests.post(sudo_url, headers=headers, json=sudo_params, verify=False)
        sudo_response.raise_for_status()  # Lança um erro se a requisição não for bem-sucedida

        # Verificar se há comandos permitidos
        sudo_info = sudo_response.json()['result']
        if 'ipaallowedcommand' in sudo_info:
            allowed_commands = sudo_info['ipaallowedcommand']
            print("Comandos Permitidos:")
            for command in allowed_commands:
                print(f"  {command}")
        else:
            print("Nenhum comando permitido encontrado.")

finally:
    # Fazer logout no servidor FreeIPA
    logout_url = f'{ipa_server}/session/logout'
    requests.post(logout_url, headers=headers, verify=False)
