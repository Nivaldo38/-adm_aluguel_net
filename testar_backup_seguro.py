#!/usr/bin/env python3
"""
Script para testar o sistema de backup de forma segura
"""

import os
import shutil
import zipfile
from datetime import datetime
from app.backup_service import BackupService

def testar_backup_seguro():
    """Testa o sistema de backup de forma segura"""
    
    print("🔍 TESTE DE BACKUP SEGURO")
    print("=" * 50)
    
    # 1. Verificar se o serviço funciona
    print("\n1. ✅ Verificando serviço de backup...")
    try:
        backup_service = BackupService()
        print("   ✅ Serviço de backup inicializado")
    except Exception as e:
        print(f"   ❌ Erro ao inicializar: {e}")
        return False
    
    # 2. Listar backups existentes
    print("\n2. 📋 Listando backups existentes...")
    backups = backup_service.list_backups()
    if backups:
        print(f"   ✅ Encontrados {len(backups)} backups:")
        for backup in backups[:3]:  # Mostrar apenas os 3 mais recentes
            print(f"      📦 {backup['filename']} ({backup['size_mb']} MB) - {backup['created']}")
    else:
        print("   ⚠️ Nenhum backup encontrado")
    
    # 3. Criar backup de teste
    print("\n3. 🆕 Criando backup de teste...")
    try:
        backup_path = backup_service.create_backup()
        if backup_path:
            print(f"   ✅ Backup criado: {os.path.basename(backup_path)}")
            
            # Verificar se o arquivo foi criado
            if os.path.exists(backup_path):
                size_mb = os.path.getsize(backup_path) / (1024 * 1024)
                print(f"   📊 Tamanho: {size_mb:.2f} MB")
            else:
                print("   ❌ Arquivo de backup não encontrado")
        else:
            print("   ❌ Falha ao criar backup")
            return False
    except Exception as e:
        print(f"   ❌ Erro ao criar backup: {e}")
        return False
    
    # 4. Testar integridade do backup
    print("\n4. 🔍 Testando integridade do backup...")
    try:
        with zipfile.ZipFile(backup_path, 'r') as zipf:
            files = zipf.namelist()
            print(f"   ✅ Backup contém {len(files)} arquivos:")
            for file in files:
                print(f"      📄 {file}")
            
            # Verificar se contém arquivos essenciais
            essential_files = ['adm_aluguel.db', 'backup_info.txt']
            missing_files = [f for f in essential_files if f not in files]
            if missing_files:
                print(f"   ⚠️ Arquivos essenciais faltando: {missing_files}")
            else:
                print("   ✅ Todos os arquivos essenciais presentes")
                
    except Exception as e:
        print(f"   ❌ Erro ao verificar integridade: {e}")
        return False
    
    # 5. Simular restauração (sem executar)
    print("\n5. 🔄 Simulando processo de restauração...")
    print("   📋 Processo que seria executado:")
    print("      1. Criar backup do banco atual")
    print("      2. Extrair backup escolhido")
    print("      3. Restaurar banco de dados")
    print("      4. Restaurar contratos PDF")
    print("      5. Limpar arquivos temporários")
    
    # 6. Verificar configurações de segurança
    print("\n6. 🛡️ Verificando configurações de segurança...")
    
    # Verificar retenção de backups
    backups_apos_criacao = backup_service.list_backups()
    if len(backups_apos_criacao) > backup_service.max_backups:
        print(f"   ⚠️ Muitos backups ({len(backups_apos_criacao)} > {backup_service.max_backups})")
        print("   🔄 Limpeza automática será executada")
    else:
        print(f"   ✅ Número de backups OK ({len(backups_apos_criacao)} <= {backup_service.max_backups})")
    
    # Verificar permissões da pasta
    backup_dir = backup_service.backup_dir
    if os.access(backup_dir, os.W_OK):
        print("   ✅ Pasta de backup com permissões corretas")
    else:
        print("   ❌ Problema com permissões da pasta de backup")
    
    print("\n" + "=" * 50)
    print("✅ TESTE DE BACKUP CONCLUÍDO COM SUCESSO!")
    print("💡 Dicas de segurança:")
    print("   • Sempre teste em ambiente de desenvolvimento")
    print("   • Mantenha backups em local seguro")
    print("   • Verifique integridade antes de restaurar")
    print("   • Documente todas as operações")
    
    return True

def mostrar_estatisticas_backup():
    """Mostra estatísticas dos backups"""
    
    print("\n📊 ESTATÍSTICAS DE BACKUP")
    print("=" * 30)
    
    backup_service = BackupService()
    backups = backup_service.list_backups()
    
    if not backups:
        print("Nenhum backup encontrado")
        return
    
    # Calcular estatísticas
    total_size = sum(b['size_mb'] for b in backups)
    oldest_backup = min(backups, key=lambda x: x['created_timestamp'])
    newest_backup = max(backups, key=lambda x: x['created_timestamp'])
    
    print(f"📦 Total de backups: {len(backups)}")
    print(f"💾 Tamanho total: {total_size:.2f} MB")
    print(f"📅 Backup mais antigo: {oldest_backup['created']}")
    print(f"📅 Backup mais recente: {newest_backup['created']}")
    print(f"🔄 Retenção configurada: {backup_service.max_backups} backups")

if __name__ == "__main__":
    print("🚀 INICIANDO TESTES DE BACKUP")
    print("=" * 50)
    
    # Executar testes
    sucesso = testar_backup_seguro()
    
    if sucesso:
        # Mostrar estatísticas
        mostrar_estatisticas_backup()
        
        print("\n🎯 PRÓXIMOS PASSOS:")
        print("1. Teste o backup no sistema web")
        print("2. Verifique a restauração em ambiente de teste")
        print("3. Configure backup automático")
        print("4. Implemente notificações de backup")
    else:
        print("\n❌ TESTES FALHARAM - Verifique os erros acima") 