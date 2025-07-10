#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste específico para problemas de botões e JavaScript
"""

import os
import sys
from pathlib import Path

def verificar_problemas_javascript():
    """Verifica problemas específicos de JavaScript"""
    print("🔍 TESTE ESPECÍFICO - PROBLEMAS DE BOTÕES")
    print("=" * 50)
    
    # Verificar templates que podem ter problemas
    templates_dir = Path("app/templates")
    
    print("\n1️⃣ VERIFICANDO TEMPLATES COM BOTÕES:")
    
    templates_com_botoes = [
        "listar_contratos.html",
        "listar_boletos.html", 
        "listar_inquilinos.html",
        "index.html"
    ]
    
    for template in templates_com_botoes:
        template_path = templates_dir / template
        if template_path.exists():
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Verificar se estende base_modern.html
                extends_base = '{% extends "base_modern.html" %}' in content
                
                # Verificar se tem botões
                has_buttons = 'href=' in content or 'onclick=' in content
                
                # Verificar se tem JavaScript
                has_js = '<script>' in content
                
                print(f"\n📄 {template}:")
                print(f"   - Estende base_modern: {'✅' if extends_base else '❌'}")
                print(f"   - Tem botões/links: {'✅' if has_buttons else '❌'}")
                print(f"   - Tem JavaScript: {'✅' if has_js else '❌'}")
                
                if not extends_base:
                    print(f"   ⚠️ PROBLEMA: {template} não estende base_modern.html")
                
        else:
            print(f"❌ {template} não encontrado")

def verificar_base_template():
    """Verifica se o template base está correto"""
    print("\n2️⃣ VERIFICANDO TEMPLATE BASE:")
    
    base_template = Path("app/templates/base_modern.html")
    if base_template.exists():
        with open(base_template, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Verificar elementos essenciais
            has_tailwind = 'tailwindcss.com' in content
            has_fontawesome = 'font-awesome' in content
            has_jquery = 'jquery' in content.lower()
            has_js = '<script>' in content
            has_css = '<style>' in content or 'tailwind' in content
            
            print(f"✅ base_modern.html encontrado")
            print(f"   - Tailwind CSS: {'✅' if has_tailwind else '❌'}")
            print(f"   - Font Awesome: {'✅' if has_fontawesome else '❌'}")
            print(f"   - JavaScript: {'✅' if has_js else '❌'}")
            print(f"   - CSS: {'✅' if has_css else '❌'}")
            
            if not has_tailwind:
                print("   ⚠️ PROBLEMA: Tailwind CSS não encontrado")
            if not has_fontawesome:
                print("   ⚠️ PROBLEMA: Font Awesome não encontrado")
            if not has_js:
                print("   ⚠️ PROBLEMA: JavaScript não encontrado")
                
    else:
        print("❌ base_modern.html não encontrado")

def verificar_rotas_com_botoes():
    """Verifica rotas que podem ter problemas com botões"""
    print("\n3️⃣ VERIFICANDO ROTAS COM BOTÕES:")
    
    try:
        from app import app
        
        with app.test_client() as client:
            # Testar rotas que têm botões
            rotas_com_botoes = [
                ('/listar_contratos', 'Listar Contratos'),
                ('/listar_boletos', 'Listar Boletos'),
                ('/listar_inquilinos', 'Listar Inquilinos'),
                ('/locais', 'Listar Locais')
            ]
            
            for rota, descricao in rotas_com_botoes:
                try:
                    response = client.get(rota)
                    if response.status_code == 200:
                        # Verificar se a resposta tem botões
                        content = response.get_data(as_text=True)
                        has_buttons = 'href=' in content or 'onclick=' in content
                        has_js = '<script>' in content
                        
                        print(f"✅ {descricao}:")
                        print(f"   - Status: {response.status_code}")
                        print(f"   - Tem botões: {'✅' if has_buttons else '❌'}")
                        print(f"   - Tem JavaScript: {'✅' if has_js else '❌'}")
                        
                        if not has_buttons:
                            print(f"   ⚠️ PROBLEMA: {descricao} não tem botões")
                        if not has_js:
                            print(f"   ⚠️ PROBLEMA: {descricao} não tem JavaScript")
                            
                    else:
                        print(f"❌ {descricao}: {response.status_code}")
                        
                except Exception as e:
                    print(f"❌ Erro em {descricao}: {e}")
                    
    except Exception as e:
        print(f"❌ Erro ao testar rotas: {e}")

def verificar_problemas_especificos():
    """Verifica problemas específicos conhecidos"""
    print("\n4️⃣ VERIFICANDO PROBLEMAS ESPECÍFICOS:")
    
    # Verificar se há conflitos de CSS/JS
    base_template = Path("app/templates/base_modern.html")
    if base_template.exists():
        with open(base_template, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Verificar problemas conhecidos
            has_conflict = '!important' in content
            has_inline_js = 'onclick=' in content
            has_external_js = 'src=' in content and 'script' in content
            
            print(f"   - CSS conflitos: {'⚠️' if has_conflict else '✅'}")
            print(f"   - JavaScript inline: {'⚠️' if has_inline_js else '✅'}")
            print(f"   - JavaScript externo: {'✅' if has_external_js else '❌'}")

def mostrar_solucoes_especificas():
    """Mostra soluções específicas para problemas de botões"""
    print("\n🔧 SOLUÇÕES ESPECÍFICAS PARA BOTÕES:")
    print("=" * 50)
    
    print("\n1️⃣ **Se os botões não respondem ao clique:**")
    print("   - Verifique console do navegador (F12)")
    print("   - Procure por erros de JavaScript")
    print("   - Teste em modo incógnito")
    print("   - Limpe cache (Ctrl+F5)")
    
    print("\n2️⃣ **Se os links não funcionam:**")
    print("   - Teste acessando URLs diretamente")
    print("   - Verifique se as rotas existem")
    print("   - Teste localmente primeiro")
    
    print("\n3️⃣ **Se o CSS não carrega:**")
    print("   - Verifique se Tailwind CSS está carregando")
    print("   - Verifique se Font Awesome está carregando")
    print("   - Teste com conexão de internet diferente")
    
    print("\n4️⃣ **Se formulários não salvam:**")
    print("   - Verifique se SECRET_KEY está configurada")
    print("   - Verifique se DATABASE_URL está configurada")
    print("   - Teste localmente primeiro")

def main():
    """Função principal"""
    print("🚀 TESTE ESPECÍFICO - PROBLEMAS DE BOTÕES")
    print("=" * 50)
    
    # Executar testes específicos
    verificar_problemas_javascript()
    verificar_base_template()
    verificar_rotas_com_botoes()
    verificar_problemas_especificos()
    
    # Mostrar soluções
    mostrar_solucoes_especificas()
    
    print("\n" + "=" * 50)
    print("🎯 PRÓXIMOS PASSOS:")
    print("1. Se encontrou problemas nos templates:")
    print("   - Corrija os templates que não estendem base_modern.html")
    print("   - Verifique se todos têm JavaScript")
    
    print("\n2. Se não encontrou problemas:")
    print("   - O problema pode ser de cache do navegador")
    print("   - Teste em modo incógnito")
    print("   - Verifique console do navegador (F12)")
    
    print("\n💡 DICA IMPORTANTE:")
    print("Se o sistema funciona localmente mas não no Railway,")
    print("o problema pode ser de CDN (Tailwind/FontAwesome)")

if __name__ == "__main__":
    main() 