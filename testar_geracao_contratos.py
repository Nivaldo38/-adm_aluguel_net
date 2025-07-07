#!/usr/bin/env python3
"""
Script para testar a geração automática de contratos
"""

import os
import sys
from datetime import datetime

# Adicionar o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from app.models import Contrato, Inquilino, Unidade, Local

def testar_geracao_contratos():
    """Testa a geração automática de contratos"""
    
    with app.app_context():
        print("🧪 Testando geração automática de contratos...")
        
        # Verificar se existem contratos
        contratos = Contrato.query.all()
        print(f"📋 Total de contratos no banco: {len(contratos)}")
        
        if not contratos:
            print("❌ Nenhum contrato encontrado. Crie um contrato primeiro.")
            return
        
        # Testar geração para cada contrato
        for contrato in contratos:
            print(f"\n📄 Testando contrato ID: {contrato.id}")
            print(f"   Inquilino: {contrato.inquilino.nome}")
            print(f"   Unidade: {contrato.unidade.nome}")
            print(f"   Valor: R$ {contrato.valor_aluguel:.2f}")
            
            # Verificar se já tem arquivo
            if contrato.arquivo_contrato:
                print(f"   ✅ Já possui arquivo: {contrato.arquivo_contrato}")
                
                # Verificar se arquivo existe
                if os.path.exists(contrato.arquivo_contrato):
                    print(f"   ✅ Arquivo existe no sistema")
                else:
                    print(f"   ❌ Arquivo não encontrado no sistema")
            else:
                print(f"   ❌ Não possui arquivo gerado")
            
            # Testar regeneração
            try:
                from app.contract_generator import ContractGenerator
                generator = ContractGenerator()
                
                # Gerar novo PDF
                contract_path = generator.generate_contract_pdf(contrato)
                
                # Atualizar no banco
                contrato.arquivo_contrato = contract_path
                db.session.commit()
                
                print(f"   ✅ Contrato regenerado: {contract_path}")
                
            except Exception as e:
                print(f"   ❌ Erro ao regenerar: {str(e)}")
        
        print("\n🎯 Teste concluído!")

if __name__ == '__main__':
    testar_geracao_contratos() 