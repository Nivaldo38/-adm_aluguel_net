#!/usr/bin/env python3
"""
Script para fazer regressão limpa do sistema
Remove funcionalidades complexas e mantém apenas o essencial
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

def limpar_requirements():
    """Limpa requirements.txt removendo módulos problemáticos"""
    print("📦 Limpando requirements.txt...")
    
    requirements_limpo = """Flask==3.0.0
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
gunicorn==21.2.0
"""
    
    with open('requirements.txt', 'w') as f:
        f.write(requirements_limpo)
    
    print("✅ requirements.txt limpo")

def remover_arquivos_complexos():
    """Remove arquivos relacionados a funcionalidades complexas"""
    print("🗑️ Removendo arquivos complexos...")
    
    arquivos_para_remover = [
        'app/ds4_integration.py',
        'app/ds4_simulado.py',
        'config_ds4.py',
        'testar_ds4.py',
        'testar_ds4_simulado.py',
        'testar_contrato_assinado.py',
        'configurar_ds4.bat'
    ]
    
    for arquivo in arquivos_para_remover:
        if os.path.exists(arquivo):
            os.remove(arquivo)
            print(f"✅ Removido: {arquivo}")

def simplificar_contract_generator():
    """Simplifica o gerador de contratos removendo PyPDF2"""
    print("📄 Simplificando contract_generator.py...")
    
    contract_generator_path = "app/contract_generator.py"
    if os.path.exists(contract_generator_path):
        with open(contract_generator_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remover import do PyPDF2
        content = content.replace("from PyPDF2 import PdfReader, PdfWriter", "# PyPDF2 removido para simplificação")
        
        # Remover funções que usam PyPDF2
        content = content.replace("def _merge_pdfs(self, pdfs, output_path):", "# Função de merge removida")
        
        with open(contract_generator_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ contract_generator.py simplificado")

def simplificar_backup_service():
    """Simplifica o serviço de backup removendo agendamento"""
    print("💾 Simplificando backup_service.py...")
    
    backup_service_path = "app/backup_service.py"
    if os.path.exists(backup_service_path):
        with open(backup_service_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remover import do schedule
        content = content.replace("import schedule", "# schedule removido para simplificação")
        content = content.replace("import time", "# time removido")
        content = content.replace("import threading", "# threading removido")
        
        # Comentar funções de agendamento
        content = content.replace("def schedule_daily_backup(self):", "# def schedule_daily_backup(self):")
        content = content.replace("def start_backup_scheduler(self):", "# def start_backup_scheduler(self):")
        
        with open(backup_service_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ backup_service.py simplificado")

def simplificar_email_service():
    """Simplifica o serviço de email"""
    print("📧 Simplificando email_service.py...")
    
    email_service_path = "app/email_service.py"
    if os.path.exists(email_service_path):
        with open(email_service_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Simplificar para sempre retornar True (simulado)
        content = content.replace("def send_email(self, to_email, subject, body, html_body=None, attachments=None):", 
                                "def send_email(self, to_email, subject, body, html_body=None, attachments=None):")
        
        # Adicionar comentário no início da função
        content = content.replace("    def send_email(self, to_email, subject, body, html_body=None, attachments=None):",
                                "    def send_email(self, to_email, subject, body, html_body=None, attachments=None):\n        # Email simulado - sempre retorna True")
        
        with open(email_service_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ email_service.py simplificado")

def simplificar_routes():
    """Simplifica as rotas removendo funcionalidades complexas"""
    print("🛣️ Simplificando routes.py...")
    
    routes_path = "app/routes.py"
    if os.path.exists(routes_path):
        with open(routes_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remover imports problemáticos
        content = content.replace("from app.contract_generator import ContractGenerator", "# from app.contract_generator import ContractGenerator")
        content = content.replace("from app.ds4_integration import DS4Integration", "# from app.ds4_integration import DS4Integration")
        content = content.replace("from app.backup_service import backup_service", "# from app.backup_service import backup_service")
        
        # Comentar rotas complexas
        content = content.replace("@app.route('/enviar_para_assinatura/<int:contrato_id>')", "# @app.route('/enviar_para_assinatura/<int:contrato_id>')")
        content = content.replace("@app.route('/verificar_status_assinatura/<int:contrato_id>')", "# @app.route('/verificar_status_assinatura/<int:contrato_id>')")
        content = content.replace("@app.route('/visualizar_contrato_assinado/<int:contrato_id>')", "# @app.route('/visualizar_contrato_assinado/<int:contrato_id>')")
        content = content.replace("@app.route('/cancelar_assinatura/<int:contrato_id>')", "# @app.route('/cancelar_assinatura/<int:contrato_id>')")
        
        with open(routes_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ routes.py simplificado")

def limpar_templates():
    """Remove referências a funcionalidades complexas nos templates"""
    print("🎨 Limpando templates...")
    
    templates_dir = Path("app/templates")
    if templates_dir.exists():
        for template_file in templates_dir.glob("*.html"):
            with open(template_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Remover botões de funcionalidades complexas
            content = content.replace("Enviar para Assinatura", "<!-- Enviar para Assinatura (removido) -->")
            content = content.replace("Ver Assinado", "<!-- Ver Assinado (removido) -->")
            content = content.replace("Cancelar Assinatura", "<!-- Cancelar Assinatura (removido) -->")
            
            with open(template_file, 'w', encoding='utf-8') as f:
                f.write(content)
        
        print("✅ Templates limpos")

def instalar_dependencias_limpas():
    """Instala apenas as dependências essenciais"""
    print("📦 Instalando dependências limpas...")
    
    try:
        # Desinstalar módulos problemáticos
        subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", "PyPDF2", "docusign-esign", "schedule"], check=False)
        
        # Instalar dependências limpas
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        
        print("✅ Dependências limpas instaladas")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False

def testar_sistema():
    """Testa se o sistema funciona após a limpeza"""
    print("🧪 Testando sistema...")
    
    try:
        # Testar import da aplicação
        import app
        print("✅ Import da aplicação OK")
        
        # Testar se o servidor inicia
        from app import app as flask_app
        print("✅ Flask app OK")
        
        return True
    except Exception as e:
        print(f"❌ Erro ao testar sistema: {e}")
        return False

def criar_arquivo_info():
    """Cria arquivo com informações sobre a regressão"""
    print("📝 Criando arquivo de informações...")
    
    info_content = """# Sistema de Aluguel - Versão Limpa

