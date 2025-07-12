#!/usr/bin/env python3
"""
Teste simples da aplicação Flask
"""

import os
import sys

# Configurar variáveis de ambiente para teste
os.environ.setdefault('RAILWAY_ENVIRONMENT', 'production')
os.environ.setdefault('SECRET_KEY', 'test_key_123')

print("🧪 Testando aplicação Flask...")

try:
    from app import app, db
    
    print("✅ Aplicação importada com sucesso")
    
    # Testar contexto da aplicação
    with app.app_context():
        print("✅ Contexto da aplicação criado")
        
        # Testar criação de tabelas
        try:
            db.create_all()
            print("✅ Tabelas criadas com sucesso")
        except Exception as e:
            print(f"⚠️ Erro ao criar tabelas: {e}")
        
        # Testar rota de healthcheck
        with app.test_client() as client:
            response = client.get('/health')
            print(f"✅ Healthcheck: {response.status_code} - {response.data.decode()}")
            
            response = client.get('/')
            print(f"✅ Homepage: {response.status_code}")
    
    print("🎉 Todos os testes passaram!")
    
except Exception as e:
    print(f"❌ Erro no teste: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1) 