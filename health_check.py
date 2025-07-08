#!/usr/bin/env python3
"""
Script de Verificação de Saúde do Sistema
Verifica se tudo está funcionando antes do deploy
"""

import os
import sys
import sqlite3
from datetime import datetime

def check_database():
    """Verifica se o banco de dados está funcionando"""
    print("🔍 Verificando banco de dados...")
    
    try:
        db_path = 'adm_aluguel.db'
        if not os.path.exists(db_path):
            print("❌ Banco de dados não encontrado")
            return False
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar tabelas principais
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        required_tables = ['local', 'unidade', 'inquilino', 'contrato', 'boleto']
        missing_tables = [table for table in required_tables if table not in tables]
        
        if missing_tables:
            print(f"❌ Tabelas faltando: {missing_tables}")
            return False
        
        # Verificar dados
        cursor.execute("SELECT COUNT(*) FROM local")
        locais_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM inquilino")
        inquilinos_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM contrato")
        contratos_count = cursor.fetchone()[0]
        
        print(f"✅ Banco OK - Locais: {locais_count}, Inquilinos: {inquilinos_count}, Contratos: {contratos_count}")
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erro no banco: {e}")
        return False

def check_directories():
    """Verifica se os diretórios necessários existem"""
    print("📁 Verificando diretórios...")
    
    required_dirs = [
        'app/templates',
        'app/static',
        'contracts',
        'backups'
    ]
    
    missing_dirs = []
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            missing_dirs.append(dir_path)
    
    if missing_dirs:
        print(f"❌ Diretórios faltando: {missing_dirs}")
        return False
    
    print("✅ Todos os diretórios existem")
    return True

def check_files():
    """Verifica se os arquivos principais existem"""
    print("📄 Verificando arquivos...")
    
    required_files = [
        'run.py',
        'requirements.txt',
        'Procfile',
        'runtime.txt',
        'app/__init__.py',
        'app/models.py',
        'app/routes.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Arquivos faltando: {missing_files}")
        return False
    
    print("✅ Todos os arquivos principais existem")
    return True

def check_dependencies():
    """Verifica se as dependências estão no requirements.txt"""
    print("📦 Verificando dependências...")
    
    try:
        with open('requirements.txt', 'r') as f:
            requirements = f.read()
        
        required_packages = [
            'Flask',
            'Flask-SQLAlchemy',
            'Werkzeug',
            'gunicorn',
            'schedule'
        ]
        
        missing_packages = []
        for package in required_packages:
            if package not in requirements:
                missing_packages.append(package)
        
        if missing_packages:
            print(f"❌ Pacotes faltando: {missing_packages}")
            return False
        
        print("✅ Todas as dependências estão listadas")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao verificar requirements.txt: {e}")
        return False

def check_environment():
    """Verifica variáveis de ambiente"""
    print("🌍 Verificando variáveis de ambiente...")
    
    # Verificar se arquivo .env existe (opcional)
    if os.path.exists('.env'):
        print("✅ Arquivo .env encontrado")
    else:
        print("⚠️ Arquivo .env não encontrado (normal para produção)")
    
    # Verificar variáveis críticas
    critical_vars = ['EMAIL_HOST', 'EMAIL_USER', 'EMAIL_PASSWORD']
    missing_vars = []
    
    for var in critical_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️ Variáveis de ambiente faltando: {missing_vars}")
        print("   Configure no Railway após o deploy")
    else:
        print("✅ Variáveis de ambiente configuradas")
    
    return True

def check_railway_config():
    """Verifica arquivos de configuração do Railway"""
    print("🚂 Verificando configuração do Railway...")
    
    railway_files = ['Procfile', 'runtime.txt', 'gunicorn.conf.py']
    missing_files = []
    
    for file_path in railway_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Arquivos do Railway faltando: {missing_files}")
        return False
    
    print("✅ Configuração do Railway OK")
    return True

def main():
    """Função principal"""
    print("🏥 Verificação de Saúde do Sistema")
    print("=" * 50)
    print(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    checks = [
        ("Arquivos", check_files),
        ("Diretórios", check_directories),
        ("Banco de Dados", check_database),
        ("Dependências", check_dependencies),
        ("Variáveis de Ambiente", check_environment),
        ("Configuração Railway", check_railway_config)
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n{name}:")
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Erro na verificação: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 50)
    print("📊 RESUMO:")
    
    all_passed = True
    for name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"  {name}: {status}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 50)
    
    if all_passed:
        print("🎉 SISTEMA PRONTO PARA DEPLOY!")
        print("✅ Todas as verificações passaram")
        print("\nPróximos passos:")
        print("1. Fazer push para GitHub")
        print("2. Conectar no Railway")
        print("3. Configurar variáveis de ambiente")
        print("4. Deploy automático!")
    else:
        print("⚠️ CORREÇÕES NECESSÁRIAS")
        print("❌ Algumas verificações falharam")
        print("\nCorrija os problemas antes do deploy")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 