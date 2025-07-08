#!/usr/bin/env python3
"""
Script para verificar se o deploy está funcionando
"""

import os
import sys
import subprocess
import time

def testar_app_local():
    """Testa se o app roda localmente"""
    print("🔍 Testando app localmente...")
    
    try:
        # Testar importação
        from app import app
        print("✅ App importado com sucesso")
        
        # Testar configuração
        print(f"📊 Configuração:")
        print(f"  - SECRET_KEY: {'✅ Configurada' if app.config.get('SECRET_KEY') else '❌ Não configurada'}")
        print(f"  - DATABASE_URL: {'✅ Configurada' if os.environ.get('DATABASE_URL') else '❌ Não configurada'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao importar app: {e}")
        return False

def testar_gunicorn_local():
    """Testa se o Gunicorn roda localmente"""
    print("\n🚀 Testando Gunicorn localmente...")
    
    try:
        # Comando para testar
        cmd = ["gunicorn", "--config", "gunicorn.conf.py", "--log-level", "debug", "app:app"]
        
        print(f"📝 Executando: {' '.join(cmd)}")
        print("⏳ Iniciando servidor (vai parar após 10 segundos)...")
        
        # Executar por 10 segundos
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        time.sleep(10)
        process.terminate()
        
        stdout, stderr = process.communicate()
        
        print("📄 Logs do Gunicorn:")
        print(stdout.decode())
        
        if stderr:
            print("❌ Erros do Gunicorn:")
            print(stderr.decode())
        
        return process.returncode == 0 or process.returncode == -15  # -15 é SIGTERM
        
    except Exception as e:
        print(f"❌ Erro ao testar Gunicorn: {e}")
        return False

def verificar_arquivos():
    """Verifica se todos os arquivos necessários existem"""
    print("\n📁 Verificando arquivos...")
    
    arquivos_necessarios = [
        "app/__init__.py",
        "app/routes.py", 
        "app/models.py",
        "gunicorn.conf.py",
        "Procfile",
        "requirements.txt",
        "railway.json"
    ]
    
    todos_ok = True
    for arquivo in arquivos_necessarios:
        if os.path.exists(arquivo):
            print(f"✅ {arquivo}")
        else:
            print(f"❌ {arquivo} - NÃO ENCONTRADO")
            todos_ok = False
    
    return todos_ok

def verificar_dependencias():
    """Verifica se as dependências estão instaladas"""
    print("\n📦 Verificando dependências...")
    
    dependencias = [
        "flask",
        "flask_sqlalchemy", 
        "flask_migrate",
        "gunicorn",
        "reportlab",
        "requests"
    ]
    
    todas_ok = True
    for dep in dependencias:
        try:
            __import__(dep)
            print(f"✅ {dep}")
        except ImportError:
            print(f"❌ {dep} - NÃO INSTALADA")
            todas_ok = False
    
    return todas_ok

def main():
    """Função principal"""
    print("🔍 Verificação Completa do Deploy")
    print("=" * 50)
    
    # Verificar arquivos
    arquivos_ok = verificar_arquivos()
    
    # Verificar dependências
    dependencias_ok = verificar_dependencias()
    
    # Testar app
    app_ok = testar_app_local()
    
    # Testar Gunicorn
    gunicorn_ok = testar_gunicorn_local()
    
    print("\n" + "=" * 50)
    print("📊 RESUMO:")
    
    if all([arquivos_ok, dependencias_ok, app_ok, gunicorn_ok]):
        print("✅ TUDO OK! Sistema pronto para deploy!")
        print("🚀 Faça push para GitHub e conecte no Railway")
    else:
        print("❌ Problemas encontrados:")
        if not arquivos_ok:
            print("  - Arquivos faltando")
        if not dependencias_ok:
            print("  - Dependências não instaladas")
        if not app_ok:
            print("  - App não inicializa")
        if not gunicorn_ok:
            print("  - Gunicorn não funciona")
        
        print("\n🔧 Para corrigir:")
        print("1. Instale dependências: pip install -r requirements.txt")
        print("2. Configure variáveis de ambiente")
        print("3. Verifique se todos os arquivos estão presentes")
    
    return all([arquivos_ok, dependencias_ok, app_ok, gunicorn_ok])

if __name__ == '__main__':
    main() 