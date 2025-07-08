"""
Script para testar o sistema de notificações
"""

import os
import sys
from datetime import datetime, timedelta

# Adicionar o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from app.models import Boleto, Contrato, Inquilino, Unidade
from app.notification_service import notification_service

def testar_notificacoes():
    """Testa o sistema de notificações"""
    print("🧪 Testando sistema de notificações...")
    
    with app.app_context():
        # Verificar se há dados para testar
        total_inquilinos = Inquilino.query.count()
        total_boletos = Boleto.query.count()
        total_contratos = Contrato.query.count()
        
        print(f"📊 Dados disponíveis:")
        print(f"   - Inquilinos: {total_inquilinos}")
        print(f"   - Boletos: {total_boletos}")
        print(f"   - Contratos: {total_contratos}")
        
        if total_inquilinos == 0:
            print("❌ Nenhum inquilino cadastrado. Adicione inquilinos primeiro.")
            return
        
        # Testar notificação de teste
        print("\n🔔 Testando notificação de teste...")
        try:
            # Buscar primeiro inquilino com email
            inquilino = Inquilino.query.filter(Inquilino.email.isnot(None)).first()
            
            if not inquilino:
                print("❌ Nenhum inquilino com email cadastrado encontrado.")
                print("💡 Adicione um email para um inquilino para testar as notificações.")
                return
            
            print(f"✅ Inquilino encontrado: {inquilino.nome} ({inquilino.email})")
            
            # Testar envio de email
            from app.email_service import email_service
            
            success = email_service.send_email(
                to_email=inquilino.email,
                subject="Teste de Notificação - Sistema de Aluguel",
                body="Teste de notificação automática",
                html_body="""
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; text-align: center;">
                        <h1>🏠 Sistema de Administração de Aluguel</h1>
                        <h2>Teste de Notificação</h2>
                    </div>
                    
                    <div style="padding: 20px; background: #f8f9fa;">
                        <h3>Olá!</h3>
                        <p>Este é um email de teste do sistema de notificações.</p>
                        
                        <div style="background: white; padding: 15px; border-radius: 8px; margin: 15px 0; border-left: 4px solid #28a745;">
                            <h4>✅ Sistema Funcionando</h4>
                            <p>As notificações automáticas estão configuradas e funcionando corretamente.</p>
                        </div>
                        
                        <div style="background: #e9ecef; padding: 15px; text-align: center; font-size: 12px; color: #6c757d;">
                            <p>Este é um email de teste do sistema de administração de aluguel.</p>
                            <p>Data/Hora: """ + datetime.now().strftime('%d/%m/%Y %H:%M:%S') + """</p>
                        </div>
                    </div>
                </div>
                """
            )
            
            if success:
                print("✅ Email de teste enviado com sucesso!")
            else:
                print("❌ Erro ao enviar email de teste.")
                
        except Exception as e:
            print(f"❌ Erro ao testar notificação: {e}")
        
        # Testar verificações automáticas
        print("\n🔍 Testando verificações automáticas...")
        try:
            notification_service.run_daily_checks()
            print("✅ Verificações automáticas executadas com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao executar verificações: {e}")
        
        # Mostrar estatísticas
        print("\n📈 Estatísticas de notificações:")
        stats = notification_service.get_notification_stats()
        print(f"   - Total: {stats['total']}")
        print(f"   - Sucessos: {stats['success']}")
        print(f"   - Falhas: {stats['failed']}")
        print(f"   - Tipos: {len(stats['types'])}")
        
        if stats['types']:
            print("   - Detalhes por tipo:")
            for tipo, quantidade in stats['types'].items():
                print(f"     * {tipo}: {quantidade}")
        
        print("\n✅ Teste concluído!")

def criar_dados_teste():
    """Cria dados de teste para notificações"""
    print("🔧 Criando dados de teste...")
    
    with app.app_context():
        # Verificar se já existem dados
        if Inquilino.query.count() > 0:
            print("ℹ️ Dados já existem. Pulando criação de dados de teste.")
            return
        
        # Criar local de teste
        from app.models import Local
        local = Local(
            nome="Edifício Teste",
            endereco="Rua Teste, 123",
            cidade="São Paulo",
            estado="SP"
        )
        db.session.add(local)
        db.session.commit()
        
        # Criar unidade de teste
        from app.models import Unidade
        unidade = Unidade(
            nome="Apartamento 101",
            tipo="Apartamento",
            valor_aluguel=1500.00,
            local_id=local.id,
            status="disponivel"
        )
        db.session.add(unidade)
        db.session.commit()
        
        # Criar inquilino de teste
        inquilino = Inquilino(
            nome="João Silva",
            cpf="123.456.789-00",
            email="joao.silva@exemplo.com",
            telefone="(11) 99999-9999",
            situacao="Ativo"
        )
        db.session.add(inquilino)
        db.session.commit()
        
        # Criar contrato de teste
        contrato = Contrato(
            inquilino_id=inquilino.id,
            unidade_id=unidade.id,
            data_inicio=datetime.now().date(),
            data_fim=datetime.now().date() + timedelta(days=30),
            valor_aluguel=1500.00,
            situacao="Ativo"
        )
        db.session.add(contrato)
        db.session.commit()
        
        # Criar boleto de teste
        boleto = Boleto(
            contrato_id=contrato.id,
            mes_referencia="Janeiro/2025",
            data_vencimento=datetime.now().date() + timedelta(days=2),
            valor_aluguel=1500.00,
            valor_agua=50.00,
            valor_luz=80.00,
            valor_condominio=200.00,
            valor_total=1830.00,
            status="pendente"
        )
        db.session.add(boleto)
        db.session.commit()
        
        print("✅ Dados de teste criados com sucesso!")

if __name__ == "__main__":
    print("🚀 Iniciando teste do sistema de notificações...")
    
    # Criar dados de teste se necessário
    criar_dados_teste()
    
    # Testar notificações
    testar_notificacoes()
    
    print("\n🎉 Teste finalizado!") 