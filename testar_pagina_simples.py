#!/usr/bin/env python3
"""
Script para testar se o problema é específico da página inicial
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from app.models import Local, Inquilino, Contrato, Unidade

def testar_sistema():
    """Testa se o sistema básico está funcionando"""
    print("🔍 Testando sistema básico...")
    
    try:
        with app.app_context():
            # Testar conexão com banco
            print("✅ Conexão com banco OK")
            
            # Testar modelos
            locais = Local.query.all()
            print(f"✅ Locais: {len(locais)} encontrados")
            
            inquilinos = Inquilino.query.all()
            print(f"✅ Inquilinos: {len(inquilinos)} encontrados")
            
            contratos = Contrato.query.all()
            print(f"✅ Contratos: {len(contratos)} encontrados")
            
            unidades = Unidade.query.all()
            print(f"✅ Unidades: {len(unidades)} encontradas")
            
            # Testar estatísticas
            contratos_ativos = Contrato.query.filter_by(situacao='Ativo').count()
            print(f"✅ Contratos ativos: {contratos_ativos}")
            
            receita_mensal = sum(c.valor_aluguel for c in contratos if c.situacao == 'Ativo')
            print(f"✅ Receita mensal: R$ {receita_mensal:.2f}")
            
            # Testar contratos recentes
            contratos_recentes = Contrato.query.order_by(Contrato.id.desc()).limit(5).all()
            print(f"✅ Contratos recentes: {len(contratos_recentes)} encontrados")
            
            print("\n🎉 Sistema básico funcionando corretamente!")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    testar_sistema() 