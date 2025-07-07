"""
Serviço de Backup Automático com Melhorias de Segurança
"""

import os
import shutil
import sqlite3
import zipfile
import hashlib
import json
from datetime import datetime, timedelta
# schedule removido para simplificação
# time removido
# threading removido
from app import app

class BackupService:
    def __init__(self):
        self.backup_dir = os.path.join(os.getcwd(), 'backups')
        self.db_path = os.path.join(os.getcwd(), 'adm_aluguel.db')
        self.contracts_dir = os.path.join(os.getcwd(), 'app', 'contracts')
        self.max_backups = 30  # Manter apenas 30 backups
        self.backup_log_file = os.path.join(self.backup_dir, 'backup_log.json')
        
        # Criar diretório de backup se não existir
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
    
    def create_backup(self):
        """Cria backup completo do sistema com verificações de segurança"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_name = f'backup_{timestamp}'
            backup_path = os.path.join(self.backup_dir, backup_name)
            
            # Verificar espaço em disco antes de criar backup
            if not self._check_disk_space():
                print("❌ Espaço insuficiente em disco para criar backup")
                return None
            
            # Criar diretório do backup
            os.makedirs(backup_path)
            
            # 1. Backup do banco de dados com verificação de integridade
            if os.path.exists(self.db_path):
                db_backup_path = os.path.join(backup_path, 'adm_aluguel.db')
                shutil.copy2(self.db_path, db_backup_path)
                
                # Verificar integridade do banco
                if not self._verify_database_integrity(db_backup_path):
                    print("❌ Banco de dados corrompido - backup cancelado")
                    shutil.rmtree(backup_path)
                    return None
                
                print(f"✅ Backup do banco criado: {db_backup_path}")
            else:
                print("❌ Banco de dados não encontrado")
                return None
            
            # 2. Backup dos contratos PDF
            if os.path.exists(self.contracts_dir):
                contracts_backup_path = os.path.join(backup_path, 'contracts')
                shutil.copytree(self.contracts_dir, contracts_backup_path)
                print(f"✅ Backup dos contratos criado: {contracts_backup_path}")
            
            # 3. Criar arquivo de informações do backup com hash de segurança
            backup_info = self._create_backup_info(backup_path)
            
            # 4. Criar arquivo ZIP do backup com verificação
            zip_path = f"{backup_path}.zip"
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(backup_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, backup_path)
                        zipf.write(file_path, arcname)
            
            # 5. Verificar integridade do ZIP
            if not self._verify_zip_integrity(zip_path):
                print("❌ Erro na criação do ZIP - backup cancelado")
                os.remove(zip_path)
                shutil.rmtree(backup_path)
                return None
            
            # 6. Remover diretório temporário
            shutil.rmtree(backup_path)
            
            # 7. Registrar backup no log
            self._log_backup_operation('create', zip_path, backup_info)
            
            # 8. Limpar backups antigos
            self.cleanup_old_backups()
            
            print(f"✅ Backup completo criado: {zip_path}")
            return zip_path
            
        except Exception as e:
            print(f"❌ Erro ao criar backup: {e}")
            # Limpar arquivos parciais em caso de erro
            if os.path.exists(backup_path):
                shutil.rmtree(backup_path)
            return None
    
    def restore_backup(self, backup_path):
        """Restaura backup com verificações de segurança"""
        try:
            if not os.path.exists(backup_path):
                print(f"❌ Arquivo de backup não encontrado: {backup_path}")
                return False
            
            # Verificar integridade do backup antes de restaurar
            if not self._verify_zip_integrity(backup_path):
                print("❌ Backup corrompido - restauração cancelada")
                return False
            
            # Criar backup de segurança antes de restaurar
            safety_backup = self._create_safety_backup()
            if not safety_backup:
                print("❌ Não foi possível criar backup de segurança - restauração cancelada")
                return False
            
            # Criar diretório temporário para extrair
            temp_dir = os.path.join(self.backup_dir, 'temp_restore')
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            os.makedirs(temp_dir)
            
            # Extrair backup
            with zipfile.ZipFile(backup_path, 'r') as zipf:
                zipf.extractall(temp_dir)
            
            # Verificar arquivos essenciais
            if not self._verify_restore_files(temp_dir):
                print("❌ Arquivos essenciais não encontrados no backup")
                shutil.rmtree(temp_dir)
                return False
            
            # Restaurar banco de dados
            db_backup = os.path.join(temp_dir, 'adm_aluguel.db')
            if os.path.exists(db_backup):
                # Verificar integridade do banco antes de restaurar
                if not self._verify_database_integrity(db_backup):
                    print("❌ Banco de dados no backup está corrompido")
                    shutil.rmtree(temp_dir)
                    return False
                
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
            
            # Registrar restauração no log
            self._log_backup_operation('restore', backup_path, {
                'safety_backup': safety_backup,
                'timestamp': datetime.now().isoformat()
            })
            
            print(f"✅ Backup restaurado com sucesso: {backup_path}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao restaurar backup: {e}")
            return False
    
    def _check_disk_space(self):
        """Verifica se há espaço suficiente em disco"""
        try:
            statvfs = os.statvfs(self.backup_dir)
            free_space = statvfs.f_frsize * statvfs.f_bavail
            required_space = 100 * 1024 * 1024  # 100 MB mínimo
            return free_space > required_space
        except:
            return True  # Se não conseguir verificar, assume que há espaço
    
    def _verify_database_integrity(self, db_path):
        """Verifica integridade do banco de dados"""
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Verificar se as tabelas principais existem
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            required_tables = ['local', 'unidade', 'inquilino', 'contrato', 'boleto']
            missing_tables = [table for table in required_tables if table not in tables]
            
            if missing_tables:
                print(f"❌ Tabelas faltando: {missing_tables}")
                return False
            
            # Verificar se há dados nas tabelas principais
            for table in required_tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                if count == 0:
                    print(f"⚠️ Tabela {table} está vazia")
            
            conn.close()
            return True
            
        except Exception as e:
            print(f"❌ Erro ao verificar integridade do banco: {e}")
            return False
    
    def _verify_zip_integrity(self, zip_path):
        """Verifica integridade do arquivo ZIP"""
        try:
            with zipfile.ZipFile(zip_path, 'r') as zipf:
                # Testar se o ZIP pode ser aberto
                zipf.testzip()
                return True
        except Exception as e:
            print(f"❌ ZIP corrompido: {e}")
            return False
    
    def _verify_restore_files(self, temp_dir):
        """Verifica se os arquivos essenciais estão presentes"""
        essential_files = ['adm_aluguel.db', 'backup_info.txt']
        for file in essential_files:
            if not os.path.exists(os.path.join(temp_dir, file)):
                print(f"❌ Arquivo essencial não encontrado: {file}")
                return False
        return True
    
    def _create_safety_backup(self):
        """Cria backup de segurança antes de restaurar"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            safety_backup = f"{self.db_path}.safety_{timestamp}"
            shutil.copy2(self.db_path, safety_backup)
            print(f"✅ Backup de segurança criado: {os.path.basename(safety_backup)}")
            return safety_backup
        except Exception as e:
            print(f"❌ Erro ao criar backup de segurança: {e}")
            return None
    
    def _create_backup_info(self, backup_path):
        """Cria informações detalhadas do backup"""
        info_content = f"""
Backup criado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
Versão do sistema: 1.0
Arquivos incluídos:
- Banco de dados SQLite
- Contratos PDF
- Configurações

Tamanho total: {self.get_dir_size(backup_path):.2f} MB
Hash de segurança: {self._calculate_backup_hash(backup_path)}
        """
        
        info_file = os.path.join(backup_path, 'backup_info.txt')
        with open(info_file, 'w', encoding='utf-8') as f:
            f.write(info_content)
        
        return {
            'timestamp': datetime.now().isoformat(),
            'size_mb': self.get_dir_size(backup_path),
            'hash': self._calculate_backup_hash(backup_path)
        }
    
    def _calculate_backup_hash(self, backup_path):
        """Calcula hash SHA256 do backup"""
        try:
            sha256_hash = hashlib.sha256()
            for root, dirs, files in os.walk(backup_path):
                for file in sorted(files):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'rb') as f:
                        for chunk in iter(lambda: f.read(4096), b""):
                            sha256_hash.update(chunk)
            return sha256_hash.hexdigest()
        except:
            return "hash_error"
    
    def _log_backup_operation(self, operation, file_path, info):
        """Registra operações de backup no log"""
        try:
            log_entry = {
                'operation': operation,
                'file': os.path.basename(file_path),
                'timestamp': datetime.now().isoformat(),
                'info': info
            }
            
            # Carregar log existente ou criar novo
            if os.path.exists(self.backup_log_file):
                with open(self.backup_log_file, 'r', encoding='utf-8') as f:
                    log = json.load(f)
            else:
                log = []
            
            log.append(log_entry)
            
            # Manter apenas os últimos 100 registros
            if len(log) > 100:
                log = log[-100:]
            
            with open(self.backup_log_file, 'w', encoding='utf-8') as f:
                json.dump(log, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"⚠️ Erro ao registrar log: {e}")
    
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
        """Lista todos os backups disponíveis, usando a data do backup_info.txt"""
        backups = []
        try:
            for file in os.listdir(self.backup_dir):
                if file.startswith('backup_') and file.endswith('.zip'):
                    file_path = os.path.join(self.backup_dir, file)
                    size = os.path.getsize(file_path) / (1024 * 1024)  # MB
                    created = None
                    # Tenta ler a data do backup_info.txt
                    try:
                        with zipfile.ZipFile(file_path, 'r') as zipf:
                            if 'backup_info.txt' in zipf.namelist():
                                with zipf.open('backup_info.txt') as info_file:
                                    for line in info_file:
                                        line = line.decode('utf-8').strip()
                                        if line.startswith('Backup criado em:'):
                                            created = line.replace('Backup criado em:', '').strip()
                                            break
                    except Exception as e:
                        created = None
                    # Se não conseguir, usa data de modificação
                    if not created:
                        created = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%d/%m/%Y %H:%M:%S')
                    backups.append({
                        'filename': file,
                        'path': file_path,
                        'size_mb': round(size, 2),
                        'created': created,
                        'created_timestamp': created
                    })
            # Ordenar por data de criação (mais recente primeiro, se possível)
            def parse_data(d):
                try:
                    return datetime.strptime(d['created'], '%d/%m/%Y %H:%M:%S')
                except:
                    return datetime.now()
            backups.sort(key=parse_data, reverse=True)
            return backups
        except Exception as e:
            print(f"❌ Erro ao listar backups: {e}")
            return []
    
    # def schedule_daily_backup(self):
        """Agenda backup diário"""
        schedule.every().day.at("02:00").do(self.create_backup)
        print("📅 Backup diário agendado para 02:00")
    
    # def start_backup_scheduler(self):
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