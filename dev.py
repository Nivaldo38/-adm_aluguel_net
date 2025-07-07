#!/usr/bin/env python3
"""
Script de desenvolvimento com logs controlados
"""

import os
import sys
from app import app

if __name__ == '__main__':
    print("🔧 Modo Desenvolvimento")
    print("📍 URL: http://127.0.0.1:5000")
    print("📝 Logs de erro serão mostrados")
    print("⏹️  Pressione Ctrl+C para parar")
    print("-" * 50)
    
    # Rodar com logs de erro apenas
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=False,  # Sem debug para menos logs
        use_reloader=False
    ) 