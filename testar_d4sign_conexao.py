#!/usr/bin/env python3
"""
Script para testar conexão com D4Sign
"""

import os
import sys
import requests
import json

def testar_conexao_d4sign():
    """Testa conexão básica com D4Sign"""
    
    print("🔍 Testando conexão com D4Sign...")
    
    # Configurações
    api_token = "live_cd026d4be49abf7c543b913e6f4514aed6c3506874617e07e352fc77fcb3cf2d"
    crypt_key = "live_crypt_MTU7hgVkgnXn2L6ajNa8t1hf6rqnDpRd"
    base_url = "https://sandbox.d4sign.com.br/api/v1"
    
    # Parâmetros de autenticação
    params = {
        'tokenAPI': api_token,
        'cryptKey': crypt_key
    }
    
    # Headers
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    
    try:
        # Teste 1: Informações da conta (endpoint correto)
        print("\n📊 Teste 1: Informações da conta...")
        response = requests.get(f"{base_url}/account", params=params, headers=headers)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print("✅ Conexão bem-sucedida!")
                print(f"📋 Dados da conta: {json.dumps(data, indent=2, ensure_ascii=False)}")
            except json.JSONDecodeError:
                print(f"⚠️ Resposta não é JSON válido: {response.text}")
        else:
            print(f"❌ Erro na conexão: {response.status_code}")
            print(f"Resposta: {response.text}")
        
        # Teste 2: Listar documentos (endpoint correto)
        print("\n📄 Teste 2: Listar documentos...")
        response = requests.get(f"{base_url}/documents", params=params, headers=headers)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print("✅ Lista de documentos obtida!")
                print(f"📋 Documentos: {json.dumps(data, indent=2, ensure_ascii=False)}")
            except json.JSONDecodeError:
                print(f"⚠️ Resposta não é JSON válido: {response.text}")
        else:
            print(f"❌ Erro ao listar documentos: {response.status_code}")
            print(f"Resposta: {response.text}")
        
        # Teste 3: Listar envelopes (endpoint correto)
        print("\n✉️ Teste 3: Listar envelopes...")
        response = requests.get(f"{base_url}/envelopes", params=params, headers=headers)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print("✅ Lista de envelopes obtida!")
                print(f"📋 Envelopes: {json.dumps(data, indent=2, ensure_ascii=False)}")
            except json.JSONDecodeError:
                print(f"⚠️ Resposta não é JSON válido: {response.text}")
        else:
            print(f"❌ Erro ao listar envelopes: {response.status_code}")
            print(f"Resposta: {response.text}")
            
        # Teste 4: Listar webhooks (endpoint correto)
        print("\n🔗 Teste 4: Listar webhooks...")
        response = requests.get(f"{base_url}/webhooks", params=params, headers=headers)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print("✅ Lista de webhooks obtida!")
                print(f"📋 Webhooks: {json.dumps(data, indent=2, ensure_ascii=False)}")
            except json.JSONDecodeError:
                print(f"⚠️ Resposta não é JSON válido: {response.text}")
        else:
            print(f"❌ Erro ao listar webhooks: {response.status_code}")
            print(f"Resposta: {response.text}")
            
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Erro de conexão: {e}")
    except requests.exceptions.Timeout as e:
        print(f"❌ Timeout: {e}")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

def testar_upload_documento():
    """Testa upload de documento"""
    
    print("\n📤 Testando upload de documento...")
    
    api_token = "live_cd026d4be49abf7c543b913e6f4514aed6c3506874617e07e352fc77fcb3cf2d"
    crypt_key = "live_crypt_MTU7hgVkgnXn2L6ajNa8t1hf6rqnDpRd"
    base_url = "https://sandbox.d4sign.com.br/api/v1"
    
    params = {
        'tokenAPI': api_token,
        'cryptKey': crypt_key
    }
    
    headers = {
        'Accept': 'application/json'
    }
    
    try:
        # Criar um PDF de teste simples
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        
        test_pdf = "teste_d4sign.pdf"
        c = canvas.Canvas(test_pdf, pagesize=letter)
        c.drawString(100, 750, "Documento de teste para D4Sign")
        c.drawString(100, 700, "Este é um documento de teste para verificar a integração.")
        c.drawString(100, 650, "Data: " + str(datetime.now().strftime('%d/%m/%Y %H:%M:%S')))
        c.save()
        
        print(f"📄 PDF de teste criado: {test_pdf}")
        
        # Upload do documento
        with open(test_pdf, 'rb') as file:
            files = {'file': (test_pdf, file, 'application/pdf')}
            response = requests.post(f"{base_url}/documents/upload", 
                                  params=params, headers=headers, files=files)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print("✅ Upload realizado com sucesso!")
                print(f"📋 Resposta: {json.dumps(data, indent=2, ensure_ascii=False)}")
                
                # Salvar o doc_key para uso posterior
                doc_key = data.get('uuid') or data.get('key')
                if doc_key:
                    with open('doc_key_test.txt', 'w') as f:
                        f.write(doc_key)
                    print(f"💾 Doc Key salvo: {doc_key}")
                    
            except json.JSONDecodeError:
                print(f"⚠️ Resposta não é JSON válido: {response.text}")
        else:
            print(f"❌ Erro no upload: {response.status_code}")
            print(f"Resposta: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro ao testar upload: {e}")

def main():
    print("🚀 Iniciando testes de conexão D4Sign...")
    print("=" * 50)
    
    testar_conexao_d4sign()
    testar_upload_documento()
    
    print("\n" + "=" * 50)
    print("✅ Testes concluídos!")

if __name__ == "__main__":
    from datetime import datetime
    main() 