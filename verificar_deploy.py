#!/usr/bin/env python3
"""
Script para verificar o status do deploy no Railway
"""

import requests
import json

def verificar_deploy():
    """Verifica o status do deploy no Railway"""
    print("🔍 Verificando status do deploy no Railway...")
    
    # URLs para testar
    urls = [
        "https://adm-aluguel-net-production.up.railway.app",
        "https://adm-aluguel-net-production.up.railway.app/",
        "https://adm-aluguel-net-production.up.railway.app/health",
        "https://adm-aluguel-net-production.up.railway.app/status"
    ]
    
    for url in urls:
        try:
            print(f"📡 Testando: {url}")
            response = requests.get(url, timeout=10)
            print(f"   Status: {response.status_code}")
            print(f"   Headers: {dict(response.headers)}")
            
            if response.status_code == 200:
                print("   ✅ Funcionando!")
            elif response.status_code == 404:
                print("   ❌ Página não encontrada")
            elif response.status_code == 500:
                print("   ❌ Erro interno do servidor")
            else:
                print(f"   ⚠️ Status inesperado: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print("   ❌ Erro de conexão - servidor pode estar offline")
        except requests.exceptions.Timeout:
            print("   ⏰ Timeout - servidor pode estar lento")
        except Exception as e:
            print(f"   ❌ Erro: {e}")
    
    print("\n💡 Dicas para resolver:")
    print("1. Acesse o painel do Railway em https://railway.app")
    print("2. Verifique se o deploy foi concluído com sucesso")
    print("3. Verifique os logs do Railway para identificar erros")
    print("4. Confirme se a URL está correta")
    print("5. Tente fazer um redeploy se necessário")

if __name__ == "__main__":
    verificar_deploy() 