#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar problemas específicos dos botões no Railway
"""

import os
import sys
from pathlib import Path

def verificar_configuracao_railway():
    """Verifica se as configurações do Railway estão corretas"""
    print("🔍 VERIFICANDO CONFIGURAÇÃO DO RAILWAY")
    print("=" * 50)
    
    # Verificar variáveis de ambiente
    print("\n📋 Variáveis de Ambiente:")
    
    # SECRET_KEY é obrigatória
    secret_key = os.getenv('SECRET_KEY')
    if secret_key:
        print("✅ SECRET_KEY configurada")
    else:
        print("❌ SECRET_KEY NÃO CONFIGURADA - Isso pode causar problemas!")
    
    # DATABASE_URL
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        print("✅ DATABASE_URL configurada")
    else:
        print("⚠️ DATABASE_URL não configurada - usando SQLite local")
    
    # Email (opcional)
    email_host = os.getenv('EMAIL_HOST')
    if email_host:
        print("✅ EMAIL_HOST configurado")
    else:
        print("⚠️ EMAIL_HOST não configurado - notificações não funcionarão")
    
    # D4Sign (opcional)
    d4sign_token = os.getenv('D4SIGN_API_TOKEN')
    if d4sign_token:
        print("✅ D4SIGN_API_TOKEN configurado")
    else:
        print("⚠️ D4SIGN_API_TOKEN não configurado - assinatura digital não funcionará")

def verificar_arquivos_estaticos():
    """Verifica se os arquivos estáticos estão acessíveis"""
    print("\n📁 Verificando arquivos estáticos:")
    
    # Verificar se o diretório static existe
    static_dir = Path("app/static")
    if static_dir.exists():
        print("✅ Diretório static existe")
        
        # Verificar arquivos importantes
        files_to_check = [
            "manifest.json",
            "sw.js"
        ]
        
        for file in files_to_check:
            file_path = static_dir / file
            if file_path.exists():
                print(f"✅ {file} existe")
            else:
                print(f"❌ {file} não encontrado")
    else:
        print("❌ Diretório static não existe")

def verificar_templates():
    """Verifica se os templates estão corretos"""
    print("\n🎨 Verificando templates:")
    
    templates_dir = Path("app/templates")
    if templates_dir.exists():
        print("✅ Diretório templates existe")
        
        # Verificar templates importantes
        important_templates = [
            "base_modern.html",
            "index.html",
            "listar_contratos.html",
            "listar_boletos.html"
        ]
        
        for template in important_templates:
            template_path = templates_dir / template
            if template_path.exists():
                print(f"✅ {template} existe")
                
                # Verificar se tem JavaScript
                with open(template_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if '<script>' in content:
                        print(f"  ✅ {template} tem JavaScript")
                    else:
                        print(f"  ⚠️ {template} não tem JavaScript")
            else:
                print(f"❌ {template} não encontrado")
    else:
        print("❌ Diretório templates não existe")

def testar_app_local():
    """Testa se o app funciona localmente"""
    print("\n🚀 Testando aplicação local:")
    
    try:
        # Importar app
        from app import app
        
        # Testar se as rotas principais existem
        with app.test_client() as client:
            # Testar rota principal
            response = client.get('/')
            if response.status_code == 200:
                print("✅ Rota principal funciona")
            else:
                print(f"❌ Rota principal retornou {response.status_code}")
            
            # Testar rota de locais
            response = client.get('/locais')
            if response.status_code == 200:
                print("✅ Rota de locais funciona")
            else:
                print(f"❌ Rota de locais retornou {response.status_code}")
            
            # Testar rota de inquilinos
            response = client.get('/inquilinos')
            if response.status_code == 200:
                print("✅ Rota de inquilinos funciona")
            else:
                print(f"❌ Rota de inquilinos retornou {response.status_code}")
            
            # Testar rota de contratos
            response = client.get('/listar_contratos')
            if response.status_code == 200:
                print("✅ Rota de contratos funciona")
            else:
                print(f"❌ Rota de contratos retornou {response.status_code}")
                
    except Exception as e:
        print(f"❌ Erro ao testar aplicação: {e}")

def verificar_problemas_comuns():
    """Verifica problemas comuns que podem afetar os botões"""
    print("\n🔧 Verificando problemas comuns:")
    
    # Verificar se há conflitos de CSS/JS
    base_template = Path("app/templates/base_modern.html")
    if base_template.exists():
        with open(base_template, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Verificar se Tailwind CSS está carregado
            if 'tailwindcss.com' in content:
                print("✅ Tailwind CSS está sendo carregado")
            else:
                print("❌ Tailwind CSS não encontrado")
            
            # Verificar se Font Awesome está carregado
            if 'font-awesome' in content:
                print("✅ Font Awesome está sendo carregado")
            else:
                print("❌ Font Awesome não encontrado")
            
            # Verificar se há JavaScript
            if '<script>' in content:
                print("✅ JavaScript está presente")
            else:
                print("❌ JavaScript não encontrado")

def mostrar_solucoes():
    """Mostra soluções para problemas comuns"""
    print("\n💡 SOLUÇÕES PARA PROBLEMAS DE BOTÕES:")
    print("=" * 50)
    
    print("\n1️⃣ **Problema: Botões não respondem ao clique**")
    print("   Solução: Verificar se o JavaScript está carregando")
    print("   - Abra o console do navegador (F12)")
    print("   - Verifique se há erros de JavaScript")
    print("   - Recarregue a página (Ctrl+F5)")
    
    print("\n2️⃣ **Problema: Links não funcionam**")
    print("   Solução: Verificar se as rotas estão corretas")
    print("   - Teste acessando diretamente a URL")
    print("   - Verifique se o Railway está online")
    print("   - Aguarde 2-3 minutos após deploy")
    
    print("\n3️⃣ **Problema: Formulários não salvam**")
    print("   Solução: Verificar configuração do banco")
    print("   - Configure DATABASE_URL no Railway")
    print("   - Verifique se SECRET_KEY está configurada")
    print("   - Teste localmente primeiro")
    
    print("\n4️⃣ **Problema: CSS não carrega**")
    print("   Solução: Verificar CDNs")
    print("   - Tailwind CSS está sendo carregado via CDN")
    print("   - Font Awesome está sendo carregado via CDN")
    print("   - Se não carregar, pode ser problema de internet")
    
    print("\n5️⃣ **Problema: Sistema lento**")
    print("   Solução: Aguardar inicialização")
    print("   - Railway pode demorar para inicializar")
    print("   - Primeira requisição pode ser lenta")
    print("   - Verificar logs no Railway")

def main():
    """Função principal"""
    print("🚀 DIAGNÓSTICO DE PROBLEMAS DOS BOTÕES NO RAILWAY")
    print("=" * 60)
    
    # Verificar configuração
    verificar_configuracao_railway()
    
    # Verificar arquivos
    verificar_arquivos_estaticos()
    verificar_templates()
    
    # Verificar problemas comuns
    verificar_problemas_comuns()
    
    # Testar app local
    testar_app_local()
    
    # Mostrar soluções
    mostrar_solucoes()
    
    print("\n" + "=" * 60)
    print("📋 RESUMO:")
    print("✅ Se todas as verificações passaram, o problema pode ser:")
    print("   - Cache do navegador (Ctrl+F5)")
    print("   - Railway ainda inicializando (aguarde 2-3 min)")
    print("   - Problema temporário de rede")
    print("   - Variáveis de ambiente não configuradas")
    
    print("\n🎯 PRÓXIMOS PASSOS:")
    print("1. Configure SECRET_KEY no Railway")
    print("2. Faça redeploy no Railway")
    print("3. Aguarde 2-3 minutos")
    print("4. Teste acessando a URL")
    print("5. Se não funcionar, verifique os logs no Railway")

if __name__ == "__main__":
    main() 