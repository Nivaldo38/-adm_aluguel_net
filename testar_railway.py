#!/usr/bin/env python3
"""
Script para testar o deploy no Railway
"""

import requests
import time

def test_railway_deploy():
    """Testa se o Railway está funcionando"""
    print("🔍 Testando deploy no Railway...")
    
    # URL do Railway (substitua pela sua URL real)
    railway_url = "https://adm-aluguel-net-production.up.railway.app"
    
    try:
        # Testar página principal
        print(f"📡 Testando: {railway_url}")
        response = requests.get(railway_url, timeout=10)
        
        if response.status_code == 200:
            print("✅ Página principal funcionando!")
        else:
            print(f"⚠️ Página principal retornou status {response.status_code}")
            
        # Testar endpoint de boletos
        print(f"📡 Testando: {railway_url}/boletos")
        response = requests.get(f"{railway_url}/boletos", timeout=10)
        
        if response.status_code == 200:
            print("✅ Endpoint /boletos funcionando!")
        else:
            print(f"❌ Endpoint /boletos retornou status {response.status_code}")
            
        # Testar outros endpoints importantes
        endpoints = [
            "/listar_contratos",
            "/inquilinos", 
            "/locais"
        ]
        
        for endpoint in endpoints:
            try:
                response = requests.get(f"{railway_url}{endpoint}", timeout=5)
                if response.status_code == 200:
                    print(f"✅ {endpoint} funcionando!")
                else:
                    print(f"⚠️ {endpoint} retornou status {response.status_code}")
            except Exception as e:
                print(f"❌ Erro ao testar {endpoint}: {e}")
                
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro de conexão: {e}")
        print("💡 Verifique se o Railway está rodando e a URL está correta")
        
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

if __name__ == "__main__":
    test_railway_deploy() 