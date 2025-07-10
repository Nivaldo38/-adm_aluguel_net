#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste completo de todos os botões do sistema
"""

import os
import sys
from pathlib import Path

def testar_todas_as_paginas():
    """Testa todas as páginas principais do sistema"""
    print("🔍 TESTE COMPLETO DE TODOS OS BOTÕES")
    print("=" * 50)
    
    try:
        from app import app
        
        with app.test_client() as client:
            # Lista de todas as páginas principais
            paginas = [
                ('/', 'Página Inicial'),
                ('/dashboard', 'Dashboard Básico'),
                ('/dashboard_avancado', 'Dashboard Avançado'),
                ('/relatorios', 'Relatórios'),
                ('/locais', 'Locais'),
                ('/inquilinos', 'Inquilinos'),
                ('/listar_contratos', 'Listar Contratos'),
                ('/boletos', 'Boletos'),
                ('/notificacoes', 'Notificações'),
                ('/backup', 'Backup'),
                ('/historico', 'Histórico')
            ]
            
            resultados = {}
            
            for rota, descricao in paginas:
                try:
                    response = client.get(rota)
                    if response.status_code == 200:
                        content = response.get_data(as_text=True)
                        
                        # Verificar elementos importantes
                        has_buttons = 'href=' in content or 'onclick=' in content
                        has_js = '<script>' in content
                        has_tailwind = 'tailwind' in content.lower()
                        has_fontawesome = 'fas fa-' in content
                        has_modern_styles = 'bg-gradient-to-r from-blue-600 to-purple-600' in content
                        
                        resultados[descricao] = {
                            'status': response.status_code,
                            'has_buttons': has_buttons,
                            'has_js': has_js,
                            'has_tailwind': has_tailwind,
                            'has_fontawesome': has_fontawesome,
                            'has_modern_styles': has_modern_styles,
                            'content_length': len(content)
                        }
                        
                        print(f"\n✅ {descricao}:")
                        print(f"   - Status: {response.status_code}")
                        print(f"   - Tem botões: {'✅' if has_buttons else '❌'}")
                        print(f"   - Tem JavaScript: {'✅' if has_js else '❌'}")
                        print(f"   - Tem Tailwind: {'✅' if has_tailwind else '❌'}")
                        print(f"   - Tem FontAwesome: {'✅' if has_fontawesome else '❌'}")
                        print(f"   - Tem estilos modernos: {'✅' if has_modern_styles else '❌'}")
                        
                        if not has_buttons:
                            print(f"   ⚠️ PROBLEMA: {descricao} não tem botões")
                        if not has_js:
                            print(f"   ⚠️ PROBLEMA: {descricao} não tem JavaScript")
                        if not has_modern_styles:
                            print(f"   ⚠️ PROBLEMA: {descricao} não usa template moderno")
                            
                    else:
                        print(f"❌ {descricao}: {response.status_code}")
                        resultados[descricao] = {'status': response.status_code, 'error': True}
                        
                except Exception as e:
                    print(f"❌ Erro em {descricao}: {e}")
                    resultados[descricao] = {'error': str(e)}
            
            return resultados
                    
    except Exception as e:
        print(f"❌ Erro ao testar páginas: {e}")
        return {}

def verificar_botoes_especificos():
    """Verifica botões específicos que podem ter problemas"""
    print("\n🎯 VERIFICANDO BOTÕES ESPECÍFICOS:")
    
    botoes_importantes = [
        'cadastrar_contrato',
        'cadastrar_inquilino', 
        'cadastrar_local',
        'listar_contratos',
        'listar_inquilinos',
        'listar_boletos',
        'gerar_boleto',
        'marcar_pago',
        'excluir_contrato',
        'excluir_inquilino',
        'editar_contrato',
        'editar_inquilino'
    ]
    
    routes_file = Path("app/routes.py")
    if routes_file.exists():
        with open(routes_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
            for botao in botoes_importantes:
                rota_encontrada = f'@app.route(\'/{botao}\')' in content or f'@app.route(\'/{botao}/' in content
                print(f"   - {botao}: {'✅' if rota_encontrada else '❌'}")

def verificar_templates_problematicos():
    """Verifica templates que podem ter problemas"""
    print("\n📄 VERIFICANDO TEMPLATES PROBLEMÁTICOS:")
    
    templates_dir = Path("app/templates")
    templates_problematicos = [
        "listar_boletos.html",
        "listar_inquilinos.html", 
        "listar_contratos.html",
        "cadastrar_contrato.html",
        "cadastrar_inquilino.html"
    ]
    
    for template in templates_problematicos:
        template_path = templates_dir / template
        if template_path.exists():
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                extends_base = '{% extends "base_modern.html" %}' in content
                has_buttons = 'href=' in content or 'onclick=' in content
                has_js = '<script>' in content
                
                print(f"\n📄 {template}:")
                print(f"   - Estende base_modern: {'✅' if extends_base else '❌'}")
                print(f"   - Tem botões: {'✅' if has_buttons else '❌'}")
                print(f"   - Tem JavaScript: {'✅' if has_js else '❌'}")
                
                if not extends_base:
                    print(f"   ⚠️ PROBLEMA: {template} não estende base_modern.html")
                if not has_buttons:
                    print(f"   ⚠️ PROBLEMA: {template} não tem botões")
                if not has_js:
                    print(f"   ⚠️ PROBLEMA: {template} não tem JavaScript")
        else:
            print(f"❌ {template} não encontrado")

def mostrar_recomendacoes():
    """Mostra recomendações baseadas nos resultados"""
    print("\n💡 RECOMENDAÇÕES:")
    print("=" * 30)
    
    print("\n1️⃣ **Se os botões não funcionam no Railway:**")
    print("   - Verifique se o deploy foi concluído")
    print("   - Limpe o cache do navegador (Ctrl+F5)")
    print("   - Teste em modo incógnito")
    print("   - Verifique os logs do Railway")
    
    print("\n2️⃣ **Se algumas páginas não carregam:**")
    print("   - Verifique se as rotas estão definidas")
    print("   - Verifique se os templates existem")
    print("   - Verifique se há erros no console (F12)")
    
    print("\n3️⃣ **Se o CSS/JS não carrega:**")
    print("   - Verifique se base_modern.html está sendo usado")
    print("   - Verifique se Tailwind CSS está carregando")
    print("   - Verifique se FontAwesome está carregando")
    
    print("\n4️⃣ **Para testar no Railway:**")
    print("   - Acesse a URL do Railway")
    print("   - Teste cada página individualmente")
    print("   - Verifique se os botões respondem ao clique")
    print("   - Teste em diferentes navegadores")

def main():
    """Função principal"""
    print("🚀 TESTE COMPLETO DE TODOS OS BOTÕES")
    print("=" * 50)
    
    # Executar testes
    resultados = testar_todas_as_paginas()
    verificar_botoes_especificos()
    verificar_templates_problematicos()
    
    # Mostrar recomendações
    mostrar_recomendacoes()
    
    print("\n" + "=" * 50)
    print("🎯 PRÓXIMOS PASSOS:")
    print("1. Aguarde o deploy no Railway (2-3 minutos)")
    print("2. Acesse a URL do Railway")
    print("3. Teste cada página individualmente")
    print("4. Verifique se os botões funcionam")
    print("5. Se houver problemas, me informe quais páginas/botões")
    
    print("\n💡 DICA IMPORTANTE:")
    print("Se os botões ainda não funcionam após o deploy,")
    print("pode ser necessário limpar o cache do navegador")

if __name__ == "__main__":
    main() 