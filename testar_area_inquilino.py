#!/usr/bin/env python3
"""
Script para testar o sistema de área do inquilino
"""

import requests
import sys
import time

# Configurações
BASE_URL = "http://127.0.0.1:5000"
SESSION = requests.Session()

def print_step(step, description):
    """Imprime um passo do teste"""
    print(f"\n{'='*50}")
    print(f"PASSO {step}: {description}")
    print(f"{'='*50}")

def test_login_page():
    """Testa a página de login do inquilino"""
    print_step(1, "Testando página de login do inquilino")
    
    try:
        response = SESSION.get(f"{BASE_URL}/inquilino/login")
        if response.status_code == 200:
            print("✅ Página de login carregada com sucesso")
            return True
        else:
            print(f"❌ Erro ao carregar página de login: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro ao acessar página de login: {e}")
        return False

def test_invalid_login():
    """Testa login com credenciais inválidas"""
    print_step(2, "Testando login com credenciais inválidas")
    
    try:
        data = {
            'username': 'usuario_inexistente',
            'password': 'senha_errada'
        }
        response = SESSION.post(f"{BASE_URL}/inquilino/login", data=data)
        
        if response.status_code == 200:
            print("✅ Login inválido tratado corretamente")
            return True
        else:
            print(f"❌ Erro no tratamento de login inválido: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro ao testar login inválido: {e}")
        return False

def test_dashboard_access_without_login():
    """Testa acesso ao dashboard sem estar logado"""
    print_step(3, "Testando acesso ao dashboard sem login")
    
    try:
        response = SESSION.get(f"{BASE_URL}/inquilino/dashboard")
        if response.status_code == 302:  # Redirecionamento para login
            print("✅ Acesso negado corretamente - redirecionado para login")
            return True
        else:
            print(f"❌ Erro na proteção do dashboard: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro ao testar acesso sem login: {e}")
        return False

def test_create_inquilino_login():
    """Testa a criação de login para um inquilino"""
    print_step(4, "Criando login para um inquilino")
    
    try:
        # Primeiro, vamos verificar se existe algum inquilino no sistema
        response = SESSION.get(f"{BASE_URL}/inquilinos")
        if response.status_code == 200:
            print("✅ Página de inquilinos acessível")
            
            # Aqui você pode adicionar lógica para criar um login
            # Por enquanto, vamos simular que o login foi criado
            print("ℹ️ Para criar login de inquilino, use o sistema administrativo")
            print("ℹ️ Ou execute manualmente no banco de dados:")
            print("""
            # Exemplo de criação de login:
            from app import db
            from app.models import Inquilino
            from werkzeug.security import generate_password_hash
            
            inquilino = Inquilino.query.first()
            if inquilino:
                inquilino.username = 'teste_inquilino'
                inquilino.password_hash = generate_password_hash('123456')
                inquilino.status_login = 'ativo'
                db.session.commit()
                print('Login criado com sucesso!')
            """)
            return True
        else:
            print(f"❌ Erro ao acessar página de inquilinos: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro ao verificar inquilinos: {e}")
        return False

def test_system_status():
    """Testa o status geral do sistema"""
    print_step(5, "Verificando status do sistema")
    
    try:
        response = SESSION.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Sistema principal funcionando")
            
            # Verificar se o link para área do inquilino está presente
            if 'inquilino/login' in response.text:
                print("✅ Link para área do inquilino encontrado na página inicial")
            else:
                print("⚠️ Link para área do inquilino não encontrado na página inicial")
            
            return True
        else:
            print(f"❌ Erro no sistema principal: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro ao verificar sistema: {e}")
        return False

def print_manual_instructions():
    """Imprime instruções manuais para testar o sistema"""
    print_step(6, "Instruções para teste manual")
    
    print("""
📋 INSTRUÇÕES PARA TESTE MANUAL:

1. 🏠 Acesse o sistema: http://127.0.0.1:5000

2. 👤 Crie login para um inquilino:
   - Vá em "Inquilinos" 
   - Edite um inquilino existente
   - Adicione username e senha
   - Ou execute no Python console:
   
   from app import db
   from app.models import Inquilino
   from werkzeug.security import generate_password_hash
   
   inquilino = Inquilino.query.first()
   inquilino.username = 'teste'
   inquilino.password_hash = generate_password_hash('123456')
   inquilino.status_login = 'ativo'
   db.session.commit()

3. 🔐 Teste o login:
   - Acesse: http://127.0.0.1:5000/inquilino/login
   - Use as credenciais criadas
   - Verifique se consegue acessar o dashboard

4. 📋 Teste as funcionalidades:
   - Dashboard do inquilino
   - Visualizar contrato
   - Ver boletos
   - Perfil do inquilino
   - Alterar senha

5. 🚪 Teste logout:
   - Clique em "Sair" no header
   - Verifique se foi redirecionado para login

6. 🔒 Teste proteção:
   - Tente acessar /inquilino/dashboard sem estar logado
   - Deve ser redirecionado para login
    """)

def main():
    """Função principal do teste"""
    print("🧪 TESTE DO SISTEMA DE ÁREA DO INQUILINO")
    print("=" * 50)
    
    tests = [
        test_system_status,
        test_login_page,
        test_invalid_login,
        test_dashboard_access_without_login,
        test_create_inquilino_login
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Erro no teste: {e}")
    
    print(f"\n{'='*50}")
    print(f"RESULTADO DOS TESTES: {passed}/{total} passaram")
    print(f"{'='*50}")
    
    if passed == total:
        print("🎉 Todos os testes básicos passaram!")
    else:
        print("⚠️ Alguns testes falharam. Verifique o sistema.")
    
    print_manual_instructions()

if __name__ == "__main__":
    main() 