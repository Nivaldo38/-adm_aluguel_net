#!/usr/bin/env python3
"""
Script para configurar o D4Sign de forma interativa
"""

import os
import sys
from pathlib import Path

def criar_arquivo_env():
    """Cria arquivo .env com configurações do D4Sign"""
    
    print("🔧 CONFIGURAÇÃO D4SIGN")
    print("=" * 50)
    
    # Verificar se arquivo .env já existe
    env_file = Path(".env")
    if env_file.exists():
        print("⚠️ Arquivo .env já existe!")
        resposta = input("Deseja sobrescrever? (s/n): ").lower()
        if resposta != 's':
            print("❌ Configuração cancelada")
            return False
    
    print("\n📋 Para configurar o D4Sign, você precisa:")
    print("1. Criar conta em: https://sandbox.d4sign.com.br/criar.html")
    print("2. Acessar 'Dev API' e copiar sua tokenAPI")
    print("3. Se cryptKey estiver habilitado, copiar também")
    
    print("\n🔑 CONFIGURAÇÃO D4SIGN:")
    
    # Ambiente
    ambiente = input("Ambiente (sandbox/production) [sandbox]: ").strip() or "sandbox"
    
    # Token API
    token_api = input("Token API (obrigatório): ").strip()
    if not token_api:
        print("❌ Token API é obrigatório!")
        return False
    
    # Crypt Key (opcional)
    crypt_key = input("Crypt Key (opcional): ").strip()
    
    # Email
    print("\n📧 CONFIGURAÇÃO DE EMAIL:")
    smtp_server = input("SMTP Server [smtp.gmail.com]: ").strip() or "smtp.gmail.com"
    smtp_port = input("SMTP Port [587]: ").strip() or "587"
    smtp_username = input("Email: ").strip()
    smtp_password = input("Senha do app: ").strip()
    admin_email = input("Email do administrador: ").strip()
    
    # Secret Key
    secret_key = input("Secret Key (deixe vazio para gerar): ").strip()
    if not secret_key:
        import secrets
        secret_key = secrets.token_hex(32)
    
    # Criar conteúdo do arquivo .env
    env_content = f"""# ===== CONFIGURAÇÃO D4SIGN =====

# Ambiente (sandbox ou production)
D4SIGN_ENVIRONMENT={ambiente}

# Credenciais de API (obrigatórias)
D4SIGN_TOKEN_API={token_api}
D4SIGN_CRYPT_KEY={crypt_key}

# ===== CONFIGURAÇÃO DE EMAIL =====

# Configuração SMTP
SMTP_SERVER={smtp_server}
SMTP_PORT={smtp_port}
SMTP_USERNAME={smtp_username}
SMTP_PASSWORD={smtp_password}
SMTP_USE_TLS=True

# Email do administrador
ADMIN_EMAIL={admin_email}

# ===== CONFIGURAÇÃO DO SISTEMA =====

# Chave secreta do Flask
SECRET_KEY={secret_key}

# Configuração do banco de dados
DATABASE_URL=sqlite:///adm_aluguel.db
"""
    
    # Salvar arquivo .env
    try:
        with open(".env", "w", encoding="utf-8") as f:
            f.write(env_content)
        
        print("\n✅ Arquivo .env criado com sucesso!")
        print("📁 Arquivo salvo como: .env")
        
        # Mostrar configurações (sem senhas)
        print("\n📋 Configurações salvas:")
        print(f"   🌐 Ambiente: {ambiente}")
        print(f"   🔑 Token API: {token_api[:10]}..." if len(token_api) > 10 else f"   🔑 Token API: {token_api}")
        print(f"   📧 SMTP: {smtp_server}:{smtp_port}")
        print(f"   👤 Email: {smtp_username}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar arquivo .env: {e}")
        return False

def testar_configuracao():
    """Testa a configuração do D4Sign"""
    print("\n🧪 TESTANDO CONFIGURAÇÃO...")
    
    try:
        # Recarregar variáveis de ambiente
        from dotenv import load_dotenv
        load_dotenv()
        
        # Importar serviço D4Sign
        from app.d4sign_service import d4sign_service
        
        print(f"   🔧 D4Sign habilitado: {d4sign_service.enabled}")
        print(f"   🌐 Ambiente: {'Produção' if d4sign_service.is_production else 'Sandbox'}")
        print(f"   🔗 URL: {d4sign_service.api_url}")
        
        if d4sign_service.enabled:
            print("   ✅ Configuração válida!")
            return True
        else:
            print("   ❌ D4Sign não está configurado corretamente")
            return False
            
    except Exception as e:
        print(f"   ❌ Erro ao testar: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 CONFIGURADOR D4SIGN")
    print("=" * 50)
    
    # Criar arquivo .env
    if criar_arquivo_env():
        # Testar configuração
        if testar_configuracao():
            print("\n🎉 Configuração concluída com sucesso!")
            print("\n📋 Próximos passos:")
            print("1. Execute: python testar_d4sign.py")
            print("2. Teste o sistema: python run.py")
            print("3. Acesse: http://localhost:5000")
        else:
            print("\n⚠️ Configuração criada, mas há problemas")
            print("Verifique as credenciais e tente novamente")
    else:
        print("\n❌ Falha na configuração")

if __name__ == "__main__":
    main() 