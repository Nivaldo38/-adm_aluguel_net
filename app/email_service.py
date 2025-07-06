"""
Serviço de Email para Notificações Automáticas
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime, timedelta
from app import app, db
from app.models import Contrato, Inquilino, Boleto

class EmailService:
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.email = os.getenv('EMAIL_USER', '')
        self.password = os.getenv('EMAIL_PASSWORD', '')
        self.enabled = bool(self.email and self.password)
    
    def send_email(self, to_email, subject, body, html_body=None, attachments=None):
        """Envia email"""
        if not self.enabled:
            print(f"📧 Email simulado para {to_email}: {subject}")
            return True
        
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = self.email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Texto simples
            text_part = MIMEText(body, 'plain', 'utf-8')
            msg.attach(text_part)
            
            # HTML se fornecido
            if html_body:
                html_part = MIMEText(html_body, 'html', 'utf-8')
                msg.attach(html_part)
            
            # Anexos
            if attachments:
                for file_path in attachments:
                    if os.path.exists(file_path):
                        with open(file_path, 'rb') as attachment:
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(attachment.read())
                        encoders.encode_base64(part)
                        part.add_header(
                            'Content-Disposition',
                            f'attachment; filename= {os.path.basename(file_path)}'
                        )
                        msg.attach(part)
            
            # Enviar
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email, self.password)
            server.send_message(msg)
            server.quit()
            
            print(f"✅ Email enviado para {to_email}: {subject}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao enviar email: {e}")
            return False
    
    def notify_contract_signed(self, contrato):
        """Notifica quando contrato é assinado"""
        subject = f"Contrato Assinado - {contrato.inquilino.nome}"
        
        body = f"""
        Olá {contrato.inquilino.nome},
        
        Seu contrato foi assinado com sucesso!
        
        Detalhes do Contrato:
        - Local: {contrato.unidade.local.nome}
        - Unidade: {contrato.unidade.nome}
        - Valor: R$ {contrato.valor_aluguel:.2f}
        - Data de Assinatura: {contrato.data_assinatura.strftime('%d/%m/%Y') if contrato.data_assinatura else 'N/A'}
        
        O contrato está disponível para download no sistema.
        
        Atenciosamente,
        Sistema de Gestão de Aluguel
        """
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; color: white; text-align: center;">
                <h1>✅ Contrato Assinado</h1>
            </div>
            <div style="padding: 20px; background: #f9f9f9;">
                <p>Olá <strong>{contrato.inquilino.nome}</strong>,</p>
                <p>Seu contrato foi assinado com sucesso!</p>
                
                <div style="background: white; padding: 15px; border-radius: 8px; margin: 20px 0;">
                    <h3>📋 Detalhes do Contrato:</h3>
                    <ul>
                        <li><strong>Local:</strong> {contrato.unidade.local.nome}</li>
                        <li><strong>Unidade:</strong> {contrato.unidade.nome}</li>
                        <li><strong>Valor:</strong> R$ {contrato.valor_aluguel:.2f}</li>
                        <li><strong>Data de Assinatura:</strong> {contrato.data_assinatura.strftime('%d/%m/%Y') if contrato.data_assinatura else 'N/A'}</li>
                    </ul>
                </div>
                
                <p>O contrato está disponível para download no sistema.</p>
                
                <div style="text-align: center; margin-top: 30px;">
                    <p style="color: #666;">Atenciosamente,<br>Sistema de Gestão de Aluguel</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(contrato.inquilino.email, subject, body, html_body)
    
    def notify_boleto_due(self, boleto):
        """Notifica vencimento de boleto"""
        days_until_due = (boleto.data_vencimento - datetime.now().date()).days
        
        if days_until_due <= 0:
            subject = f"BOLETO VENCIDO - {boleto.contrato.inquilino.nome}"
            urgency = "VENCIDO"
        elif days_until_due <= 3:
            subject = f"BOLETO VENCE HOJE - {boleto.contrato.inquilino.nome}"
            urgency = "VENCE HOJE"
        elif days_until_due <= 7:
            subject = f"BOLETO VENCE EM {days_until_due} DIAS - {boleto.contrato.inquilino.nome}"
            urgency = f"VENCE EM {days_until_due} DIAS"
        else:
            return True  # Não notificar se ainda falta muito tempo
        
        body = f"""
        Olá {boleto.contrato.inquilino.nome},
        
        {urgency}!
        
        Detalhes do Boleto:
        - Valor: R$ {boleto.valor:.2f}
        - Vencimento: {boleto.data_vencimento.strftime('%d/%m/%Y')}
        - Código: {boleto.codigo_barras}
        
        Local: {boleto.contrato.unidade.local.nome} - {boleto.contrato.unidade.nome}
        
        Por favor, realize o pagamento o quanto antes.
        
        Atenciosamente,
        Sistema de Gestão de Aluguel
        """
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: {'#dc3545' if days_until_due <= 0 else '#ffc107'}; padding: 20px; color: white; text-align: center;">
                <h1>⚠️ {urgency}</h1>
            </div>
            <div style="padding: 20px; background: #f9f9f9;">
                <p>Olá <strong>{boleto.contrato.inquilino.nome}</strong>,</p>
                <p><strong>{urgency}!</strong></p>
                
                <div style="background: white; padding: 15px; border-radius: 8px; margin: 20px 0; border-left: 4px solid {'#dc3545' if days_until_due <= 0 else '#ffc107'};">
                    <h3>💰 Detalhes do Boleto:</h3>
                    <ul>
                        <li><strong>Valor:</strong> R$ {boleto.valor:.2f}</li>
                        <li><strong>Vencimento:</strong> {boleto.data_vencimento.strftime('%d/%m/%Y')}</li>
                        <li><strong>Código:</strong> {boleto.codigo_barras}</li>
                    </ul>
                    <p><strong>Local:</strong> {boleto.contrato.unidade.local.nome} - {boleto.contrato.unidade.nome}</p>
                </div>
                
                <p>Por favor, realize o pagamento o quanto antes.</p>
                
                <div style="text-align: center; margin-top: 30px;">
                    <p style="color: #666;">Atenciosamente,<br>Sistema de Gestão de Aluguel</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(boleto.contrato.inquilino.email, subject, body, html_body)
    
    def send_monthly_report(self, contrato):
        """Envia relatório mensal"""
        subject = f"Relatório Mensal - {contrato.inquilino.nome}"
        
        # Buscar boletos do mês
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        boletos_mes = Boleto.query.filter(
            Boleto.contrato_id == contrato.id,
            db.extract('month', Boleto.data_vencimento) == current_month,
            db.extract('year', Boleto.data_vencimento) == current_year
        ).all()
        
        total_boletos = len(boletos_mes)
        boletos_pagos = len([b for b in boletos_mes if b.status == 'pago'])
        valor_total = sum(b.valor for b in boletos_mes)
        valor_pago = sum(b.valor for b in boletos_mes if b.status == 'pago')
        
        body = f"""
        Olá {contrato.inquilino.nome},
        
        Relatório Mensal - {datetime.now().strftime('%B/%Y')}
        
        Resumo:
        - Total de Boletos: {total_boletos}
        - Boletos Pagos: {boletos_pagos}
        - Valor Total: R$ {valor_total:.2f}
        - Valor Pago: R$ {valor_pago:.2f}
        - Pendente: R$ {valor_total - valor_pago:.2f}
        
        Local: {contrato.unidade.local.nome} - {contrato.unidade.nome}
        
        Atenciosamente,
        Sistema de Gestão de Aluguel
        """
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #28a745 0%, #20c997 100%); padding: 20px; color: white; text-align: center;">
                <h1>📊 Relatório Mensal</h1>
                <p>{datetime.now().strftime('%B/%Y')}</p>
            </div>
            <div style="padding: 20px; background: #f9f9f9;">
                <p>Olá <strong>{contrato.inquilino.nome}</strong>,</p>
                <p>Aqui está seu relatório mensal:</p>
                
                <div style="background: white; padding: 15px; border-radius: 8px; margin: 20px 0;">
                    <h3>📋 Resumo:</h3>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                        <div><strong>Total de Boletos:</strong> {total_boletos}</div>
                        <div><strong>Boletos Pagos:</strong> {boletos_pagos}</div>
                        <div><strong>Valor Total:</strong> R$ {valor_total:.2f}</div>
                        <div><strong>Valor Pago:</strong> R$ {valor_pago:.2f}</div>
                    </div>
                    <div style="margin-top: 10px; padding: 10px; background: {'#d4edda' if valor_total == valor_pago else '#f8d7da'}; border-radius: 5px;">
                        <strong>Pendente:</strong> R$ {valor_total - valor_pago:.2f}
                    </div>
                </div>
                
                <p><strong>Local:</strong> {contrato.unidade.local.nome} - {contrato.unidade.nome}</p>
                
                <div style="text-align: center; margin-top: 30px;">
                    <p style="color: #666;">Atenciosamente,<br>Sistema de Gestão de Aluguel</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(contrato.inquilino.email, subject, body, html_body)

# Instância global
email_service = EmailService() 