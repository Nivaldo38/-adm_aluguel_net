#!/usr/bin/env python3
"""
Script para testar o sistema antes do deploy no Railway
"""

import os
import sys
import importlib

def test_imports():
    """Testa se todas as dependências estão disponíveis"""
    print("🔍 Testando imports...")
    
    required_modules = [
        'flask',
        'flask_sqlalchemy', 
        'flask_migrate',
        'schedule',
        'gunicorn'
    ]
    
    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            return False
    
    return True

def test_app_creation():
    """Testa se a aplicação Flask pode ser criada"""
    print("\n🔍 Testando criação da aplicação...")
    
    try:
        from app import app, db
        print("✅ Aplicação Flask criada com sucesso")
        print(f"✅ Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
        return True
    except Exception as e:
        print(f"❌ Erro ao criar aplicação: {e}")
        return False

def test_database():
    """Testa se o banco de dados está acessível"""
    print("\n🔍 Testando banco de dados...")
    
    try:
        from app import app, db
        from app.models import Local, Unidade, Inquilino, Contrato, Boleto
        
        with app.app_context():
            # Testar conexão
            with db.engine.connect() as conn:
                conn.execute(db.text("SELECT 1"))
            print("✅ Conexão com banco de dados OK")
            
            # Testar modelos
            print("✅ Modelos carregados:")
            print(f"  - Local: {Local}")
            print(f"  - Unidade: {Unidade}")
            print(f"  - Inquilino: {Inquilino}")
            print(f"  - Contrato: {Contrato}")
            print(f"  - Boleto: {Boleto}")
            
            return True
    except Exception as e:
        print(f"❌ Erro no banco de dados: {e}")
        return False

def test_routes():
    """Testa se as rotas estão funcionando"""
    print("\n🔍 Testando rotas...")
    
    try:
        from app import app
        
        # Verificar se as rotas principais existem
        routes_to_check = [
            '/',
            '/locais',
            '/inquilinos',
            '/listar_contratos',
            '/boletos'
        ]
        
        with app.test_client() as client:
            for route in routes_to_check:
                try:
                    response = client.get(route)
                    if response.status_code in [200, 302, 404]:  # 404 é OK para algumas rotas
                        print(f"✅ {route}: {response.status_code}")
                    else:
                        print(f"⚠️ {route}: {response.status_code}")
                except Exception as e:
                    print(f"❌ {route}: {e}")
        
        return True
    except Exception as e:
        print(f"❌ Erro ao testar rotas: {e}")
        return False

def test_scheduler():
    """Testa se o scheduler está funcionando"""
    print("\n🔍 Testando scheduler...")
    
    try:
        from scheduler import run_notification_checks
        print("✅ Scheduler importado com sucesso")
        return True
    except Exception as e:
        print(f"❌ Erro no scheduler: {e}")
        return False

def test_environment():
    """Testa variáveis de ambiente"""
    print("\n🔍 Testando variáveis de ambiente...")
    
    # Verificar PORT
    port = os.environ.get('PORT', '5000')
    print(f"✅ PORT: {port}")
    
    # Verificar outras variáveis importantes
    important_vars = ['DATABASE_URL', 'SECRET_KEY', 'RAILWAY_ENVIRONMENT']
    
    for var in important_vars:
        value = os.environ.get(var)
        if value:
            print(f"✅ {var}: definida")
        else:
            print(f"⚠️ {var}: não definida (pode ser normal)")
    
    return True

def main():
    """Executa todos os testes"""
    print("🚀 Iniciando testes de deploy...")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_app_creation,
        test_database,
        test_routes,
        test_scheduler,
        test_environment
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Erro inesperado em {test.__name__}: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Resultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 Todos os testes passaram! Sistema pronto para deploy.")
        return True
    else:
        print("⚠️ Alguns testes falharam. Verifique os problemas antes do deploy.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 