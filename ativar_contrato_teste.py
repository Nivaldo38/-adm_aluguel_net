#!/usr/bin/env python3
"""
Script para ativar um contrato existente para teste de assinatura
"""

from app import app, db
from app.models import Inquilino, Contrato

def ativar_contrato_teste():
    email_teste = "nivaldoteles38@gmail.com"
    
    with app.app_context():
        # Buscar inquilino
        inquilino = Inquilino.query.filter_by(email=email_teste).first()
        if not inquilino:
            print("❌ Inquilino não encontrado!")
            return
        
        print(f"✅ Inquilino: {inquilino.nome}")
        
        # Buscar contratos deste inquilino
        contratos = Contrato.query.filter_by(inquilino_id=inquilino.id).all()
        if not contratos:
            print("❌ Nenhum contrato encontrado para este inquilino!")
            return
        
        print(f"📋 Encontrados {len(contratos)} contratos:")
        for i, contrato in enumerate(contratos):
            print(f"  {i+1}. ID: {contrato.id} - Status: {contrato.situacao} - Valor: R$ {contrato.valor_aluguel}")
        
        # Ativar o primeiro contrato
        contrato_para_ativar = contratos[0]
        contrato_para_ativar.situacao = 'Ativo'
        db.session.commit()
        
        print(f"✅ Contrato ID {contrato_para_ativar.id} ativado com sucesso!")
        print(f"💰 Valor do aluguel: R$ {contrato_para_ativar.valor_aluguel}")
        print(f"📅 Data início: {contrato_para_ativar.data_inicio}")
        
        return contrato_para_ativar

if __name__ == "__main__":
    ativar_contrato_teste() 