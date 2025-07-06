import sqlite3

def remover_tabela_temporaria():
    try:
        # Conectar ao banco de dados
        conn = sqlite3.connect('adm_aluguel.db')
        cur = conn.cursor()
        
        # Verificar se a tabela existe
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='_alembic_tmp_inquilino';")
        tabela_existe = cur.fetchone()
        
        if tabela_existe:
            # Remover a tabela temporária
            cur.execute("DROP TABLE _alembic_tmp_inquilino;")
            conn.commit()
            print("✅ Tabela temporária _alembic_tmp_inquilino removida com sucesso!")
        else:
            print("ℹ️ Tabela temporária _alembic_tmp_inquilino não existe.")
        
        # Fechar conexão
        conn.close()
        
    except Exception as e:
        print(f"❌ Erro ao remover tabela temporária: {e}")

if __name__ == "__main__":
    print("🔧 Removendo tabela temporária do banco de dados...")
    remover_tabela_temporaria()
    print("✅ Processo concluído!") 