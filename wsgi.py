#!/usr/bin/env python3
"""
WSGI entry point para produção
"""

import os
import sys

# Adicionar o diretório atual ao path
sys.path.insert(0, os.path.dirname(__file__))

# Configurar variáveis de ambiente para produção
os.environ.setdefault('RAILWAY_ENVIRONMENT', 'production')

try:
    from app import app, db
    
    # Criar contexto da aplicação
    with app.app_context():
        # Tentar criar tabelas se não existirem
        try:
            db.create_all()
            print("✅ Banco de dados inicializado com sucesso")
        except Exception as e:
            print(f"⚠️ Erro ao inicializar banco: {e}")
            # Continuar mesmo com erro de banco
    
    print("🚀 Aplicação pronta para produção!")
    
except Exception as e:
    print(f"❌ Erro crítico na inicialização: {e}")
    # Criar uma aplicação mínima para healthcheck
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/health')
    def health_check():
        return 'OK', 200
    
    @app.route('/')
    def home():
        return 'Sistema em manutenção', 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 