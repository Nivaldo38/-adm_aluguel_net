"""
Serviço de Notificações Automáticas
"""

import os
import json
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app import app, db
from app.models import Boleto, Contrato, Inquilino, Unidade
from app.email_service import email_service

class NotificationService:
    def __init__(self):
        self.notifications_dir = os.path.join(os.getcwd(), 'notifications')
        self.log_file = os.path.join(self.notifications_dir, 'notification_log.json')
        
        # Criar diretório se não existir
        if not os.path.exists(self.notifications_dir):
            os.makedirs(self.notifications_dir)
    
    def check_boletos_vencendo(self):
        """Verifica boletos vencendo nos próximos 3 dias"""
        hoje = datetime.now().date()
        tres_dias = hoje + timedelta(days=3)
        
        boletos_vencendo = Boleto.query.filter(
            Boleto.status == 'pendente',
            Boleto.data_vencimento >= hoje,
            Boleto.data_vencimento <= tres_dias
        ).all()
        
        for boleto in boletos_vencendo:
            self.send_boleto_vencimento_notification(boleto)
    
    def check_contratos_vencendo(self):
        """Verifica contratos vencendo nos próximos 30 dias"""
        hoje = datetime.now().date()
        trinta_dias = hoje + timedelta(days=30)
        
        contratos_vencendo = Contrato.query.filter(
            Contrato.situacao == 'Ativo',
            Contrato.data_fim.isnot(None),
            Contrato.data_fim >= hoje,
            Contrato.data_fim <= trinta_dias
        ).all()
        
        for contrato in contratos_vencendo:
            self.send_contrato_vencimento_notification(contrato)
    
    def check_unidades_manutencao(self):
        """Verifica unidades em manutenção há mais de 7 dias"""
        hoje = datetime.now().date()
        sete_dias = hoje - timedelta(days=7)
        
        # Aqui você pode adicionar lógica para verificar unidades em manutenção
        # Por enquanto, vamos apenas logar
        unidades_manutencao = Unidade.query.filter_by(status='manutencao').all()
        
        if unidades_manutencao:
            self.send_manutencao_notification(unidades_manutencao)
    
    def send_boleto_vencimento_notification(self, boleto):
        """Envia notificação de boleto vencendo"""
        try:
            contrato = boleto.contrato
            inquilino = contrato.inquilino
            
            if not inquilino.email:
                print(f"⚠️ Inquilino {inquilino.nome} não tem email cadastrado")
                return False
            
            # Calcular dias até vencimento
            dias_vencimento = (boleto.data_vencimento - datetime.now().date()).days
            
            subject = f"Boleto vence em {dias_vencimento} dias - {contrato.unidade.nome}"
            
            # Template do email
            html_content = f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; text-align: center;">
                    <h1>🏠 Sistema de Administração de Aluguel</h1>
                    <h2>Lembrete de Boleto</h2>
                </div>
                
                <div style="padding: 20px; background: #f8f9fa;">
                    <h3>Olá, {inquilino.nome}!</h3>
                    
                    <p>Este é um lembrete sobre seu boleto de aluguel:</p>
                    
                    <div style="background: white; padding: 15px; border-radius: 8px; margin: 15px 0; border-left: 4px solid #28a745;">
                        <h4>📋 Detalhes do Boleto</h4>
                        <p><strong>Unidade:</strong> {contrato.unidade.nome}</p>
                        <p><strong>Mês de Referência:</strong> {boleto.mes_referencia}</p>
                        <p><strong>Valor Total:</strong> R$ {boleto.valor_total:.2f}</p>
                        <p><strong>Data de Vencimento:</strong> {boleto.data_vencimento.strftime('%d/%m/%Y')}</p>
                        <p><strong>Dias Restantes:</strong> {dias_vencimento} dias</p>
                    </div>
                    
                    <div style="background: #fff3cd; padding: 15px; border-radius: 8px; margin: 15px 0; border-left: 4px solid #ffc107;">
                        <h4>⚠️ Importante</h4>
                        <p>Para evitar juros e multas, pague seu boleto até a data de vencimento.</p>
                    </div>
                    
                    <div style="text-align: center; margin: 20px 0;">
                        <a href="#" style="background: #007bff; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block;">
                            📄 Ver Boleto Completo
                        </a>
                    </div>
                </div>
                
                <div style="background: #e9ecef; padding: 15px; text-align: center; font-size: 12px; color: #6c757d;">
                    <p>Este é um email automático do sistema de administração de aluguel.</p>
                    <p>Em caso de dúvidas, entre em contato conosco.</p>
                </div>
            </div>
            """
            
            # Enviar email
            success = email_service.send_email(
                to_email=inquilino.email,
                subject=subject,
                body="Notificação de boleto vencendo",
                html_body=html_content
            )
            
            if success:
                self.log_notification('boleto_vencimento', boleto.id, inquilino.email, success=True)
                print(f"✅ Notificação de boleto enviada para {inquilino.email}")
            else:
                self.log_notification('boleto_vencimento', boleto.id, inquilino.email, success=False)
                print(f"❌ Erro ao enviar notificação para {inquilino.email}")
            
            return success
            
        except Exception as e:
            print(f"❌ Erro ao enviar notificação de boleto: {e}")
            return False
    
    def send_contrato_vencimento_notification(self, contrato):
        """Envia notificação de contrato vencendo"""
        try:
            inquilino = contrato.inquilino
            
            if not inquilino.email:
                print(f"⚠️ Inquilino {inquilino.nome} não tem email cadastrado")
                return False
            
            # Calcular dias até vencimento
            dias_vencimento = (contrato.data_fim - datetime.now().date()).days
            
            subject = f"Contrato vence em {dias_vencimento} dias - {contrato.unidade.nome}"
            
            # Template do email
            html_content = f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; text-align: center;">
                    <h1>🏠 Sistema de Administração de Aluguel</h1>
                    <h2>Lembrete de Contrato</h2>
                </div>
                
                <div style="padding: 20px; background: #f8f9fa;">
                    <h3>Olá, {inquilino.nome}!</h3>
                    
                    <p>Este é um lembrete sobre seu contrato de aluguel:</p>
                    
                    <div style="background: white; padding: 15px; border-radius: 8px; margin: 15px 0; border-left: 4px solid #17a2b8;">
                        <h4>📋 Detalhes do Contrato</h4>
                        <p><strong>Unidade:</strong> {contrato.unidade.nome}</p>
                        <p><strong>Data de Início:</strong> {contrato.data_inicio.strftime('%d/%m/%Y')}</p>
                        <p><strong>Data de Término:</strong> {contrato.data_fim.strftime('%d/%m/%Y')}</p>
                        <p><strong>Valor do Aluguel:</strong> R$ {contrato.valor_aluguel:.2f}</p>
                        <p><strong>Dias Restantes:</strong> {dias_vencimento} dias</p>
                    </div>
                    
                    <div style="background: #d1ecf1; padding: 15px; border-radius: 8px; margin: 15px 0; border-left: 4px solid #17a2b8;">
                        <h4>💡 Próximos Passos</h4>
                        <p>Entre em contato conosco para renovar seu contrato ou fazer a devolução da unidade.</p>
                    </div>
                    
                    <div style="text-align: center; margin: 20px 0;">
                        <a href="#" style="background: #28a745; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block;">
                            📄 Ver Contrato
                        </a>
                    </div>
                </div>
                
                <div style="background: #e9ecef; padding: 15px; text-align: center; font-size: 12px; color: #6c757d;">
                    <p>Este é um email automático do sistema de administração de aluguel.</p>
                    <p>Em caso de dúvidas, entre em contato conosco.</p>
                </div>
            </div>
            """
            
            # Enviar email
            success = email_service.send_email(
                to_email=inquilino.email,
                subject=subject,
                body="Notificação de contrato vencendo",
                html_body=html_content
            )
            
            if success:
                self.log_notification('contrato_vencimento', contrato.id, inquilino.email, success=True)
                print(f"✅ Notificação de contrato enviada para {inquilino.email}")
            else:
                self.log_notification('contrato_vencimento', contrato.id, inquilino.email, success=False)
                print(f"❌ Erro ao enviar notificação para {inquilino.email}")
            
            return success
            
        except Exception as e:
            print(f"❌ Erro ao enviar notificação de contrato: {e}")
            return False
    
    def send_manutencao_notification(self, unidades):
        """Envia notificação sobre unidades em manutenção"""
        try:
            # Email para administrador
            admin_email = "admin@exemplo.com"  # Configurar email do admin
            
            subject = f"Unidades em Manutenção - {len(unidades)} unidades"
            
            # Lista de unidades
            unidades_list = ""
            for unidade in unidades:
                unidades_list += f"<li>{unidade.nome} - {unidade.local.nome}</li>"
            
            html_content = f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <div style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); color: white; padding: 20px; text-align: center;">
                    <h1>🏠 Sistema de Administração de Aluguel</h1>
                    <h2>Alerta de Manutenção</h2>
                </div>
                
                <div style="padding: 20px; background: #f8f9fa;">
                    <h3>Unidades em Manutenção</h3>
                    
                    <div style="background: white; padding: 15px; border-radius: 8px; margin: 15px 0; border-left: 4px solid #dc3545;">
                        <h4>🔧 Unidades Afetadas</h4>
                        <ul>{unidades_list}</ul>
                    </div>
                    
                    <div style="background: #f8d7da; padding: 15px; border-radius: 8px; margin: 15px 0; border-left: 4px solid #dc3545;">
                        <h4>⚠️ Ação Necessária</h4>
                        <p>Verifique o status das manutenções e atualize quando concluídas.</p>
                    </div>
                </div>
                
                <div style="background: #e9ecef; padding: 15px; text-align: center; font-size: 12px; color: #6c757d;">
                    <p>Este é um email automático do sistema de administração de aluguel.</p>
                </div>
            </div>
            """
            
            # Enviar email
            success = email_service.send_email(
                to_email=admin_email,
                subject=subject,
                body="Notificação de manutenção",
                html_body=html_content
            )
            
            if success:
                self.log_notification('manutencao', len(unidades), admin_email, success=True)
                print(f"✅ Notificação de manutenção enviada para {admin_email}")
            else:
                self.log_notification('manutencao', len(unidades), admin_email, success=False)
                print(f"❌ Erro ao enviar notificação para {admin_email}")
            
            return success
            
        except Exception as e:
            print(f"❌ Erro ao enviar notificação de manutenção: {e}")
            return False
    
    def log_notification(self, notification_type, item_id, email, success=True, error_message=None):
        """Registra notificação no log"""
        try:
            log_entry = {
                'type': notification_type,
                'item_id': item_id,
                'email': email,
                'success': success,
                'timestamp': datetime.now().isoformat(),
                'error_message': error_message
            }
            
            # Carregar log existente ou criar novo
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    log = json.load(f)
            else:
                log = []
            
            log.append(log_entry)
            
            # Manter apenas os últimos 1000 registros
            if len(log) > 1000:
                log = log[-1000:]
            
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(log, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"⚠️ Erro ao registrar log: {e}")
    
    def get_notification_stats(self):
        """Retorna estatísticas das notificações"""
        try:
            if not os.path.exists(self.log_file):
                return {
                    'total': 0,
                    'success': 0,
                    'failed': 0,
                    'types': {}
                }
            
            with open(self.log_file, 'r', encoding='utf-8') as f:
                log = json.load(f)
            
            stats = {
                'total': len(log),
                'success': len([l for l in log if l.get('success', False)]),
                'failed': len([l for l in log if not l.get('success', True)]),
                'types': {}
            }
            
            # Contar por tipo
            for entry in log:
                notification_type = entry.get('type', 'unknown')
                if notification_type not in stats['types']:
                    stats['types'][notification_type] = 0
                stats['types'][notification_type] += 1
            
            return stats
            
        except Exception as e:
            print(f"❌ Erro ao obter estatísticas: {e}")
            return {
                'total': 0,
                'success': 0,
                'failed': 0,
                'types': {}
            }
    
    def run_daily_checks(self):
        """Executa todas as verificações diárias"""
        print("🔔 Iniciando verificações diárias de notificações...")
        
        # Verificar boletos vencendo
        self.check_boletos_vencendo()
        
        # Verificar contratos vencendo
        self.check_contratos_vencendo()
        
        # Verificar unidades em manutenção
        self.check_unidades_manutencao()
        
        print("✅ Verificações diárias concluídas!")

# Instância global do serviço
notification_service = NotificationService() 