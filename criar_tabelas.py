#!/usr/bin/env python3
"""
Script para criar todas as tabelas do banco de dados
"""

from app import app, db
from app.models import *

def criar_tabelas():
    """Cria todas as tabelas do banco de dados"""
    with app.app_context():
        try:
            print("🔧 Criando tabelas do banco de dados...")
            db.create_all()
            print("✅ Todas as tabelas foram criadas com sucesso!")
            
            # Verificar se as tabelas foram criadas
            print("\n📊 Verificando tabelas criadas:")
            inspector = db.inspect(db.engine)
            tabelas = inspector.get_table_names()
            for tabela in tabelas:
                print(f"   ✅ {tabela}")
                
        except Exception as e:
            print(f"❌ Erro ao criar tabelas: {e}")
            import traceback
            print(f"   Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    criar_tabelas() 