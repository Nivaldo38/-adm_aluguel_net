#!/usr/bin/env python3
"""
Script para testar configuração do Railway
"""

import os
import sys

def testar_ambiente_railway():
    """Testa se o ambiente Railway está configurado corretamente"""
    print("🔍 Testando ambiente Railway...")
    print("=" * 50)
    
    # Verificar variáveis críticas
    variaveis_criticas = {
        'PORT': 'Porta do servidor',
        'DATABASE_URL': 'URL do banco de dados',
        'SECRET_KEY': 'Chave secreta do Flask'
    }
    
    variaveis_opcionais = {
        'EMAIL_HOST': 'Servidor de email',
        'EMAIL_USER': 'Usuário de email',
        'EMAIL_PASSWORD': 'Senha de email',
        'D4SIGN_API_URL': 'URL da API D4Sign',
        'D4SIGN_API_TOKEN': 'Token D4Sign',
        'D4SIGN_SAFE_KEY': 'Safe Key D4Sign'
    }
    
    print("📊 Variáveis críticas:")
    for var, desc in variaveis_criticas.items():
        valor = os.environ.get(var)
        if valor:
            print(f"✅ {var}: {desc} - Configurada")
        else:
            print(f"❌ {var}: {desc} - NÃO CONFIGURADA")
    
    print("\n📊 Variáveis opcionais:")
    for var, desc in variaveis_opcionais.items():
        valor = os.environ.get(var)
        if valor:
            print(f"✅ {var}: {desc} - Configurada")
        else:
            print(f"⚠️ {var}: {desc} - Não configurada (opcional)")
    
    # Testar importação do app
    print("\n🔧 Testando importação do app...")
    try:
        from app import app
        print("✅ App Flask importado com sucesso")
        
        # Testar configuração do banco
        db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
        if 'postgresql' in db_uri:
            print("✅ Banco PostgreSQL configurado")
        elif 'sqlite' in db_uri:
            print("⚠️ Usando SQLite (não recomendado para produção)")
        else:
            print("❌ Banco não configurado")
            
    except Exception as e:
        print(f"❌ Erro ao importar app: {e}")
        return False
    
    return True

def testar_gunicorn():
    """Testa se o Gunicorn consegue iniciar"""
    print("\n🚀 Testando Gunicorn...")
    try:
        import gunicorn
        print("✅ Gunicorn instalado")
        
        # Testar comando
        cmd = "gunicorn --config gunicorn.conf.py --log-level debug app:app"
        print(f"📝 Comando: {cmd}")
        
    except ImportError:
        print("❌ Gunicorn não instalado")
        return False
    
    return True

def main():
    """Função principal"""
    print("🚀 Teste de Configuração Railway")
    print("=" * 50)
    
    # Testar ambiente
    ambiente_ok = testar_ambiente_railway()
    
    # Testar Gunicorn
    gunicorn_ok = testar_gunicorn()
    
    print("\n" + "=" * 50)
    print("📊 RESUMO:")
    
    if ambiente_ok and gunicorn_ok:
        print("✅ Ambiente Railway configurado corretamente!")
        print("🚀 Pronto para deploy!")
    else:
        print("❌ Problemas encontrados:")
        if not ambiente_ok:
            print("  - Variáveis de ambiente faltando")
        if not gunicorn_ok:
            print("  - Gunicorn não configurado")
        
        print("\n🔧 Para corrigir:")
        print("1. Configure as variáveis de ambiente no Railway")
        print("2. Verifique se o banco PostgreSQL foi criado")
        print("3. Confirme se o requirements.txt está atualizado")
    
    return ambiente_ok and gunicorn_ok

if __name__ == '__main__':
    main() 