import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging():
    """Configura logs para arquivo separado"""
    
    # Criar pasta de logs se não existir
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Configurar logger
    logger = logging.getLogger('adm_aluguel')
    logger.setLevel(logging.INFO)
    
    # Handler para arquivo
    file_handler = RotatingFileHandler(
        'logs/app.log', 
        maxBytes=1024*1024,  # 1MB
        backupCount=5
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    logger.addHandler(file_handler)
    
    return logger 