"""
Agendador de Notificações Automáticas
"""

import schedule
import time
import threading
from datetime import datetime
from app.notification_service import notification_service

def run_notification_checks():
    """Executa verificações de notificações"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🔔 Executando verificações automáticas de notificações...")
    
    try:
        notification_service.run_daily_checks()
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✅ Verificações concluídas com sucesso!")
    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ❌ Erro ao executar verificações: {e}")

def start_scheduler():
    """Inicia o agendador de tarefas"""
    print("🚀 Iniciando agendador de notificações...")
    
    # Agendar verificações diárias às 8:00
    schedule.every().day.at("08:00").do(run_notification_checks)
    
    # Agendar verificações semanais aos domingos às 9:00
    schedule.every().sunday.at("09:00").do(run_notification_checks)
    
    # Agendar verificações mensais no primeiro dia do mês às 10:00
    schedule.every().day.at("10:00").do(run_notification_checks)
    
    print("📅 Agendamentos configurados:")
    print("   - Diário: 08:00")
    print("   - Semanal: Domingo às 09:00")
    print("   - Mensal: Primeiro dia do mês às 10:00")
    
    # Loop principal do agendador
    while True:
        schedule.run_pending()
        time.sleep(60)  # Verificar a cada minuto

def run_scheduler_in_background():
    """Executa o agendador em background"""
    scheduler_thread = threading.Thread(target=start_scheduler, daemon=True)
    scheduler_thread.start()
    print("✅ Agendador iniciado em background")

if __name__ == "__main__":
    # Para testar o agendador
    print("🧪 Modo de teste - executando verificações imediatamente...")
    run_notification_checks()
    
    print("\n🔄 Iniciando agendador...")
    start_scheduler() 