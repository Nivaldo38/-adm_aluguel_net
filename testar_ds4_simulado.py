#!/usr/bin/env python3
"""
Script para testar DS4 Simulado
"""

import os
import sys
from app import app, db
from app.models import Contrato
from app.ds4_simulado import DS4Simulado

def testar_ds4_simulado():
    """Testa a funcionalidade DS4 simulado"""
    print("🔧 Testando DS4 Simulado...")
    
    # Criar instância simulada
    ds4 = DS4Simulado()
    
    # Testar token
    print("\n1. Testando obtenção de token:")
    token = ds4.get_access_token()
    print(f"✅ Token simulado: {token}")
    
    # Buscar contrato para teste
    with app.app_context():
        contrato = Contrato.query.first()
        if not contrato:
            print("❌ Nenhum contrato encontrado para teste")
            return
        
        print(f"\n2. Testando com contrato ID: {contrato.id}")
        print(f"   Inquilino: {contrato.inquilino.nome}")
        print(f"   Status atual: {contrato.status_assinatura or 'Não enviado'}")
        
        # Simular envio para assinatura
        print("\n3. Simulando envio para assinatura:")
        pdf_path = contrato.arquivo_contrato or "contracts/teste.pdf"
        
        result = ds4.send_contract_for_signature(contrato, pdf_path)
        print(f"   Resultado: {result}")
        
        if result['success']:
            envelope_id = result['envelope_id']
            print(f"   Envelope ID: {envelope_id}")
            
            # Simular verificação de status
            print("\n4. Simulando verificação de status:")
            for i in range(3):
                status = ds4.get_envelope_status(envelope_id)
                print(f"   Verificação {i+1}: {status}")
                
                if status == 'completed':
                    print("   ✅ Contrato assinado!")
                    break
                
                import time
                time.sleep(2)  # Simular tempo de espera
    
    print("\n🎯 Para testar no navegador:")
    print("1. Acesse: http://127.0.0.1:5000/listar_contratos")
    print("2. Clique em '✍️ Enviar para Assinatura'")
    print("3. Aguarde alguns segundos e clique em '📊 Verificar Status'")
    print("4. O contrato será marcado como assinado automaticamente")

if __name__ == "__main__":
    testar_ds4_simulado() 