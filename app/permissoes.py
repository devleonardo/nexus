from app.config import *

# Página de alteração de wallpapers
adwall = [ LDAP_GROUP_DN ,LDAP_GROUP_DN4]

# Página audit, responsável pelos logs do Nexus
audit = [LDAP_GROUP_DN]

# Página que exibe o dashboard de monitoramento dos rdns
detector = [ LDAP_GROUP_DN ,NX_CALLBACK, NX_CALLADM, NX_CALLSUP]

# Página que exibe a consulta de resolução de dominios
dashboard = [ LDAP_GROUP_DN, NX_CALLADM, NX_CALLBACK, NX_CALLSUP ]

# Página que exibe os status do IX
statusIX = [ LDAP_GROUP_DN, NX_CALLADM, NX_CALLBACK, NX_CALLSUP ]

# Página que exibe os status do ClickSign
statusCS = [ LDAP_GROUP_DN, NX_CALLADM, NX_CALLBACK, NX_CALLSUP ]

# Página que realiza busca de usuário do Radius
busca_radius = [ LDAP_GROUP_DN, NX_CALLADM, NX_CALLBACK, NX_CALLSUP ]

# Página que realiza busca de IP do Radius
busca_radiusIP = [ LDAP_GROUP_DN ]

# Página que realiza a busca por urls bloqueados
busca_url = [ LDAP_GROUP_DN, NX_CALLSUP ]

# Página que exibe consulta MAC
busca_mac = [ LDAP_GROUP_DN, NX_CALLADM, NX_CALLBACK, NX_CALLSUP ]

# Página que exibe calculadora de IP
subnet = [ LDAP_GROUP_DN, NX_CALLADM, NX_CALLBACK, NX_CALLSUP ]

# Página que exibe os servidores integrados no Freeipa
freeipa_servers = [LDAP_GROUP_DN]

# Página para criação de espelho de ponto manual, utilizado pelo RH
ponto_grd = [LDAP_GROUP_DN, LDAP_GROUP_DN5]

# Página responsável pela criação de grupos
create_group = [LDAP_GROUP_DN]

# Página responsável pela busca de usuários ou OU's
busca = [LDAP_GROUP_DN]
