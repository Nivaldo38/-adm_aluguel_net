#!/usr/bin/env python3
"""
Script para testar a visualização de contrato assinado
"""

import os
import sys
from app import app, db
from app.models import Contrato
from app.ds4_simulado import DS4Simulado

def testar_contrato_assinado():
    """Testa a funcionalidade de contrato assinado"""
    print("🔍 Testando Visualização de Contrato Assinado...")
    
    with app.app_context():
        # Buscar contrato para teste
        contrato = Contrato.query.first()
        if not contrato:
            print("❌ Nenhum contrato encontrado para teste")
            return
        
        print(f"\n1. Contrato encontrado:")
        print(f"   ID: {contrato.id}")
        print(f"   Inquilino: {contrato.inquilino.nome}")
        print(f"   Status Assinatura: {contrato.status_assinatura or 'Não enviado'}")
        print(f"   Envelope ID: {contrato.envelope_id or 'N/A'}")
        
        # Simular processo de assinatura
        print("\n2. Simulando processo de assinatura:")
        ds4 = DS4Simulado()
        
        # Simular envio para assinatura
        pdf_path = contrato.arquivo_contrato or "contracts/teste.pdf"
        result = ds4.send_contract_for_signature(contrato, pdf_path)
        
        if result['success']:
            envelope_id = result['envelope_id']
            print(f"   ✅ Envelope criado: {envelope_id}")
            
            # Simular assinatura completa
            print("\n3. Simulando assinatura completa:")
            
            # Atualizar contrato no banco
            contrato.envelope_id = envelope_id
            contrato.status_assinatura = 'assinado'
            contrato.arquivo_contrato_assinado = f"contracts/contrato_{contrato.id}_assinado.pdf"
            
            # Simular download do documento assinado
            signed_path = contrato.arquivo_contrato_assinado
            if ds4.download_signed_document(envelope_id, signed_path):
                print(f"   ✅ Documento assinado salvo: {signed_path}")
                
                # Salvar no banco
                db.session.commit()
                print("   ✅ Contrato atualizado no banco de dados")
                
                print(f"\n🎯 Para testar no navegador:")
                print(f"1. Acesse: http://127.0.0.1:5000/listar_contratos")
                print(f"2. Procure o contrato ID: {contrato.id}")
                print(f"3. Clique em '✅ Ver Assinado' para ver a página de visualização")
                print(f"4. Clique em '📄 Baixar PDF' para baixar o arquivo")
                print(f"5. Ou acesse diretamente: http://127.0.0.1:5000/visualizar_contrato_assinado/{contrato.id}")
            else:
                print("   ❌ Erro ao salvar documento assinado")
        else:
            print(f"   ❌ Erro ao criar envelope: {result['message']}")

if __name__ == "__main__":
    testar_contrato_assinado() 