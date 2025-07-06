#!/usr/bin/env python3
"""
Script para testar o envio de credenciais por e-mail
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from app.models import Inquilino
from app.email_service import email_service

def testar_envio_credenciais():
    """Testa o envio de credenciais por e-mail"""
    print("🧪 Testando envio de credenciais por e-mail...")
    
    try:
        with app.app_context():
            # Buscar um inquilino para teste
            inquilino = Inquilino.query.first()
            
            if not inquilino:
                print("❌ Nenhum inquilino encontrado no banco de dados")
                return False
            
            print(f"📧 Testando envio para: {inquilino.nome} ({inquilino.email})")
            
            # Dados de teste
            username = "teste_usuario"
            senha = "123456"
            
            # Enviar credenciais
            resultado = email_service.send_tenant_credentials(inquilino, username, senha)
            
            if resultado:
                print("✅ E-mail de credenciais enviado com sucesso!")
                print(f"   Usuário: {username}")
                print(f"   Senha: {senha}")
                print(f"   Para: {inquilino.email}")
                return True
            else:
                print("❌ Erro ao enviar e-mail de credenciais")
                return False
                
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        return False

def testar_criacao_login():
    """Testa a criação de login com envio de e-mail"""
    print("\n🧪 Testando criação de login com envio de e-mail...")
    
    try:
        with app.app_context():
            # Buscar um inquilino sem login
            inquilino = Inquilino.query.filter_by(username=None).first()
            
            if not inquilino:
                print("❌ Nenhum inquilino sem login encontrado")
                return False
            
            print(f"👤 Testando criação de login para: {inquilino.nome}")
            
            # Importar função
            from app.routes import criar_login_inquilino
            
            # Criar login
            username = f"teste_{inquilino.id}"
            senha = "123456"
            
            success, message = criar_login_inquilino(inquilino.id, username, senha)
            
            if success:
                print(f"✅ Login criado com sucesso!")
                print(f"   Mensagem: {message}")
                print(f"   Usuário: {username}")
                print(f"   Senha: {senha}")
                return True
            else:
                print(f"❌ Erro ao criar login: {message}")
                return False
                
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando testes de credenciais...")
    
    # Teste 1: Envio direto de e-mail
    test1 = testar_envio_credenciais()
    
    # Teste 2: Criação de login com envio
    test2 = testar_criacao_login()
    
    print("\n📊 Resultado dos testes:")
    print(f"   Teste 1 (Envio direto): {'✅ PASSOU' if test1 else '❌ FALHOU'}")
    print(f"   Teste 2 (Criação + envio): {'✅ PASSOU' if test2 else '❌ FALHOU'}")
    
    if test1 and test2:
        print("\n🎉 Todos os testes passaram! O sistema de credenciais está funcionando.")
    else:
        print("\n⚠️  Alguns testes falharam. Verifique as configurações de e-mail.") 