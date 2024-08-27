# Autenticação via LDAP
#### O Sistema tem por objetivo, autenticar e permitir acesso aos dados do Ative Directory com autenticação via LDAP, liberando assim os usuários do servidor.
#### Além da função de teste de DNS que somente os usuarios conectados terão acesso, o sistema agora conta também com a função de busca de usuários, onde até o momento é possível visualizar usuários listados na busca, assim como abrir uma página de cada usuário onde será exibido informações mais detalhadas, como os grupos no qual o usuario faz parte dentro do controlador de domínio.
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?logo=css3&logoColor=white&style=for-the-badge) ![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?logo=html5&logoColor=white&style=for-the-badge) ![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?logo=javascript&logoColor=%23F7DF1E&style=for-the-badge) ![Python](https://img.shields.io/badge/python-3670A0?logo=python&logoColor=ffdd54&style=for-the-badge) ![Bootstrap](https://img.shields.io/badge/bootstrap-%23563D7C.svg?logo=bootstrap&logoColor=white&style=for-the-badge) ![Flask](https://img.shields.io/badge/flask-%23000.svg?logo=flask&logoColor=white&style=for-the-badge)

### Tela de login em Python com Flask e autenticação via ldap.
- **Biblioteca:** ldap3
#### O Sistema tem por objetivo, autenticar e permitir acesso aos dados do Ative Directory com autenticação via LDAP.

![Autenticação via LDAP](https://github.com/devleonardo/images/blob/9d2b9d795e91c8ae2489e4de1627debc2d15b268/imgs/code333.png)
#
### Testes de resolução de nome com lista predefinida de dns, com tempo de resolução para cada dns e ping para o domínio resolvido.
- **Bibliotecas:** dns.resolver, ping3
 Além da função de teste de DNS, a aplicação conta também com a função de busca de usuários, onde  é possível listar usuários buscando pelo nome de usuário, nome completo ou até pelo e-mail. Podendo também abrir uma página de cada usuário onde será exibido informações mais detalhadas, como por exemplo, os grupos no qual o usuário pertence dentro do controlador de domínio.

![Resolução de DNS e Ping](https://github.com/devleonardo/images/blob/4dedfd73daddb081ae57012c7573a87b4066f467/imgs/code.png)
## Bibliotecas

#
### Regex para deolver somente o avg:
 - Filtra o resultado do teste de ping retornando somente o avg.
 - Converte esse resultado em float caso o teste seja executado com sucesso.
 - Tendo erro ao obter um teste de ping, retorna o valor **0.0**
 1. Flask: Construção de sites e apps web
 2. Ldap3: Autenticação via LDAP
 3. Ping3: Teste de ping
 4. Dns.resolver: Executa a pesquisa de DNS por consultas de nomes de
    servidores

![Failtragem de ping](https://github.com/devleonardo/images/blob/4dedfd73daddb081ae57012c7573a87b4066f467/imgs/code222.png)
## Configuração

```python
# Endereço do servidor
LDAP_HOST  =  'ldap://localhost:389'
# Nome de domínio
LDAP_BASE_DN  =  'dc=exemplo,dc=com'
# Usuário com permissão de leita para autenticação no servidor
LDAP_USER_DN  =  'admin'
# Senha do usuário
LDAP_USER_PASSWORD  =  'admin_password'
# Grupo que terá a permissão de acesso a aplicação, unidade organizacional e domínio
LDAP_GROUP_DN  =  'CN=USERS_STI,OU=SISTEMASTI,DC=exemplo,DC=com'
```


## Iniciando a aplicação
```python
python main.py
```