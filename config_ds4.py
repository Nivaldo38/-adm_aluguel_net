# Configuração DS4 (DocuSign)
# 
# Para usar a assinatura digital, você precisa:
# 1. Criar uma conta no DocuSign Developer (https://developers.docusign.com/)
# 2. Obter suas credenciais de integração
# 3. Configurar as variáveis de ambiente abaixo

import os

# Configurações DS4 - Configure estas variáveis de ambiente
DS4_CONFIG = {
    'ACCOUNT_ID': os.getenv('DS4_ACCOUNT_ID', ''),
    'INTEGRATION_KEY': os.getenv('DS4_INTEGRATION_KEY', ''),
    'USER_ID': os.getenv('DS4_USER_ID', ''),
    'PRIVATE_KEY_PATH': os.getenv('DS4_PRIVATE_KEY_PATH', ''),
    'BASE_PATH': 'https://demo.docusign.net/restapi',  # Use 'https://www.docusign.net/restapi' para produção
    'AUTH_SERVER': 'https://account-d.docusign.com'  # Use 'https://account.docusign.com' para produção
}

# Instruções para configurar:
"""
1. Acesse: https://developers.docusign.com/
2. Crie uma conta gratuita
3. Vá em "Tools" > "API Keys"
4. Crie uma nova Integration Key
5. Configure as permissões necessárias
6. Obtenha suas credenciais:
   - Account ID
   - Integration Key
   - User ID
   - Private Key

7. Configure as variáveis de ambiente:
   export DS4_ACCOUNT_ID="seu_account_id"
   export DS4_INTEGRATION_KEY="sua_integration_key"
   export DS4_USER_ID="seu_user_id"
   export DS4_PRIVATE_KEY_PATH="caminho/para/sua/private_key.pem"

8. Para Windows (PowerShell):
   $env:DS4_ACCOUNT_ID="seu_account_id"
   $env:DS4_INTEGRATION_KEY="sua_integration_key"
   $env:DS4_USER_ID="seu_user_id"
   $env:DS4_PRIVATE_KEY_PATH="caminho/para/sua/private_key.pem"
"""

def check_ds4_config():
    """Verifica se as configurações do DS4 estão completas"""
    missing = []
    for key, value in DS4_CONFIG.items():
        if not value and key != 'BASE_PATH':
            missing.append(key)
    
    if missing:
        print("⚠️  Configurações DS4 incompletas:")
        for item in missing:
            print(f"   - {item}")
        print("\nConfigure as variáveis de ambiente conforme instruções em config_ds4.py")
        return False
    
    print("✅ Configurações DS4 completas!")
    return True

if __name__ == "__main__":
    check_ds4_config() 