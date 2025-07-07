#!/usr/bin/env python3
"""
Script limpo para rodar o servidor Flask
Sem poluir o terminal com logs desnecessários
"""

import os
import sys
from app import app

if __name__ == '__main__':
    # Configurar para modo produção (menos logs)
    os.environ['FLASK_ENV'] = 'production'
    
    print("🚀 Iniciando servidor de administração de aluguel...")
    print("📍 URL: http://127.0.0.1:5000")
    print("⏹️  Pressione Ctrl+C para parar")
    print("-" * 50)
    
    # Rodar servidor com logs mínimos
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
        use_reloader=False  # Evita logs de reload
    ) 