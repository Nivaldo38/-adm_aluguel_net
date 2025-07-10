#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste específico para dashboard avançado e relatórios
"""

import os
import sys
from pathlib import Path

def testar_rotas_especificas():
    """Testa as rotas específicas que estão com problemas"""
    print("🔍 TESTE ESPECÍFICO - DASHBOARD E RELATÓRIOS")
    print("=" * 50)
    
    try:
        from app import app
        
        with app.test_client() as client:
            # Testar rotas específicas
            rotas_problematicas = [
                ('/dashboard_avancado', 'Dashboard Avançado'),
                ('/relatorios', 'Relatórios')
            ]
            
            for rota, descricao in rotas_problematicas:
                try:
                    response = client.get(rota)
                    if response.status_code == 200:
                        content = response.get_data(as_text=True)
                        
                        # Verificar elementos específicos
                        has_buttons = 'href=' in content or 'onclick=' in content
                        has_js = '<script>' in content
                        has_tailwind = 'tailwind' in content.lower()
                        has_fontawesome = 'fas fa-' in content
                        
                        print(f"\n✅ {descricao}:")
                        print(f"   - Status: {response.status_code}")
                        print(f"   - Tem botões: {'✅' if has_buttons else '❌'}")
                        print(f"   - Tem JavaScript: {'✅' if has_js else '❌'}")
                        print(f"   - Tem Tailwind: {'✅' if has_tailwind else '❌'}")
                        print(f"   - Tem FontAwesome: {'✅' if has_fontawesome else '❌'}")
                        
                        if not has_buttons:
                            print(f"   ⚠️ PROBLEMA: {descricao} não tem botões")
                        if not has_js:
                            print(f"   ⚠️ PROBLEMA: {descricao} não tem JavaScript")
                        if not has_tailwind:
                            print(f"   ⚠️ PROBLEMA: {descricao} não tem Tailwind CSS")
                        if not has_fontawesome:
                            print(f"   ⚠️ PROBLEMA: {descricao} não tem FontAwesome")
                            
                    else:
                        print(f"❌ {descricao}: {response.status_code}")
                        
                except Exception as e:
                    print(f"❌ Erro em {descricao}: {e}")
                    
    except Exception as e:
        print(f"❌ Erro ao testar rotas: {e}")

def verificar_templates_especificos():
    """Verifica os templates específicos"""
    print("\n🎨 VERIFICANDO TEMPLATES ESPECÍFICOS:")
    
    templates_especificos = [
        "dashboard_avancado.html",
        "relatorios.html"
    ]
    
    templates_dir = Path("app/templates")
    
    for template in templates_especificos:
        template_path = templates_dir / template
        if template_path.exists():
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Verificar elementos
                extends_base = '{% extends "base_modern.html" %}' in content
                has_buttons = 'href=' in content or 'onclick=' in content
                has_js = '<script>' in content
                has_tailwind = 'tailwind' in content.lower()
                has_fontawesome = 'fas fa-' in content
                
                print(f"\n📄 {template}:")
                print(f"   - Estende base_modern: {'✅' if extends_base else '❌'}")
                print(f"   - Tem botões: {'✅' if has_buttons else '❌'}")
                print(f"   - Tem JavaScript: {'✅' if has_js else '❌'}")
                print(f"   - Tem Tailwind: {'✅' if has_tailwind else '❌'}")
                print(f"   - Tem FontAwesome: {'✅' if has_fontawesome else '❌'}")
                
                if not extends_base:
                    print(f"   ⚠️ PROBLEMA: {template} não estende base_modern.html")
                if not has_buttons:
                    print(f"   ⚠️ PROBLEMA: {template} não tem botões")
                if not has_js:
                    print(f"   ⚠️ PROBLEMA: {template} não tem JavaScript")
                    
        else:
            print(f"❌ {template} não encontrado")

def verificar_rotas_no_codigo():
    """Verifica se as rotas estão definidas no código"""
    print("\n🔧 VERIFICANDO ROTAS NO CÓDIGO:")
    
    routes_file = Path("app/routes.py")
    if routes_file.exists():
        with open(routes_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Verificar se as rotas estão definidas
            has_dashboard = '@app.route(\'/dashboard_avancado\')' in content
            has_relatorios = '@app.route(\'/relatorios\')' in content
            
            print(f"   - Dashboard avançado: {'✅' if has_dashboard else '❌'}")
            print(f"   - Relatórios: {'✅' if has_relatorios else '❌'}")
            
            if not has_dashboard:
                print("   ⚠️ PROBLEMA: Rota dashboard_avancado não encontrada")
            if not has_relatorios:
                print("   ⚠️ PROBLEMA: Rota relatorios não encontrada")
    else:
        print("❌ app/routes.py não encontrado")

def mostrar_solucoes_especificas():
    """Mostra soluções específicas"""
    print("\n🔧 SOLUÇÕES ESPECÍFICAS:")
    print("=" * 30)
    
    print("\n1️⃣ **Se os botões não funcionam no dashboard/relatórios:**")
    print("   - Verifique se as rotas estão definidas em app/routes.py")
    print("   - Verifique se os templates estendem base_modern.html")
    print("   - Verifique se há JavaScript nos templates")
    
    print("\n2️⃣ **Se as páginas não carregam:**")
    print("   - Verifique se as rotas estão corretas")
    print("   - Verifique se há erros no console (F12)")
    print("   - Teste acessando URLs diretamente")
    
    print("\n3️⃣ **Se o CSS não carrega:**")
    print("   - Verifique se Tailwind CSS está sendo carregado")
    print("   - Verifique se FontAwesome está sendo carregado")
    print("   - Teste em modo incógnito")

def main():
    """Função principal"""
    print("🚀 TESTE ESPECÍFICO - DASHBOARD E RELATÓRIOS")
    print("=" * 50)
    
    # Executar testes específicos
    testar_rotas_especificas()
    verificar_templates_especificos()
    verificar_rotas_no_codigo()
    
    # Mostrar soluções
    mostrar_solucoes_especificas()
    
    print("\n" + "=" * 50)
    print("🎯 PRÓXIMOS PASSOS:")
    print("1. Se encontrou problemas nas rotas:")
    print("   - Verifique se as rotas estão definidas em app/routes.py")
    print("   - Verifique se os templates existem")
    
    print("\n2. Se encontrou problemas nos templates:")
    print("   - Corrija os templates que não estendem base_modern.html")
    print("   - Adicione JavaScript se necessário")
    
    print("\n💡 DICA IMPORTANTE:")
    print("Se as páginas carregam mas os botões não funcionam,")
    print("o problema pode ser de JavaScript ou CSS não carregando")

if __name__ == "__main__":
    main() 