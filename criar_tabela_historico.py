#!/usr/bin/env python3
"""
Script para criar apenas a tabela de histórico sem afetar dados existentes
"""

from app import app, db
from app.models import HistoricoAlteracao

def criar_tabela_historico():
    """Cria apenas a tabela de histórico se ela não existir"""
    with app.app_context():
        try:
            # Verificar se a tabela já existe
            with db.engine.connect() as conn:
                result = conn.execute(db.text("SELECT name FROM sqlite_master WHERE type='table' AND name='historico_alteracao'"))
                if result.fetchone():
                    print("✅ Tabela historico_alteracao já existe!")
                    return True
                
                # Criar a tabela manualmente
                print("📝 Criando tabela historico_alteracao...")
                
                # SQL para criar a tabela conforme o modelo
                create_table_sql = """
                CREATE TABLE historico_alteracao (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tabela VARCHAR(50) NOT NULL,
                    registro_id INTEGER NOT NULL,
                    tipo_alteracao VARCHAR(20) NOT NULL,
                    campo_alterado VARCHAR(50),
                    valor_anterior TEXT,
                    valor_novo TEXT,
                    data_alteracao DATETIME NOT NULL,
                    usuario VARCHAR(100),
                    observacao TEXT
                );
                """
                
                conn.execute(db.text(create_table_sql))
                conn.commit()
                print("✅ Tabela historico_alteracao criada com sucesso!")
                return True
                
        except Exception as e:
            print(f"❌ Erro ao criar tabela: {e}")
            return False

def verificar_dados():
    """Verifica se os dados ainda estão intactos"""
    with app.app_context():
        try:
            from app.models import Contrato, Inquilino, Local, Boleto
            
            print("\n📊 Verificando dados existentes:")
            print(f"   Contratos: {Contrato.query.count()}")
            print(f"   Inquilinos: {Inquilino.query.count()}")
            print(f"   Locais: {Local.query.count()}")
            print(f"   Boletos: {Boleto.query.count()}")
            
            return True
        except Exception as e:
            print(f"❌ Erro ao verificar dados: {e}")
            return False

def main():
    """Função principal"""
    print("🔧 CRIANDO TABELA DE HISTÓRICO")
    print("=" * 40)
    
    # Criar tabela de histórico
    if criar_tabela_historico():
        # Verificar dados
        if verificar_dados():
            print("\n✅ SUCESSO! Tabela criada e dados preservados!")
            print("\n📋 Próximos passos:")
            print("1. Teste o sistema: python testar_melhorias_completas.py")
            print("2. Acesse: http://127.0.0.1:5000")
        else:
            print("\n❌ Dados foram perdidos! Restaure o backup.")
    else:
        print("\n❌ Falha ao criar tabela.")

if __name__ == "__main__":
    main() 