#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar o status atual do Railway
"""

import os
import sys
from pathlib import Path

def verificar_status_atual():
    """Verifica o status atual do sistema"""
    print("🔍 VERIFICANDO STATUS ATUAL DO RAILWAY")
    print("=" * 50)
    
    # Verificar variáveis de ambiente
    print("\n📋 Variáveis de Ambiente Atuais:")
    
    secret_key = os.getenv('SECRET_KEY')
    if secret_key:
        print("✅ SECRET_KEY configurada")
        print(f"   Valor: {secret_key[:10]}... (primeiros 10 caracteres)")
    else:
        print("❌ SECRET_KEY não encontrada")
    
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        print("✅ DATABASE_URL configurada")
    else:
        print("⚠️ DATABASE_URL não configurada")
    
    # Verificar outras variáveis
    email_host = os.getenv('EMAIL_HOST')
    if email_host:
        print("✅ EMAIL_HOST configurado")
    else:
        print("⚠️ EMAIL_HOST não configurado")
    
    d4sign_token = os.getenv('D4SIGN_API_TOKEN')
    if d4sign_token:
        print("✅ D4SIGN_API_TOKEN configurado")
    else:
        print("⚠️ D4SIGN_API_TOKEN não configurado")

def verificar_problemas_comuns():
    """Verifica problemas comuns que podem afetar os botões"""
    print("\n🔧 VERIFICANDO PROBLEMAS COMUNS:")
    
    # Verificar se há erros no código
    print("\n1️⃣ Verificando arquivos principais:")
    
    files_to_check = [
        "app/__init__.py",
        "app/routes.py",
        "app/models.py",
        "run.py"
    ]
    
    for file in files_to_check:
        if Path(file).exists():
            print(f"✅ {file} existe")
        else:
            print(f"❌ {file} não encontrado")
    
    # Verificar templates
    print("\n2️⃣ Verificando templates:")
    templates_dir = Path("app/templates")
    if templates_dir.exists():
        important_templates = [
            "base_modern.html",
            "index.html",
            "listar_contratos.html"
        ]
        
        for template in important_templates:
            template_path = templates_dir / template
            if template_path.exists():
                print(f"✅ {template} existe")
            else:
                print(f"❌ {template} não encontrado")
    else:
        print("❌ Diretório templates não existe")

def testar_app_local():
    """Testa se o app funciona localmente"""
    print("\n🚀 TESTANDO APLICAÇÃO LOCAL:")
    
    try:
        from app import app
        
        with app.test_client() as client:
            # Testar rotas principais
            routes_to_test = [
                ('/', 'Página inicial'),
                ('/locais', 'Listar locais'),
                ('/inquilinos', 'Listar inquilinos'),
                ('/listar_contratos', 'Listar contratos'),
                ('/boletos', 'Listar boletos')
            ]
            
            for route, description in routes_to_test:
                try:
                    response = client.get(route)
                    if response.status_code == 200:
                        print(f"✅ {description} funciona")
                    else:
                        print(f"❌ {description} retornou {response.status_code}")
                except Exception as e:
                    print(f"❌ Erro em {description}: {e}")
                    
    except Exception as e:
        print(f"❌ Erro ao testar aplicação: {e}")

def mostrar_diagnostico():
    """Mostra diagnóstico baseado nos problemas encontrados"""
    print("\n💡 DIAGNÓSTICO:")
    print("=" * 30)
    
    print("\n🎯 Se SECRET_KEY está configurada mas os botões não funcionam:")
    print("1. **Cache do navegador** - Limpe com Ctrl+F5")
    print("2. **Railway ainda inicializando** - Aguarde 2-3 minutos")
    print("3. **Problema de rede** - Teste em outro navegador")
    print("4. **Erro no código** - Verifique logs do Railway")
    print("5. **Problema de JavaScript** - Verifique console F12")

def mostrar_solucoes_especificas():
    """Mostra soluções específicas"""
    print("\n🔧 SOLUÇÕES ESPECÍFICAS:")
    print("=" * 30)
    
    print("\n1️⃣ **Se a página carrega mas os botões não funcionam:**")
    print("   - Abra o console do navegador (F12)")
    print("   - Verifique se há erros de JavaScript")
    print("   - Recarregue a página (Ctrl+F5)")
    
    print("\n2️⃣ **Se a página não carrega:**")
    print("   - Verifique os logs no Railway")
    print("   - Teste a URL diretamente")
    print("   - Aguarde mais tempo (Railway pode demorar)")
    
    print("\n3️⃣ **Se formulários não salvam:**")
    print("   - Verifique se DATABASE_URL está configurada")
    print("   - Teste localmente primeiro")
    print("   - Verifique logs de erro")
    
    print("\n4️⃣ **Se links não funcionam:**")
    print("   - Teste acessando URLs diretamente")
    print("   - Verifique se o Railway está online")
    print("   - Aguarde inicialização completa")

def verificar_logs_railway():
    """Instruções para verificar logs no Railway"""
    print("\n📋 COMO VERIFICAR LOGS NO RAILWAY:")
    print("=" * 40)
    
    print("\n1. Acesse: https://railway.app")
    print("2. Entre no seu projeto")
    print("3. Vá em 'Deployments'")
    print("4. Clique no último deploy")
    print("5. Clique em 'View Logs'")
    print("6. Procure por erros em vermelho")
    
    print("\n🔍 O que procurar nos logs:")
    print("- Erros de importação")
    print("- Erros de banco de dados")
    print("- Erros de variáveis de ambiente")
    print("- Erros de dependências")

def main():
    """Função principal"""
    print("🚀 DIAGNÓSTICO COMPLETO - RAILWAY")
    print("=" * 50)
    
    # Verificar status atual
    verificar_status_atual()
    
    # Verificar problemas comuns
    verificar_problemas_comuns()
    
    # Testar app local
    testar_app_local()
    
    # Mostrar diagnóstico
    mostrar_diagnostico()
    
    # Mostrar soluções específicas
    mostrar_solucoes_especificas()
    
    # Instruções para logs
    verificar_logs_railway()
    
    print("\n" + "=" * 50)
    print("📋 PRÓXIMOS PASSOS:")
    print("1. Verifique os logs no Railway")
    print("2. Teste a URL diretamente")
    print("3. Limpe cache do navegador (Ctrl+F5)")
    print("4. Teste em outro navegador")
    print("5. Aguarde mais tempo se necessário")
    
    print("\n💡 Se ainda não funcionar:")
    print("- Copie os erros dos logs")
    print("- Teste localmente primeiro")
    print("- Verifique se há mudanças recentes")

if __name__ == "__main__":
    main() 