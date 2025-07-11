#!/usr/bin/env python3
"""
Teste específico de upload de documentos D4Sign
"""

import requests
import json
import os

def testar_upload_documento():
    """Testa upload de documento usando diferentes métodos"""
    
    # Configurações
    api_token = "live_cd026d4be49abf7c543b913e6f4514aed6c3506874617e07e352fc77fcb3cf2d"
    crypt_key = "live_crypt_MTU7hgVkgnXn2L6ajNa8t1hf6rqnDpRd"
    base_url = "https://sandbox.d4sign.com.br/api/v1"
    
    # Parâmetros de autenticação
    params = {
        'tokenAPI': api_token,
        'cryptKey': crypt_key
    }
    
    # Criar um PDF de teste
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    
    test_pdf = "teste_upload_d4sign.pdf"
    c = canvas.Canvas(test_pdf, pagesize=letter)
    c.drawString(100, 750, "Documento de teste para upload D4Sign")
    c.drawString(100, 700, "Este é um documento de teste para verificar o upload.")
    c.save()
    
    print(f"📄 PDF de teste criado: {test_pdf}")
    
    # Método 1: Upload com files
    print("\n🔧 Método 1: Upload com files")
    try:
        with open(test_pdf, 'rb') as file:
            files = {'file': (test_pdf, file, 'application/pdf')}
            headers = {'Accept': 'application/json'}
            
            response = requests.post(f"{base_url}/documents/upload", 
                                  params=params, headers=headers, files=files)
            
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # Método 2: Upload com data
    print("\n🔧 Método 2: Upload com data")
    try:
        with open(test_pdf, 'rb') as file:
            data = {'file': file.read()}
            headers = {'Accept': 'application/json'}
            
            response = requests.post(f"{base_url}/documents/upload", 
                                  params=params, headers=headers, data=data)
            
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # Método 3: Upload com JSON
    print("\n🔧 Método 3: Upload com JSON")
    try:
        with open(test_pdf, 'rb') as file:
            import base64
            file_content = base64.b64encode(file.read()).decode('utf-8')
            
            data = {
                'file': file_content,
                'filename': test_pdf
            }
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
            
            response = requests.post(f"{base_url}/documents/upload", 
                                  params=params, headers=headers, json=data)
            
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # Limpar arquivo de teste
    if os.path.exists(test_pdf):
        os.remove(test_pdf)
        print(f"\n🗑️ Arquivo de teste removido: {test_pdf}")

if __name__ == "__main__":
    testar_upload_documento() 