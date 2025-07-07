#!/usr/bin/env python3
"""
Script para atualizar o status das unidades existentes
"""

from app import app, db
from app.models import Unidade, Inquilino, Contrato

def atualizar_status_unidades():
    """Atualiza o status das unidades baseado nos dados existentes"""
    
    with app.app_context():
        # Buscar todas as unidades
        unidades = Unidade.query.all()
        
        for unidade in unidades:
            print(f"Processando unidade: {unidade.nome} (ID: {unidade.id})")
            
            # Verificar se tem inquilino ativo
            inquilino_ativo = Inquilino.query.filter_by(unidade_id=unidade.id).first()
            
            # Verificar se tem contrato ativo
            contrato_ativo = Contrato.query.filter_by(
                unidade_id=unidade.id, 
                situacao='ativo'
            ).first()
            
            # Determinar o novo status
            if contrato_ativo:
                novo_status = 'ocupada'
                print(f"  -> Contrato ativo encontrado: marcando como OCUPADA")
            elif inquilino_ativo:
                novo_status = 'ocupada'
                print(f"  -> Inquilino ativo encontrado: marcando como OCUPADA")
            else:
                novo_status = 'disponivel'
                print(f"  -> Nenhum contrato/inquilino ativo: marcando como DISPONÍVEL")
            
            # Atualizar status
            unidade.status = novo_status
            print(f"  -> Status atualizado: {unidade.status}")
        
        # Commit das mudanças
        db.session.commit()
        print("\n✅ Atualização concluída!")
        
        # Mostrar estatísticas finais
        total = Unidade.query.count()
        disponiveis = Unidade.query.filter_by(status='disponivel').count()
        ocupadas = Unidade.query.filter_by(status='ocupada').count()
        manutencao = Unidade.query.filter_by(status='manutencao').count()
        
        print(f"\n📊 Estatísticas finais:")
        print(f"   Total: {total}")
        print(f"   Disponíveis: {disponiveis}")
        print(f"   Ocupadas: {ocupadas}")
        print(f"   Manutenção: {manutencao}")

if __name__ == '__main__':
    atualizar_status_unidades() 