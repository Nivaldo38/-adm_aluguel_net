# Configuração do Gunicorn para produção
import os

bind = f"0.0.0.0:{os.environ.get('PORT', '8080')}"
workers = 2
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 50
preload_app = True
reload = False

# Configurações de log para debug
loglevel = "debug"
accesslog = "-"
errorlog = "-"
capture_output = True
enable_stdio_inheritance = True 