#!/usr/bin/env python3
"""
Script para testar a integração com D4Sign
"""

import os
import sys
from datetime import datetime

# Adicionar o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from app.models import Contrato, Inquilino, Unidade, Local
from app.d4sign_service import d4sign_service

def testar_configuracao_d4sign():
    """Testa a configuração básica do D4Sign"""
    print("🔧 TESTE DE CONFIGURAÇÃO D4SIGN")
    print("=" * 50)
    
    # Verificar se o serviço foi inicializado
    print("\n1. ✅ Verificando inicialização do serviço...")
    if d4sign_service.simulated_mode:
        print("   ⚠️ Modo simulado ativo (D4Sign não configurado)")
        print("   💡 Configure as variáveis de ambiente para usar D4Sign real")
        return False
    else:
        print(f"   ✅ D4Sign configurado")
        print(f"   🌐 Ambiente: {'Produção' if d4sign_service.is_production else 'Sandbox'}")
        print(f"   🔗 URL: {d4sign_service.api_url}")
    
    # Testar conexão com a API
    print("\n2. 🔗 Testando conexão com API...")
    try:
        account_info = d4sign_service.get_account_info()
        if account_info['success']:
            print("   ✅ Conexão com API estabelecida")
            print(f"   📊 Informações da conta: {account_info['data']}")
        else:
            print(f"   ❌ Erro na conexão: {account_info['message']}")
            return False
    except Exception as e:
        print(f"   ❌ Erro ao conectar: {e}")
        return False
    
    return True

def testar_upload_documento():
    """Testa upload de documento"""
    print("\n3. 📤 Testando upload de documento...")
    
    # Criar um PDF de teste se não existir
    test_pdf = "teste_contrato.pdf"
    if not os.path.exists(test_pdf):
        print(f"   ⚠️ Arquivo {test_pdf} não encontrado")
        print("   💡 Crie um PDF de teste para continuar")
        return False
    
    try:
        result = d4sign_service.upload_document(test_pdf)
        if result['success']:
            print(f"   ✅ Upload realizado com sucesso")
            print(f"   🔑 Doc Key: {result['doc_key']}")
            return result['doc_key']
        else:
            print(f"   ❌ Erro no upload: {result['message']}")
            return None
    except Exception as e:
        print(f"   ❌ Erro no upload: {e}")
        return None

def testar_criacao_envelope(doc_key):
    """Testa criação de envelope"""
    print("\n4. 📋 Testando criação de envelope...")
    
    # Buscar um contrato de teste
    with app.app_context():
        contrato = Contrato.query.first()
        if not contrato:
            print("   ⚠️ Nenhum contrato encontrado no banco")
            print("   💡 Cadastre um contrato primeiro")
            return None
        
        print(f"   📄 Usando contrato: {contrato.inquilino.nome}")
        
        try:
            result = d4sign_service.create_envelope(contrato, doc_key)
            if result['success']:
                print(f"   ✅ Envelope criado com sucesso")
                print(f"   🆔 Envelope ID: {result['envelope_id']}")
                return result['envelope_id']
            else:
                print(f"   ❌ Erro ao criar envelope: {result['message']}")
                return None
        except Exception as e:
            print(f"   ❌ Erro ao criar envelope: {e}")
            return None

def testar_status_envelope(envelope_id):
    """Testa verificação de status do envelope"""
    print("\n5. 📊 Testando verificação de status...")
    
    try:
        result = d4sign_service.get_envelope_status(envelope_id)
        if result['success']:
            print(f"   ✅ Status verificado")
            print(f"   📈 Status: {result['status']}")
            print(f"   📝 Mensagem: {result['message']}")
            return True
        else:
            print(f"   ❌ Erro ao verificar status: {result['message']}")
            return False
    except Exception as e:
        print(f"   ❌ Erro ao verificar status: {e}")
        return False

def testar_webhook():
    """Testa criação de webhook"""
    print("\n6. 🔗 Testando criação de webhook...")
    
    webhook_url = "https://seudominio.com/webhook/d4sign"
    
    try:
        result = d4sign_service.create_webhook(webhook_url)
        if result['success']:
            print(f"   ✅ Webhook criado com sucesso")
            print(f"   🆔 Webhook ID: {result['webhook_id']}")
        else:
            print(f"   ⚠️ Erro ao criar webhook: {result['message']}")
            print("   💡 Webhooks são opcionais")
    except Exception as e:
        print(f"   ⚠️ Erro ao criar webhook: {e}")

