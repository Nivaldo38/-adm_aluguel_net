#!/usr/bin/env python3
"""
Script para testar a funcionalidade DS4 (DocuSign)
"""

import os
import sys
from app import app, db
from app.models import Contrato
from app.ds4_integration import DS4Integration

def testar_ds4():
    """Testa a funcionalidade DS4"""
    print("🔍 Testando Integração DS4...")
    
    # Verificar configuração
    print("\n1. Verificando configuração DS4:")
    ds4 = DS4Integration()
    
    if not ds4.account_id:
        print("❌ DS4_ACCOUNT_ID não configurado")
        print("   Configure: $env:DS4_ACCOUNT_ID='sua_account_id'")
    else:
        print("✅ DS4_ACCOUNT_ID configurado")
    
    if not ds4.integration_key:
        print("❌ DS4_INTEGRATION_KEY não configurado")
        print("   Configure: $env:DS4_INTEGRATION_KEY='sua_integration_key'")
    else:
        print("✅ DS4_INTEGRATION_KEY configurado")
    
    if not ds4.user_id:
        print("❌ DS4_USER_ID não configurado")
        print("   Configure: $env:DS4_USER_ID='seu_user_id'")
    else:
        print("✅ DS4_USER_ID configurado")
    
    if not ds4.private_key_path:
        print("❌ DS4_PRIVATE_KEY_PATH não configurado")
        print("   Configure: $env:DS4_PRIVATE_KEY_PATH='caminho/para/private_key.pem'")
    else:
        print("✅ DS4_PRIVATE_KEY_PATH configurado")
    
    # Verificar contratos
    print("\n2. Verificando contratos disponíveis:")
    with app.app_context():
        contratos = Contrato.query.all()
        print(f"   Encontrados {len(contratos)} contratos")
        
        for contrato in contratos[:3]:  # Mostrar apenas os 3 primeiros
            print(f"   - ID: {contrato.id}, Inquilino: {contrato.inquilino.nome}")
            print(f"     Status Assinatura: {contrato.status_assinatura or 'Não enviado'}")
            print(f"     Envelope ID: {contrato.envelope_id or 'N/A'}")
    
    # Testar token de acesso
    print("\n3. Testando obtenção de token:")
    try:
        token = ds4.get_access_token()
        if token:
            print("✅ Token obtido com sucesso")
        else:
            print("❌ Falha ao obter token")
    except Exception as e:
        print(f"❌ Erro ao obter token: {e}")
    
    print("\n📋 Próximos passos:")
    print("1. Configure as variáveis de ambiente DS4")
    print("2. Acesse http://127.0.0.1:5000/listar_contratos")
    print("3. Clique em '✍️ Enviar para Assinatura' em um contrato")
    print("4. Verifique o status da assinatura")
    
    print("\n🔧 Para configurar as variáveis DS4:")
    print("   $env:DS4_ACCOUNT_ID='sua_account_id'")
    print("   $env:DS4_INTEGRATION_KEY='sua_integration_key'")
    print("   $env:DS4_USER_ID='seu_user_id'")
    print("   $env:DS4_PRIVATE_KEY_PATH='caminho/para/private_key.pem'")

if __name__ == "__main__":
    testar_ds4() 