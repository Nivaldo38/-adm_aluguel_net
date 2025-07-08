"""
Serviço Simulado do D4Sign para Testes
Usado quando não há credenciais da API disponíveis
"""

import os
import shutil
import uuid
from datetime import datetime, timedelta
from app import app, db
from app.models import Contrato, Inquilino

class D4SignSimulado:
    def __init__(self):
        self.enabled = True
        self.simulated_envelopes = {}
        self.simulated_documents = {}
        
    def create_envelope(self, contrato, pdf_path):
        """Simula criação de envelope de assinatura"""
        try:
            # Gerar ID único para o envelope
            envelope_id = f"sim_{uuid.uuid4().hex[:8]}"
            
            # Simular upload do documento
            doc_key = f"doc_{uuid.uuid4().hex[:8]}"
            
            # Criar envelope simulado
            self.simulated_envelopes[envelope_id] = {
                'name': f'Contrato - {contrato.inquilino.nome}',
                'status': 'sent',
                'created_at': datetime.now(),
                'documents': [doc_key],
                'signers': [
                    {
                        'email': contrato.inquilino.email,
                        'name': contrato.inquilino.nome,
                        'status': 'pending'
                    }
                ]
            }
            
            # Simular envio de email
            print(f"📧 [SIMULADO] Email enviado para {contrato.inquilino.email}")
            print(f"🔗 [SIMULADO] Link de assinatura: https://d4sign.com.br/sign/{envelope_id}")
            
            return {
                'success': True,
                'envelope_id': envelope_id,
                'message': 'Envelope simulado criado com sucesso'
            }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Erro ao criar envelope simulado: {str(e)}',
                'envelope_id': None
            }
    
    def get_envelope_status(self, envelope_id):
        """Simula verificação de status do envelope"""
        if envelope_id not in self.simulated_envelopes:
            return {
                'success': False,
                'status': 'not_found',
                'message': 'Envelope não encontrado'
            }
        
        envelope = self.simulated_envelopes[envelope_id]
        
        # Simular diferentes status baseado no tempo
        created_time = envelope['created_at']
        time_diff = datetime.now() - created_time
        
        if time_diff > timedelta(hours=24):
            status = 'signed'
        elif time_diff > timedelta(hours=1):
            status = 'sent'
        else:
            status = 'draft'
        
        # Mapear status
        status_mapping = {
            'draft': 'enviado',
            'sent': 'enviado',
            'signed': 'assinado',
            'completed': 'assinado',
            'cancelled': 'cancelado',
            'expired': 'expirado'
        }
        
        mapped_status = status_mapping.get(status, status)
        
        return {
            'success': True,
            'status': mapped_status,
            'original_status': status,
            'message': f'Status simulado: {mapped_status}'
        }
    
    def cancel_envelope(self, envelope_id):
        """Simula cancelamento de envelope"""
        if envelope_id not in self.simulated_envelopes:
            return {
                'success': False,
                'message': 'Envelope não encontrado'
            }
        
        self.simulated_envelopes[envelope_id]['status'] = 'cancelled'
        
        return {
            'success': True,
            'message': 'Envelope simulado cancelado com sucesso'
        }
    
    def download_signed_document(self, envelope_id, output_path):
        """Simula download do documento assinado"""
        if envelope_id not in self.simulated_envelopes:
            return {
                'success': False,
                'message': 'Envelope não encontrado'
            }
        
        envelope = self.simulated_envelopes[envelope_id]
        
        if envelope['status'] != 'signed':
            return {
                'success': False,
                'message': 'Documento ainda não foi assinado'
            }
        
        try:
            # Simular cópia do documento original com marca de assinatura
            original_path = output_path.replace('_assinado.pdf', '.pdf')
            
            if os.path.exists(original_path):
                # Copiar arquivo original
                shutil.copy2(original_path, output_path)
                
                # Adicionar marca de assinatura simulada
                print(f"📄 [SIMULADO] Documento assinado salvo em: {output_path}")
                
                return {
                    'success': True,
                    'message': 'Documento simulado baixado com sucesso'
                }
            else:
                return {
                    'success': False,
                    'message': 'Documento original não encontrado'
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Erro ao baixar documento simulado: {str(e)}'
            }
    
    def send_contract_for_signature(self, contrato):
        """Simula envio de contrato para assinatura"""
        try:
            # Verificar se já existe envelope
            if contrato.envelope_id:
                return {
                    'success': False,
                    'message': 'Contrato já foi enviado para assinatura'
                }
            
            # Gerar PDF se não existir
            if not contrato.arquivo_contrato or not os.path.exists(contrato.arquivo_contrato):
                return {
                    'success': False,
                    'message': 'Arquivo do contrato não encontrado'
                }
            
            # Criar envelope
            result = self.create_envelope(contrato, contrato.arquivo_contrato)
            
            if result['success']:
                # Atualizar contrato
                contrato.envelope_id = result['envelope_id']
                contrato.status_assinatura = 'enviado'
                contrato.data_envio_assinatura = datetime.now()
                db.session.commit()
                
                return {
                    'success': True,
                    'message': 'Contrato enviado para assinatura simulada',
                    'envelope_id': result['envelope_id']
                }
            else:
                return result
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Erro ao enviar contrato: {str(e)}'
            }
    
    def check_signature_status(self, contrato):
        """Simula verificação de status da assinatura"""
        if not contrato.envelope_id:
            return {
                'success': False,
                'message': 'Contrato não foi enviado para assinatura'
            }
        
        result = self.get_envelope_status(contrato.envelope_id)
        
        if result['success']:
            # Atualizar status no banco
            contrato.status_assinatura = result['status']
            if result['status'] == 'assinado':
                contrato.data_assinatura = datetime.now()
            db.session.commit()
        
        return result
    
    def cancel_signature_process(self, contrato):
        """Simula cancelamento do processo de assinatura"""
        if not contrato.envelope_id:
            return {
                'success': False,
                'message': 'Contrato não foi enviado para assinatura'
            }
        
        result = self.cancel_envelope(contrato.envelope_id)
        
        if result['success']:
            contrato.status_assinatura = 'cancelado'
            db.session.commit()
        
        return result

# Instância global do serviço simulado
d4sign_simulado = D4SignSimulado() 