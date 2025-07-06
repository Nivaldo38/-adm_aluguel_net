from app import app
from app.backup_service import backup_service

if __name__ == '__main__':
    # Iniciar agendador de backup
    backup_service.start_backup_scheduler()
    
    app.run(debug=True)
