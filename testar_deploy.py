#!/usr/bin/env python3
"""
Script para testar deploy e funcionalidades do AluguelNet
"""

import requests
import time
import sys
import os

def test_web_app(url):
    """Testa a aplicação web"""
    print("🌐 Testando aplicação web...")
    
    try:
        # Teste básico
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print("✅ Aplicação web funcionando")
            return True
        else:
            print(f"❌ Erro HTTP: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        return False

def test_mobile_app(url):
    """Testa a aplicação mobile"""
    print("📱 Testando aplicação mobile...")
    
    try:
        mobile_url = f"{url}/mobile/"
        response = requests.get(mobile_url, timeout=10)
        if response.status_code == 200:
            print("✅ Aplicação mobile funcionando")
            return True
        else:
            print(f"❌ Erro HTTP Mobile: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro ao conectar mobile: {e}")
        return False

def test_pwa_features(url):
    """Testa recursos PWA"""
    print("🔧 Testando recursos PWA...")
    
    try:
        # Teste manifest
        manifest_url = f"{url}/static/manifest.json"
        response = requests.get(manifest_url, timeout=10)
        if response.status_code == 200:
            print("✅ Manifest PWA funcionando")
        else:
            print("❌ Manifest PWA não encontrado")
            
        # Teste service worker
        sw_url = f"{url}/static/sw.js"
        response = requests.get(sw_url, timeout=10)
        if response.status_code == 200:
            print("✅ Service Worker funcionando")
        else:
            print("❌ Service Worker não encontrado")
            
        return True
    except Exception as e:
        print(f"❌ Erro ao testar PWA: {e}")
        return False

def test_api_endpoints(url):
    """Testa endpoints da API"""
    print("🔌 Testando endpoints da API...")
    
    endpoints = [
        "/api/unidades/1",
        "/listar_contratos",
        "/listar_inquilinos",
        "/locais"
    ]
    
    success_count = 0
    for endpoint in endpoints:
        try:
            response = requests.get(f"{url}{endpoint}", timeout=10)
            if response.status_code in [200, 302]:
                print(f"✅ {endpoint} - OK")
                success_count += 1
            else:
                print(f"❌ {endpoint} - {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint} - Erro: {e}")
    
    return success_count >= len(endpoints) * 0.8  # 80% de sucesso

def test_performance(url):
    """Testa performance"""
    print("⚡ Testando performance...")
    
    try:
        start_time = time.time()
        response = requests.get(url, timeout=10)
        end_time = time.time()
        
        response_time = (end_time - start_time) * 1000  # ms
        
        if response_time < 2000:  # menos de 2 segundos
            print(f"✅ Performance OK: {response_time:.0f}ms")
            return True
        else:
            print(f"⚠️ Performance lenta: {response_time:.0f}ms")
            return False
    except Exception as e:
        print(f"❌ Erro ao testar performance: {e}")
        return False

def generate_report(url, results):
    """Gera relatório de teste"""
    print("\n" + "="*50)
    print("📊 RELATÓRIO DE TESTE")
    print("="*50)
    
    print(f"🌐 URL Testada: {url}")
    print(f"⏰ Data/Hora: {time.strftime('%d/%m/%Y %H:%M:%S')}")
    print()
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    success_rate = (passed_tests / total_tests) * 100
    
    print("📋 Resultados:")
    for test_name, result in results.items():
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"  {test_name}: {status}")
    
    print()
    print(f"📈 Taxa de Sucesso: {success_rate:.1f}% ({passed_tests}/{total_tests})")
    
    if success_rate >= 80:
        print("🎉 DEPLOY SUCESSO!")
        print("✅ Sistema pronto para produção")
    elif success_rate >= 60:
        print("⚠️ DEPLOY PARCIAL")
        print("🔧 Alguns ajustes necessários")
    else:
        print("❌ DEPLOY FALHOU")
        print("🔧 Revisão necessária")
    
    print()
    print("📱 Para testar no celular:")
    print(f"   {url}/mobile/")
    print()
    print("🔧 Para configurar:")
    print("   - Email: configurar SMTP")
    print("   - DS4: configurar credenciais")
    print("   - Backup: verificar agendamento")

def main():
    """Função principal"""
    print("🚀 TESTE DE DEPLOY - ALUGUELNET")
    print("="*50)
    
    # URL do deploy (substitua pela sua)
    url = input("Digite a URL do seu deploy (ex: https://aluguelnet.onrender.com): ").strip()
    
    if not url:
        print("❌ URL não fornecida")
        sys.exit(1)
    
    # Remove trailing slash
    url = url.rstrip('/')
    
    print(f"\n🔍 Testando: {url}")
    print()
    
    # Executar testes
    results = {
        "Aplicação Web": test_web_app(url),
        "Aplicação Mobile": test_mobile_app(url),
        "Recursos PWA": test_pwa_features(url),
        "Endpoints API": test_api_endpoints(url),
        "Performance": test_performance(url)
    }
    
    # Gerar relatório
    generate_report(url, results)
    
    # Salvar relatório
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    report_file = f"deploy_test_{timestamp}.txt"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(f"Relatório de Deploy - {timestamp}\n")
        f.write(f"URL: {url}\n")
        f.write(f"Resultados: {results}\n")
    
    print(f"\n📄 Relatório salvo: {report_file}")

if __name__ == "__main__":
    main() 