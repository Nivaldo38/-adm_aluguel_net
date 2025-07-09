#!/usr/bin/env python3
"""
Script para verificar se tudo está pronto para deploy no Railway
"""

import os
import sys
from pathlib import Path

def verificar_arquivos_essenciais():
    """Verifica se todos os arquivos essenciais existem"""
    print("🔍 Verificando arquivos essenciais...")
    
    arquivos_necessarios = [
        'requirements.txt',
        'Procfile',
        'railway.json',
        'gunicorn.conf.py',
        'run.py',
        'app/__init__.py',
        'app/routes.py',
        'app/models.py'
    ]
    
    for arquivo in arquivos_necessarios:
        if Path(arquivo).exists():
            print(f"✅ {arquivo}")
        else:
            print(f"❌ {arquivo} - FALTANDO!")
            return False
    
    return True

def verificar_configuracoes():
    """Verifica configurações importantes"""
    print("\n🔧 Verificando configurações...")
    
    # Verificar gunicorn.conf.py
    try:
        with open('gunicorn.conf.py', 'r') as f:
            config = f.read()
            if 'bind =' in config and 'workers =' in config:
                print("✅ gunicorn.conf.py configurado corretamente")
            else:
                print("❌ gunicorn.conf.py mal configurado")
                return False
    except:
        print("❌ Erro ao ler gunicorn.conf.py")
        return False
    
    # Verificar Procfile
    try:
        with open('Procfile', 'r') as f:
            procfile = f.read()
            if 'gunicorn' in procfile and 'app:app' in procfile:
                print("✅ Procfile configurado corretamente")
            else:
                print("❌ Procfile mal configurado")
                return False
    except:
        print("❌ Erro ao ler Procfile")
        return False
    
    # Verificar railway.json
    try:
        with open('railway.json', 'r') as f:
            railway = f.read()
            if 'gunicorn' in railway and 'healthcheckPath' in railway:
                print("✅ railway.json configurado corretamente")
            else:
                print("❌ railway.json mal configurado")
                return False
    except:
        print("❌ Erro ao ler railway.json")
        return False
    
    return True

def verificar_dependencias():
    """Verifica se as dependências estão no requirements.txt"""
    print("\n📦 Verificando dependências...")
    
    dependencias_essenciais = [
        'Flask',
        'Flask-SQLAlchemy',
        'gunicorn',
        'Werkzeug',
        'Jinja2'
    ]
    
    try:
        with open('requirements.txt', 'r') as f:
            requirements = f.read()
            
        for dep in dependencias_essenciais:
            if dep in requirements:
                print(f"✅ {dep}")
            else:
                print(f"❌ {dep} - FALTANDO!")
                return False
    except:
        print("❌ Erro ao ler requirements.txt")
        return False
    
    return True

def verificar_app():
    """Verifica se a aplicação Flask está funcionando"""
    print("\n🚀 Testando aplicação Flask...")
    
    try:
        # Importar a aplicação
        sys.path.append('.')
        from app import app
        
        print("✅ Aplicação Flask importada com sucesso")
        
        # Verificar se tem rotas básicas
        with app.test_client() as client:
            response = client.get('/')
            if response.status_code == 200:
                print("✅ Rota principal funcionando")
            else:
                print(f"⚠️ Rota principal retornou status {response.status_code}")
        
    except Exception as e:
        print(f"❌ Erro ao testar aplicação: {e}")
        return False
    
    return True

def main():
    """Função principal"""
    print("🚀 VERIFICAÇÃO PARA DEPLOY NO RAILWAY")
    print("=" * 50)
    
    sucesso = True
    
    # Verificar arquivos
    if not verificar_arquivos_essenciais():
        sucesso = False
    
    # Verificar configurações
    if not verificar_configuracoes():
        sucesso = False
    
    # Verificar dependências
    if not verificar_dependencias():
        sucesso = False
    
    # Verificar aplicação
    if not verificar_app():
        sucesso = False
    
    print("\n" + "=" * 50)
    if sucesso:
        print("🎉 TUDO PRONTO PARA DEPLOY!")
        print("\n📋 PRÓXIMOS PASSOS:")
        print("1. Faça commit das alterações:")
        print("   git add .")
        print("   git commit -m 'Adicionar filtro por local nos contratos'")
        print("\n2. Faça push para o GitHub:")
        print("   git push origin main")
        print("\n3. O Railway fará deploy automático!")
        print("\n⚠️ LEMBRE-SE: Configure as variáveis de ambiente no Railway:")
        print("   - SECRET_KEY")
        print("   - DATABASE_URL (se usar PostgreSQL)")
        print("   - EMAIL_* (para notificações)")
    else:
        print("❌ CORRIJA OS PROBLEMAS ANTES DO DEPLOY!")
    
    return sucesso

if __name__ == "__main__":
    main() 