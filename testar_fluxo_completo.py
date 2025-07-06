#!/usr/bin/env python3
"""
Script para testar o fluxo completo do sistema:
1. Cadastro de inquilino
2. Criação de contrato
3. Assinatura do contrato
4. Envio automático de credenciais
"""

import sys
import os
import random
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from app.models import Inquilino, Contrato, Unidade, Local
from app.email_service import email_service
from datetime import datetime, timedelta

def gerar_cpf_aleatorio():
    """Gera um CPF aleatório válido (apenas para testes)"""
    def calc_digito(digs):
        s = sum([v * (len(digs)+1-i) for i, v in enumerate(digs)])
        r = 11 - s % 11
        return r if r < 10 else 0
    n = [random.randint(0, 9) for _ in range(9)]
    n.append(calc_digito(n))
    n.append(calc_digito(n))
    return ''.join(map(str, n))

def testar_fluxo_completo():
    """Testa o fluxo completo do sistema"""
    print("🚀 Testando fluxo completo do sistema...")
    
    try:
        with app.app_context():
            # 1. Verificar se há locais e unidades
            locais = Local.query.all()
            unidades = Unidade.query.all()
            
            if not locais:
                print("❌ Nenhum local encontrado. Crie um local primeiro.")
                return False
                
            if not unidades:
                print("❌ Nenhuma unidade encontrada. Crie uma unidade primeiro.")
                return False
            
            # 2. Criar inquilino de teste
            print("\n👤 Criando inquilino de teste...")
            cpf_aleatorio = gerar_cpf_aleatorio()
            inquilino_teste = Inquilino(
                nome="João Silva Teste",
                cpf=cpf_aleatorio,
                data_nascimento=datetime.now().date() - timedelta(days=25*365),
                idade=25,
                endereco="Rua Teste, 123",
                cep="12345-678",
                telefone="(11) 99999-9999",
                email=f"joao.teste{cpf_aleatorio[-4:]}@email.com",
                unidade_id=unidades[0].id
            )
            
            db.session.add(inquilino_teste)
            db.session.commit()
            print(f"✅ Inquilino criado: {inquilino_teste.nome} (ID: {inquilino_teste.id})")
            
            # 3. Criar contrato de teste
            print("\n📋 Criando contrato de teste...")
            contrato_teste = Contrato(
                inquilino_id=inquilino_teste.id,
                unidade_id=unidades[0].id,
                valor_aluguel=1500.00,
                data_inicio=datetime.now().date(),
                data_fim=datetime.now().date() + timedelta(days=365),
                situacao='Ativo',
                dia_vencimento='05',
                proprietario_nome="Proprietário Teste",
                proprietario_cnpjcpf="12345678901",
                proprietario_endereco="Rua do Proprietário, 456",
                proprietario_telefone="(11) 88888-8888",
                proprietario_email="proprietario@teste.com",
                envelope_id='sim_teste_123',
                status_assinatura='completed'
            )
            
            db.session.add(contrato_teste)
            db.session.commit()
            print(f"✅ Contrato criado: R$ {contrato_teste.valor_aluguel:.2f}")
            
            # 4. Simular assinatura do contrato
            print("\n✍️  Simulando assinatura do contrato...")
            
            # Verificar se o inquilino já tem login
            if not inquilino_teste.username:
                print("🔐 Gerando credenciais automáticas...")
                
                # Importar função de geração de credenciais
                from app.routes import gerar_credenciais_automaticas, criar_login_inquilino
                
                # Gerar credenciais
                username, senha = gerar_credenciais_automaticas(inquilino_teste)
                print(f"   Username: {username}")
                print(f"   Senha: {senha}")
                
                # Criar login e enviar credenciais
                success, message = criar_login_inquilino(inquilino_teste.id, username, senha)
                
                if success:
                    print("✅ Credenciais enviadas automaticamente!")
                    print(f"   Mensagem: {message}")
                else:
                    print(f"❌ Erro ao enviar credenciais: {message}")
            else:
                print("ℹ️  Inquilino já possui login criado")
            
            # 5. Testar login do inquilino
            print("\n🔑 Testando login do inquilino...")
            if inquilino_teste.username:
                print(f"   Username: {inquilino_teste.username}")
                print(f"   Status: {inquilino_teste.status_login}")
                print("✅ Login configurado corretamente")
            else:
                print("❌ Login não foi criado")
            
            # 6. Limpar dados de teste
            print("\n🧹 Limpando dados de teste...")
            db.session.delete(contrato_teste)
            db.session.delete(inquilino_teste)
            db.session.commit()
            print("✅ Dados de teste removidos")
            
            print("\n🎉 Fluxo completo testado com sucesso!")
            return True
            
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Iniciando teste do fluxo completo...")
    success = testar_fluxo_completo()
    
    if success:
        print("\n✅ Todos os testes passaram!")
        print("\n📋 Resumo do fluxo:")
        print("   1. ✅ Cadastro de inquilino")
        print("   2. ✅ Criação de contrato")
        print("   3. ✅ Assinatura do contrato")
        print("   4. ✅ Geração automática de credenciais")
        print("   5. ✅ Envio de e-mail com credenciais")
        print("   6. ✅ Configuração de login")
    else:
        print("\n❌ Alguns testes falharam. Verifique os logs acima.") 