#!/usr/bin/env python3
"""
Teste de endpoints disponíveis na API D4Sign
"""

import requests
import json

def testar_endpoints():
    """Testa diferentes endpoints da API D4Sign"""
    
    # Configurações
    api_token = "live_cd026d4be49abf7c543b913e6f4514aed6c3506874617e07e352fc77fcb3cf2d"
    crypt_key = "live_crypt_MTU7hgVkgnXn2L6ajNa8t1hf6rqnDpRd"
    base_url = "https://sandbox.d4sign.com.br/api/v1"
    
    # Parâmetros de autenticação
    params = {
        'tokenAPI': api_token,
        'cryptKey': crypt_key
    }
    
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    
    # Lista de endpoints para testar
    endpoints = [
        'account',
        'documents',
        'documents/upload',
        'envelopes',
        'envelopes/create',
        'envelopes/send',
        'webhooks',
        'signers',
        'folders'
    ]
    
    print("🔍 Testando endpoints da API D4Sign...")
    print("=" * 50)
    
    for endpoint in endpoints:
        try:
            print(f"\n📡 Testando: {endpoint}")
            response = requests.get(f"{base_url}/{endpoint}", params=params, headers=headers)
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"✅ Sucesso: {json.dumps(data, indent=2, ensure_ascii=False)[:200]}...")
                except:
                    print(f"✅ Sucesso (não JSON): {response.text[:200]}...")
            else:
                try:
                    error_data = response.json()
                    print(f"❌ Erro: {json.dumps(error_data, indent=2, ensure_ascii=False)}")
                except:
                    print(f"❌ Erro: {response.text}")
                    
        except Exception as e:
            print(f"❌ Exceção: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Teste de endpoints concluído!")

if __name__ == "__main__":
    testar_endpoints() 