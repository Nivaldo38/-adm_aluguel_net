#!/usr/bin/env python3
"""
Script para Deploy no Railway
"""

import os
import subprocess
import sys

def check_git():
    """Verifica se o Git está configurado"""
    try:
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Git configurado")
            return True
        else:
            print("❌ Git não configurado")
            return False
    except FileNotFoundError:
        print("❌ Git não encontrado")
        return False

def check_railway_cli():
    """Verifica se o Railway CLI está instalado"""
    try:
        result = subprocess.run(['railway', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Railway CLI instalado")
            return True
        else:
            print("❌ Railway CLI não configurado")
            return False
    except FileNotFoundError:
        print("❌ Railway CLI não encontrado")
        return False

def create_gitignore():
    """Cria .gitignore se não existir"""
    gitignore_content = """
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# Database
*.db
*.sqlite
*.sqlite3

# Logs
*.log

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Backup files
backups/
*.zip

# Contracts
contracts/
*.pdf

# Environment variables
.env
.env.local

# Railway
.railway/
"""
    
    if not os.path.exists('.gitignore'):
        with open('.gitignore', 'w') as f:
            f.write(gitignore_content)
        print("✅ .gitignore criado")
    else:
        print("✅ .gitignore já existe")

def deploy_to_railway():
    """Faz o deploy para o Railway"""
    print("\n🚀 Iniciando deploy para o Railway...")
    
    # Verificar se estamos no diretório correto
    if not os.path.exists('app'):
        print("❌ Erro: Execute este script no diretório raiz do projeto")
        return False
    
    # Criar .gitignore
    create_gitignore()
    
    # Verificar Git
    if not check_git():
        print("\n📝 Configurando Git...")
        subprocess.run(['git', 'init'])
        subprocess.run(['git', 'add', '.'])
        subprocess.run(['git', 'commit', '-m', 'Deploy para Railway'])
    
    # Verificar Railway CLI
    if not check_railway_cli():
        print("\n📦 Instalando Railway CLI...")
        print("Execute: npm install -g @railway/cli")
        return False
    
    # Fazer deploy
    print("\n🚀 Fazendo deploy...")
    try:
        subprocess.run(['railway', 'deploy'])
        print("✅ Deploy concluído!")
        return True
    except Exception as e:
        print(f"❌ Erro no deploy: {e}")
        return False

def main():
    """Função principal"""
    print("🏠 Sistema de Administração de Aluguel - Deploy Railway")
    print("=" * 60)
    
    # Verificar dependências
    print("\n🔍 Verificando dependências...")
    
    if not check_git():
        print("\n❌ Git não está configurado")
        print("Configure o Git primeiro:")
        print("git config --global user.name 'Seu Nome'")
        print("git config --global user.email 'seu@email.com'")
        return
    
    if not check_railway_cli():
        print("\n❌ Railway CLI não está instalado")
        print("Instale o Railway CLI:")
        print("npm install -g @railway/cli")
        print("railway login")
        return
    
    # Fazer deploy
    if deploy_to_railway():
        print("\n🎉 Deploy concluído com sucesso!")
        print("\n📋 Próximos passos:")
        print("1. Acesse o Railway Dashboard")
        print("2. Configure as variáveis de ambiente:")
        print("   - DATABASE_URL (automático)")
        print("   - SECRET_KEY")
        print("   - EMAIL_USER (opcional)")
        print("   - EMAIL_PASSWORD (opcional)")
        print("   - D4SIGN_TOKEN_API (opcional)")
        print("   - D4SIGN_CRYPT_KEY (opcional)")
        print("3. Acesse a URL do seu projeto")
    else:
        print("\n❌ Deploy falhou")

if __name__ == "__main__":
    main() 