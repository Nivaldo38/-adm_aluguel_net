#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste completo para identificar problemas no Railway
"""

import os
import sys
import requests
import time
from pathlib import Path

def testar_configuracao_local():
    """Testa configuração local completa"""
    print("🔍 TESTE 1: CONFIGURAÇÃO LOCAL")
    print("=" * 40)
    
    # Verificar variáveis de ambiente
    print("\n📋 Variáveis de Ambiente:")
    secret_key = os.getenv('SECRET_KEY')
    if secret_key:
        print(f"✅ SECRET_KEY: {secret_key[:10]}...")
    else:
        print("❌ SECRET_KEY não configurada")
    
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        print("✅ DATABASE_URL configurada")
    else:
        print("⚠️ DATABASE_URL não configurada (usando SQLite)")
    
    # Verificar arquivos essenciais
    print("\n📁 Arquivos Essenciais:")
    essential_files = [
        "app/__init__.py",
        "app/routes.py", 
        "app/models.py",
        "run.py",
        "requirements.txt",
        "Procfile"
    ]
    
    for file in essential_files:
        if Path(file).exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file} não encontrado")

def testar_app_local():
    """Testa aplicação local completa"""
    print("\n🚀 TESTE 2: APLICAÇÃO LOCAL")
    print("=" * 40)
    
    try:
        from app import app
        
        with app.test_client() as client:
            # Testar todas as rotas principais
            routes = [
                ('/', 'Página inicial'),
                ('/locais', 'Listar locais'),
                ('/inquilinos', 'Listar inquilinos'),
                ('/listar_contratos', 'Listar contratos'),
                ('/boletos', 'Listar boletos'),
                ('/cadastrar_local', 'Cadastrar local'),
                ('/cadastrar_inquilino', 'Cadastrar inquilino'),
                ('/cadastrar_contrato', 'Cadastrar contrato')
            ]
            
            for route, description in routes:
                try:
                    response = client.get(route)
                    if response.status_code == 200:
                        print(f"✅ {description}: OK")
                    else:
                        print(f"❌ {description}: {response.status_code}")
                except Exception as e:
                    print(f"❌ {description}: Erro - {e}")
                    
    except Exception as e:
        print(f"❌ Erro ao testar aplicação local: {e}")

def testar_templates():
    """Testa se os templates estão corretos"""
    print("\n🎨 TESTE 3: TEMPLATES")
    print("=" * 40)
    
    templates_dir = Path("app/templates")
    if not templates_dir.exists():
        print("❌ Diretório templates não existe")
        return
    
    # Verificar templates importantes
    important_templates = [
        "base_modern.html",
        "index.html", 
        "listar_contratos.html",
        "listar_boletos.html",
        "cadastrar_inquilino.html"
    ]
    
    for template in important_templates:
        template_path = templates_dir / template
        if template_path.exists():
            # Verificar se tem JavaScript
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
                has_js = '<script>' in content
                has_tailwind = 'tailwindcss.com' in content
                has_fontawesome = 'font-awesome' in content
                
                print(f"✅ {template}:")
                print(f"   - JavaScript: {'✅' if has_js else '❌'}")
                print(f"   - Tailwind: {'✅' if has_tailwind else '❌'}")
                print(f"   - FontAwesome: {'✅' if has_fontawesome else '❌'}")
        else:
            print(f"❌ {template} não encontrado")

def testar_dependencias():
    """Testa se todas as dependências estão instaladas"""
    print("\n📦 TESTE 4: DEPENDÊNCIAS")
    print("=" * 40)
    
    required_packages = [
        'flask',
        'flask-sqlalchemy', 
        'gunicorn',
        'werkzeug',
        'jinja2'
    ]
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} não instalado")

def testar_banco_dados():
    """Testa conexão com banco de dados"""
    print("\n🗄️ TESTE 5: BANCO DE DADOS")
    print("=" * 40)
    
    try:
        from app import db
        from app.models import Local, Inquilino, Contrato
        
        # Testar criação de tabelas
        db.create_all()
        print("✅ Tabelas criadas com sucesso")
        
        # Testar consultas básicas
        locais_count = Local.query.count()
        inquilinos_count = Inquilino.query.count()
        contratos_count = Contrato.query.count()
        
        print(f"✅ Locais: {locais_count}")
        print(f"✅ Inquilinos: {inquilinos_count}")
        print(f"✅ Contratos: {contratos_count}")
        
    except Exception as e:
        print(f"❌ Erro no banco de dados: {e}")

def testar_servicos():
    """Testa serviços opcionais"""
    print("\n🔧 TESTE 6: SERVIÇOS")
    print("=" * 40)
    
    # Testar email service
    try:
        from app.email_service import email_service
        print("✅ Email service disponível")
    except:
        print("⚠️ Email service não configurado")
    
    # Testar D4Sign service
    try:
        from app.d4sign_service import d4sign_service
        print("✅ D4Sign service disponível")
    except:
        print("⚠️ D4Sign service não configurado")
    
    # Testar backup service
    try:
        from app.backup_service import BackupService
        print("✅ Backup service disponível")
    except:
        print("⚠️ Backup service não configurado")

def testar_arquivos_estaticos():
    """Testa arquivos estáticos"""
    print("\n📁 TESTE 7: ARQUIVOS ESTÁTICOS")
    print("=" * 40)
    
    static_dir = Path("app/static")
    if static_dir.exists():
        print("✅ Diretório static existe")
        
        # Verificar arquivos importantes
        static_files = ["manifest.json", "sw.js"]
        for file in static_files:
            file_path = static_dir / file
            if file_path.exists():
                print(f"✅ {file} existe")
            else:
                print(f"❌ {file} não encontrado")
    else:
        print("❌ Diretório static não existe")

def gerar_relatorio():
    """Gera relatório completo"""
    print("\n📊 RELATÓRIO COMPLETO")
    print("=" * 40)
    
    print("\n🎯 PROBLEMAS POSSÍVEIS NO RAILWAY:")
    print("1. **Variáveis de ambiente** - Verificar SECRET_KEY")
    print("2. **Dependências** - Verificar requirements.txt")
    print("3. **Banco de dados** - Verificar DATABASE_URL")
    print("4. **Templates** - Verificar se carregam corretamente")
    print("5. **JavaScript** - Verificar console do navegador")
    print("6. **CDNs** - Verificar se Tailwind/FontAwesome carregam")
    
    print("\n🔧 SOLUÇÕES PARA RAILWAY:")
    print("1. **Verificar logs** no Railway (Deployments → View Logs)")
    print("2. **Limpar cache** do navegador (Ctrl+F5)")
    print("3. **Testar em modo incógnito**")
    print("4. **Aguardar inicialização** (2-3 minutos)")
    print("5. **Verificar console** do navegador (F12)")
    
    print("\n📋 CHECKLIST PARA RAILWAY:")
    print("✅ SECRET_KEY configurada")
    print("✅ Deploy recente feito")
    print("✅ Aguardou 2-3 minutos")
    print("✅ Limpou cache (Ctrl+F5)")
    print("✅ Testou em outro navegador")
    print("✅ Verificou logs do Railway")

def main():
    """Função principal"""
    print("🚀 TESTE COMPLETO - SISTEMA DE ALUGUEL")
    print("=" * 50)
    
    # Executar todos os testes
    testar_configuracao_local()
    testar_app_local()
    testar_templates()
    testar_dependencias()
    testar_banco_dados()
    testar_servicos()
    testar_arquivos_estaticos()
    
    # Gerar relatório
    gerar_relatorio()
    
    print("\n" + "=" * 50)
    print("🎯 PRÓXIMOS PASSOS:")
    print("1. Se todos os testes passaram localmente:")
    print("   - O problema é específico do Railway")
    print("   - Verifique os logs no Railway")
    print("   - Teste a URL diretamente")
    
    print("\n2. Se algum teste falhou:")
    print("   - Corrija o problema localmente primeiro")
    print("   - Faça commit e push")
    print("   - Teste novamente no Railway")
    
    print("\n💡 DICA IMPORTANTE:")
    print("O sistema funciona localmente, então o problema")
    print("é específico do ambiente Railway. Verifique os logs!")

if __name__ == "__main__":
    main() 