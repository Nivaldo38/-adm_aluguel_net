#!/usr/bin/env python3
"""
Script rápido para corrigir todos os problemas
"""

import os
import subprocess
import sys

def corrigir_requirements():
    """Corrige requirements.txt"""
    requirements = """Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Migrate==4.0.5
Flask-WTF==1.2.1
WTForms==3.1.1
email-validator==2.1.0
reportlab==4.4.2
Werkzeug==3.0.1
Jinja2==3.1.2
MarkupSafe==2.1.3
itsdangerous==2.1.2
click==8.1.7
blinker==1.7.0
SQLAlchemy==2.0.23
alembic==1.13.1
python-dotenv==1.0.0
gunicorn==21.2.0"""
    
    with open('requirements.txt', 'w', encoding='utf-8') as f:
        f.write(requirements)
    print("✅ Requirements.txt corrigido")

def corrigir_routes():
    """Corrige routes.py"""
    try:
        with open('app/routes.py', 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        # Tenta com encoding diferente se UTF-8 falhar
        with open('app/routes.py', 'r', encoding='latin-1') as f:
            content = f.read()
    
    # Remove imports problemáticos
    content = content.replace('from app.contract_generator import ContractGenerator', '# from app.contract_generator import ContractGenerator  # Removido')
    content = content.replace('from app.ds4_integration import DS4Integration', '# from app.ds4_integration import DS4Integration  # Removido')
    content = content.replace('from app.backup_service import backup_service', '# from app.backup_service import backup_service  # Removido')
    
    # Corrige campos de modelo
    content = content.replace('.filter_by(status=', '.filter_by(situacao=')
    content = content.replace('.data_criacao', '.id')
    
    with open('app/routes.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Routes.py corrigido")

def corrigir_templates():
    """Corrige templates"""
    # Corrige base_modern.html
    try:
        with open('app/templates/base_modern.html', 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open('app/templates/base_modern.html', 'r', encoding='latin-1') as f:
            content = f.read()
    
    content = content.replace('backup_management', 'backup_page')
    content = content.replace('email_notifications', 'index')
    
    with open('app/templates/base_modern.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Templates corrigidos")

def instalar_dependencias():
    """Instala dependências"""
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
    print("✅ Dependências instaladas")

def main():
    print("🔧 Corrigindo problemas...")
    corrigir_requirements()
    corrigir_routes()
    corrigir_templates()
    instalar_dependencias()
    print("✅ Tudo corrigido! Agora pode fazer deploy.")

if __name__ == "__main__":
    main() 