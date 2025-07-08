#!/usr/bin/env python3
"""
Script para configurar automaticamente o Railway
"""

import os
import secrets
import string

def gerar_secret_key():
    """Gera uma chave secreta segura"""
    caracteres = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(caracteres) for _ in range(50))

def criar_env_exemplo():
    """Cria arquivo .env com variáveis de exemplo"""
    print("📝 Criando arquivo .env com variáveis de exemplo...")
    
    secret_key = gerar_secret_key()
    
    env_content = f"""# Configurações para Railway
# Copie estas variáveis para o painel do Railway

# Chave secreta do Flask (OBRIGATÓRIO)
SECRET_KEY={secret_key}

# Configurações de Email (OPCIONAL - para notificações)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=seu_email@gmail.com
EMAIL_PASSWORD=sua_senha_app

# Configurações D4Sign (OPCIONAL - para assinatura digital)
D4SIGN_API_URL=https://api.d4sign.com.br
D4SIGN_API_TOKEN=seu_token_aqui
D4SIGN_SAFE_KEY=sua_safe_key_aqui

# Configurações do Sistema
FLASK_ENV=production
"""
    
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print("✅ Arquivo .env criado!")
    print("📋 Copie as variáveis acima para o Railway")

def mostrar_instrucoes_railway():
    """Mostra instruções para configurar o Railway"""
    print("\n" + "=" * 60)
    print("🚀 INSTRUÇÕES PARA CONFIGURAR O RAILWAY")
    print("=" * 60)
    
    print("\n1️⃣ Acesse o Railway:")
    print("   https://railway.app")
    
    print("\n2️⃣ Vá para seu projeto e clique em 'Variables'")
    
    print("\n3️⃣ Adicione estas variáveis (OBRIGATÓRIAS):")
    print("   SECRET_KEY=sua_chave_secreta_aqui")
    print("   DATABASE_URL=postgresql://... (criado automaticamente pelo Railway)")
    
    print("\n4️⃣ Adicione estas variáveis (OPCIONAIS):")
    print("   EMAIL_HOST=smtp.gmail.com")
    print("   EMAIL_PORT=587")
    print("   EMAIL_USER=seu_email@gmail.com")
    print("   EMAIL_PASSWORD=sua_senha_app")
    print("   D4SIGN_API_URL=https://api.d4sign.com.br")
    print("   D4SIGN_API_TOKEN=seu_token_aqui")
    print("   D4SIGN_SAFE_KEY=sua_safe_key_aqui")
    
    print("\n5️⃣ Clique em 'Deploy' para fazer o redeploy")
    
    print("\n6️⃣ Aguarde o deploy e teste a URL")

def testar_deploy_rapido():
    """Testa se o deploy está funcionando"""
    print("\n🔍 Testando deploy...")
    
    # Verificar se o app roda localmente
    try:
        from app import app
        print("✅ App Flask funcionando localmente")
        
        # Verificar configuração
        if app.config.get('SECRET_KEY'):
            print("✅ SECRET_KEY configurada")
        else:
            print("❌ SECRET_KEY não configurada")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no app: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 Configurador do Railway")
    print("=" * 50)
    
    # Criar arquivo .env
    criar_env_exemplo()
    
    # Mostrar instruções
    mostrar_instrucoes_railway()
    
    # Testar app
    app_ok = testar_deploy_rapido()
    
    print("\n" + "=" * 50)
    print("📊 RESUMO:")
    
    if app_ok:
        print("✅ Sistema pronto para deploy!")
        print("🚀 Configure as variáveis no Railway e faça deploy")
    else:
        print("❌ Problemas encontrados")
        print("🔧 Verifique os logs acima")
    
    print("\n💡 Dicas:")
    print("- O Railway criará automaticamente o DATABASE_URL")
    print("- Configure pelo menos SECRET_KEY no Railway")
    print("- As outras variáveis são opcionais")
    print("- Após configurar, faça redeploy no Railway")

if __name__ == '__main__':
    main() 