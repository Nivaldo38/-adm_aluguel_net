from app import app
import os
from scheduler import run_scheduler_in_background

# Forçar recarregamento de templates
app.config['TEMPLATES_AUTO_RELOAD'] = True

if __name__ == '__main__':
    # Iniciar agendador de notificações em background
    run_scheduler_in_background()
    
    # Iniciar aplicação Flask
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