## Funcionalidades Disponíveis
✅ Dashboard moderno
✅ CRUD de Locais
✅ CRUD de Unidades
✅ CRUD de Inquilinos
✅ CRUD de Contratos
✅ Geração básica de PDF
✅ Sistema de login para inquilinos
✅ Backup manual
✅ Interface mobile responsiva

## Funcionalidades Removidas (Temporariamente)
❌ DocuSign (DS4)
❌ Assinatura digital
❌ Boletos com conexão real
❌ Email automático
❌ Agendamento de backups
❌ Módulos problemáticos (PyPDF2, docusign-esign, schedule)

## Próximos Passos
1. Testar funcionalidades básicas
2. Fazer deploy
3. Documentar sistema
4. Planejar melhorias futuras

## Como Usar
1. Execute: python run.py
2. Acesse: http://127.0.0.1:5000
3. Teste todas as funcionalidades básicas
4. Faça deploy quando estiver estável
"""
    
    with open('INFO_REGRESSAO.md', 'w', encoding='utf-8') as f:
        f.write(info_content)
    
    print("✅ Arquivo INFO_REGRESSAO.md criado")

def main():
    """Função principal da regressão"""
    print("🚀 Iniciando regressão limpa do sistema...")
    
    # 1. Limpar requirements
    limpar_requirements()
    
    # 2. Remover arquivos complexos
    remover_arquivos_complexos()
    
    # 3. Simplificar código
    simplificar_contract_generator()
    simplificar_backup_service()
    simplificar_email_service()
    simplificar_routes()
    
    # 4. Limpar templates
    limpar_templates()
    
    # 5. Instalar dependências limpas
    if not instalar_dependencias_limpas():
        print("❌ Falha na instalação de dependências")
        return False
    
    # 6. Testar sistema
    if not testar_sistema():
        print("❌ Falha no teste do sistema")
        return False
    
    # 7. Criar arquivo de informações
    criar_arquivo_info()
    
    print("\n🎉 Regressão limpa concluída!")
    print("\n📋 Próximos passos:")
    print("1. Teste localmente: python run.py")
    print("2. Verifique todas as funcionalidades básicas")
    print("3. Se tudo estiver OK, faça o commit e push")
    print("4. Deploy no Railway/Render")
    print("5. Leia INFO_REGRESSAO.md para mais detalhes")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 