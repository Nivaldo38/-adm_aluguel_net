"""
Serviço de Backup Automático
"""

import os
import shutil
import sqlite3
import zipfile
from datetime import datetime, timedelta
import schedule
import time
import threading
from app import app

class BackupService:
    def __init__(self):
        self.backup_dir = os.path.join(os.getcwd(), 'backups')
        self.db_path = os.path.join(os.getcwd(), 'adm_aluguel.db')
        self.contracts_dir = os.path.join(os.getcwd(), 'app', 'contracts')
        self.max_backups = 30  # Manter apenas 30 backups
        
        # Criar diretório de backup se não existir
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
    
    def create_backup(self):
        """Cria backup completo do sistema"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_name = f'backup_{timestamp}'
            backup_path = os.path.join(self.backup_dir, backup_name)
            
            # Criar diretório do backup
            os.makedirs(backup_path)
            
            # 1. Backup do banco de dados
            if os.path.exists(self.db_path):
                db_backup_path = os.path.join(backup_path, 'adm_aluguel.db')
                shutil.copy2(self.db_path, db_backup_path)
                print(f"✅ Backup do banco criado: {db_backup_path}")
            
            # 2. Backup dos contratos PDF
            if os.path.exists(self.contracts_dir):
                contracts_backup_path = os.path.join(backup_path, 'contracts')
                shutil.copytree(self.contracts_dir, contracts_backup_path)
                print(f"✅ Backup dos contratos criado: {contracts_backup_path}")
            
            # 3. Criar arquivo de informações do backup
            info_content = f"""
Backup criado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
Versão do sistema: 1.0
Arquivos incluídos:
- Banco de dados SQLite
- Contratos PDF
- Configurações

Tamanho total: {self.get_dir_size(backup_path):.2f} MB
            """
            
            with open(os.path.join(backup_path, 'backup_info.txt'), 'w', encoding='utf-8') as f:
                f.write(info_content)
            
            # 4. Criar arquivo ZIP do backup
            zip_path = f"{backup_path}.zip"
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(backup_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, backup_path)
                        zipf.write(file_path, arcname)
            
            # 5. Remover diretório temporário
            shutil.rmtree(backup_path)
            
            # 6. Limpar backups antigos
            self.cleanup_old_backups()
            
            print(f"✅ Backup completo criado: {zip_path}")
            return zip_path
            
        except Exception as e:
            print(f"❌ Erro ao criar backup: {e}")
            return None
    
    def restore_backup(self, backup_path):
        """Restaura backup"""
        try:
            if not os.path.exists(backup_path):
                print(f"❌ Arquivo de backup não encontrado: {backup_path}")
                return False
            
            # Criar diretório temporário para extrair
            temp_dir = os.path.join(self.backup_dir, 'temp_restore')
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            os.makedirs(temp_dir)
            
            # Extrair backup
            with zipfile.ZipFile(backup_path, 'r') as zipf:
                zipf.extractall(temp_dir)
            
            # Restaurar banco de dados
            db_backup = os.path.join(temp_dir, 'adm_aluguel.db')
            if os.path.exists(db_backup):
                # Fazer backup do banco atual antes de restaurar
                current_backup = f"{self.db_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                shutil.copy2(self.db_path, current_backup)
                
                # Restaurar
                shutil.copy2(db_backup, self.db_path)
                print(f"✅ Banco de dados restaurado")
            
            # Restaurar contratos
            contracts_backup = os.path.join(temp_dir, 'contracts')
            if os.path.exists(contracts_backup):
                if os.path.exists(self.contracts_dir):
                    shutil.rmtree(self.contracts_dir)
                shutil.copytree(contracts_backup, self.contracts_dir)
                print(f"✅ Contratos restaurados")
            
            # Limpar diretório temporário
            shutil.rmtree(temp_dir)
            
            print(f"✅ Backup restaurado com sucesso: {backup_path}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao restaurar backup: {e}")
            return False
    
    def cleanup_old_backups(self):
        """Remove backups antigos mantendo apenas os mais recentes"""
        try:
            backup_files = []
            for file in os.listdir(self.backup_dir):
                if file.startswith('backup_') and file.endswith('.zip'):
                    file_path = os.path.join(self.backup_dir, file)
                    backup_files.append((file_path, os.path.getctime(file_path)))
            
            # Ordenar por data de criação (mais recente primeiro)
            backup_files.sort(key=lambda x: x[1], reverse=True)
            
            # Remover backups antigos
            if len(backup_files) > self.max_backups:
                for file_path, _ in backup_files[self.max_backups:]:
                    os.remove(file_path)
                    print(f"🗑️ Backup removido: {os.path.basename(file_path)}")
            
        except Exception as e:
            print(f"❌ Erro ao limpar backups antigos: {e}")
    
    def get_dir_size(self, path):
        """Calcula tamanho do diretório em MB"""
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                total_size += os.path.getsize(filepath)
        return total_size / (1024 * 1024)  # Converter para MB
    
    def list_backups(self):
        """Lista todos os backups disponíveis"""
        backups = []
        try:
            for file in os.listdir(self.backup_dir):
                if file.startswith('backup_') and file.endswith('.zip'):
                    file_path = os.path.join(self.backup_dir, file)
                    size = os.path.getsize(file_path) / (1024 * 1024)  # MB
                    created = datetime.fromtimestamp(os.path.getctime(file_path))
                    backups.append({
                        'filename': file,
                        'path': file_path,
                        'size_mb': round(size, 2),
                        'created': created.strftime('%d/%m/%Y %H:%M:%S'),
                        'created_timestamp': created
                    })
            
            # Ordenar por data de criação (mais recente primeiro)
            backups.sort(key=lambda x: x['created_timestamp'], reverse=True)
            return backups
            
        except Exception as e:
            print(f"❌ Erro ao listar backups: {e}")
            return []
    
    def schedule_daily_backup(self):
        """Agenda backup diário"""
        schedule.every().day.at("02:00").do(self.create_backup)
        print("📅 Backup diário agendado para 02:00")
    
    def start_backup_scheduler(self):
        """Inicia o agendador de backups em thread separada"""
        def run_scheduler():
            self.schedule_daily_backup()
            while True:
                schedule.run_pending()
                time.sleep(60)  # Verificar a cada minuto
        
        scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        scheduler_thread.start()
        print("🔄 Agendador de backups iniciado")

# Instância global
backup_service = BackupService() 