def testar_embed_url(envelope_id):
    """Testa geração de URL de embed"""
    print("\n7. 🌐 Testando geração de URL de embed...")
    
    try:
        result = d4sign_service.get_embed_url(envelope_id)
        if result['success']:
            print(f"   ✅ URL de embed gerada")
            print(f"   🔗 URL: {result['embed_url']}")
        else:
            print(f"   ⚠️ Erro ao gerar URL: {result['message']}")
    except Exception as e:
        print(f"   ⚠️ Erro ao gerar URL: {e}")

def mostrar_estatisticas():
    """Mostra estatísticas dos contratos"""
    print("\n📊 ESTATÍSTICAS DE CONTRATOS")
    print("=" * 30)
    
    with app.app_context():
        total_contratos = Contrato.query.count()
        contratos_enviados = Contrato.query.filter_by(status_assinatura='enviado').count()
        contratos_assinados = Contrato.query.filter_by(status_assinatura='assinado').count()
        contratos_cancelados = Contrato.query.filter_by(status_assinatura='cancelado').count()
        
        print(f"📄 Total de contratos: {total_contratos}")
        print(f"📤 Enviados para assinatura: {contratos_enviados}")
        print(f"✅ Assinados: {contratos_assinados}")
        print(f"❌ Cancelados: {contratos_cancelados}")
        
        # Mostrar contratos com envelope ID
        contratos_com_envelope = Contrato.query.filter(Contrato.envelope_id.isnot(None)).all()
        if contratos_com_envelope:
            print(f"\n📋 Contratos com envelope ID:")
            for contrato in contratos_com_envelope[:5]:  # Mostrar apenas os 5 primeiros
                print(f"   • {contrato.inquilino.nome} - {contrato.envelope_id} ({contrato.status_assinatura})")

def criar_dados_teste():
    """Cria dados de teste se necessário"""
    with app.app_context():
        # Verificar se há dados
        if Contrato.query.count() == 0:
            print("📝 Criando dados de teste...")
            
            # Criar local
            local = Local(nome="Edifício Teste")
            db.session.add(local)
            db.session.commit()
            
            # Criar unidade
            unidade = Unidade(nome="Apto 101", local_id=local.id, status="disponivel")
            db.session.add(unidade)
            db.session.commit()
            
            # Criar inquilino
            inquilino = Inquilino(
                nome="João Silva",
                cpf="123.456.789-00",
                data_nascimento=datetime(1990, 1, 1),
                endereco="Rua Teste, 123",
                cep="12345-678",
                telefone="(11) 99999-9999",
                email="joao@teste.com",
                unidade_id=unidade.id
            )
            db.session.add(inquilino)
            db.session.commit()
            
            # Criar contrato
            contrato = Contrato(
                inquilino_id=inquilino.id,
                unidade_id=unidade.id,
                valor_aluguel=1500.00,
                data_inicio=datetime.now().date(),
                dia_vencimento="05",
                proprietario_nome="Maria Santos",
                proprietario_cnpjcpf="123.456.789-00",
                proprietario_endereco="Rua Proprietário, 456",
                situacao="Ativo"
            )
            db.session.add(contrato)
            db.session.commit()
            
            print("✅ Dados de teste criados")

def main():
    """Função principal de teste"""
    print("🚀 INICIANDO TESTES D4SIGN")
    print("=" * 50)
    
    # Criar dados de teste se necessário
    criar_dados_teste()
    
    # Testar configuração
    if not testar_configuracao_d4sign():
        print("\n❌ CONFIGURAÇÃO FALHOU")
        print("💡 Configure as variáveis de ambiente do D4Sign")
        return
    
    # Testar upload
    doc_key = testar_upload_documento()
    if not doc_key:
        print("\n❌ UPLOAD FALHOU")
        return
    
    # Testar criação de envelope
    envelope_id = testar_criacao_envelope(doc_key)
    if not envelope_id:
        print("\n❌ CRIAÇÃO DE ENVELOPE FALHOU")
        return
    
    # Testar verificação de status
    testar_status_envelope(envelope_id)
    
    # Testar webhook (opcional)
    testar_webhook()
    
    # Testar URL de embed
    testar_embed_url(envelope_id)
    
    # Mostrar estatísticas
    mostrar_estatisticas()
    
    print("\n" + "=" * 50)
    print("✅ TESTES D4SIGN CONCLUÍDOS COM SUCESSO!")
    print("💡 Próximos passos:")
    print("   1. Configure as credenciais reais do D4Sign")
    print("   2. Teste com documentos reais")
    print("   3. Implemente webhooks se necessário")
    print("   4. Configure o ambiente de produção")

if __name__ == "__main__":
    main() 