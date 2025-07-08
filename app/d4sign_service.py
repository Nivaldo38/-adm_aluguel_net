"""
Serviço de Integração com D4Sign para Assinatura Digital
"""

import os
import requests
import json
from datetime import datetime
from app import app, db
from app.models import Contrato, Inquilino

class D4SignService:
    def __init__(self):
        # Configurações do D4Sign
        self.api_url = os.getenv('D4SIGN_API_URL', 'https://api.d4sign.com.br')
        self.api_token = os.getenv('D4SIGN_API_TOKEN', '')
        self.safe_key = os.getenv('D4SIGN_SAFE_KEY', '')
        self.enabled = bool(self.api_token and self.safe_key)
        
        # Se não há credenciais, usar modo simulado
        if not self.enabled:
            print("⚠️ D4Sign não configurado - usando modo simulado")
            from app.d4sign_simulado import d4sign_simulado
            self.simulated_mode = True
            self.simulated_service = d4sign_simulado
        else:
            self.simulated_mode = False
        
        # Headers padrão
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_token}'
        }
    
    def create_envelope(self, contrato, pdf_path):
        """Cria um envelope de assinatura no D4Sign"""
        if not self.enabled:
            if self.simulated_mode:
                return self.simulated_service.create_envelope(contrato, pdf_path)
            else:
                return {
                    'success': False,
                    'message': 'D4Sign não está configurado. Configure as variáveis de ambiente.',
                    'envelope_id': None
                }
        
        try:
            # Upload do documento
            upload_result = self.upload_document(pdf_path)
            if not upload_result['success']:
                return upload_result
            
            doc_key = upload_result['doc_key']
            
            # Criar envelope
            envelope_data = {
                'name': f'Contrato - {contrato.inquilino.nome}',
                'message': f'Contrato de aluguel para {contrato.unidade.nome}',
                'skip_email': False,
                'workflow': 1,  # Assinatura sequencial
                'documents': [doc_key],
                'signers': [
                    {
                        'email': contrato.inquilino.email,
                        'name': contrato.inquilino.nome,
                        'send_automatic_email': True,
                        'custom_message': f'Olá {contrato.inquilino.nome}, por favor assine o contrato de aluguel.',
                        'lock_after_sign': True
                    }
                ]
            }
            
            response = requests.post(
                f'{self.api_url}/envelopes',
                headers=self.headers,
                json=envelope_data
            )
            
            if response.status_code == 201:
                result = response.json()
                return {
                    'success': True,
                    'envelope_id': result['uuid'],
                    'message': 'Envelope criado com sucesso'
                }
            else:
                return {
                    'success': False,
                    'message': f'Erro ao criar envelope: {response.text}',
                    'envelope_id': None
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Erro ao criar envelope: {str(e)}',
                'envelope_id': None
            }
    
    def upload_document(self, pdf_path):
        """Faz upload do documento para o D4Sign"""
        try:
            with open(pdf_path, 'rb') as file:
                files = {'file': file}
                response = requests.post(
                    f'{self.api_url}/documents/upload',
                    headers={'Authorization': f'Bearer {self.api_token}'},
                    files=files
                )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    'success': True,
                    'doc_key': result['uuid'],
                    'message': 'Documento enviado com sucesso'
                }
            else:
                return {
                    'success': False,
                    'message': f'Erro ao fazer upload: {response.text}',
                    'doc_key': None
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Erro ao fazer upload: {str(e)}',
                'doc_key': None
            }
    
    def get_envelope_status(self, envelope_id):
        """Verifica o status do envelope de assinatura"""
        if not self.enabled:
            if self.simulated_mode:
                return self.simulated_service.get_envelope_status(envelope_id)
            else:
                return {
                    'success': False,
                    'status': 'nao_configurado',
                    'message': 'D4Sign não está configurado'
                }
        
        try:
            response = requests.get(
                f'{self.api_url}/envelopes/{envelope_id}',
                headers=self.headers
            )
            
            if response.status_code == 200:
                result = response.json()
                status = result.get('status', 'unknown')
                
                # Mapear status do D4Sign para nosso sistema
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
                    'message': f'Status: {mapped_status}'
                }
            else:
                return {
                    'success': False,
                    'status': 'erro',
                    'message': f'Erro ao verificar status: {response.text}'
                }
                
        except Exception as e:
            return {
                'success': False,
                'status': 'erro',
                'message': f'Erro ao verificar status: {str(e)}'
            }
    
    def cancel_envelope(self, envelope_id):
        """Cancela um envelope de assinatura"""
        if not self.enabled:
            if self.simulated_mode:
                return self.simulated_service.cancel_envelope(envelope_id)
            else:
                return {
                    'success': False,
                    'message': 'D4Sign não está configurado'
                }
        
        try:
            response = requests.delete(
                f'{self.api_url}/envelopes/{envelope_id}',
                headers=self.headers
            )
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'message': 'Envelope cancelado com sucesso'
                }
            else:
                return {
                    'success': False,
                    'message': f'Erro ao cancelar envelope: {response.text}'
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Erro ao cancelar envelope: {str(e)}'
            }
    
    def download_signed_document(self, envelope_id, output_path):
        """Baixa o documento assinado"""
        if not self.enabled:
            if self.simulated_mode:
                return self.simulated_service.download_signed_document(envelope_id, output_path)
            else:
                return {
                    'success': False,
                    'message': 'D4Sign não está configurado'
                }
        
        try:
            response = requests.get(
                f'{self.api_url}/envelopes/{envelope_id}/download',
                headers=self.headers
            )
            
            if response.status_code == 200:
                with open(output_path, 'wb') as file:
                    file.write(response.content)
                
                return {
                    'success': True,
                    'message': 'Documento baixado com sucesso',
                    'path': output_path
                }
            else:
                return {
                    'success': False,
                    'message': f'Erro ao baixar documento: {response.text}'
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Erro ao baixar documento: {str(e)}'
            }
    
    def send_contract_for_signature(self, contrato):
        """Envia contrato para assinatura via D4Sign"""
        try:
            # Verificar se o contrato foi gerado
            if not contrato.arquivo_contrato:
                return {
                    'success': False,
                    'message': 'Contrato deve ser gerado antes de enviar para assinatura.',
                    'envelope_id': None
                }
            
            # Caminho do arquivo PDF
            pdf_path = os.path.join('contracts', contrato.arquivo_contrato)
            
            if not os.path.exists(pdf_path):
                return {
                    'success': False,
                    'message': 'Arquivo do contrato não encontrado.',
                    'envelope_id': None
                }
            
            # Criar envelope no D4Sign
            result = self.create_envelope(contrato, pdf_path)
            
            if result['success']:
                # Atualizar contrato no banco
                contrato.status_assinatura = 'enviado'
                contrato.data_envio_assinatura = datetime.now()
                contrato.envelope_id = result['envelope_id']
                db.session.commit()
                
                return {
                    'success': True,
                    'message': f"Contrato enviado para assinatura digital! Envelope ID: {result['envelope_id']}",
                    'envelope_id': result['envelope_id']
                }
            else:
                return result
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Erro ao enviar para assinatura: {str(e)}',
                'envelope_id': None
            }
    
    def check_signature_status(self, contrato):
        """Verifica status da assinatura e atualiza automaticamente"""
        try:
            if not contrato.envelope_id:
                return {
                    'success': False,
                    'message': 'Contrato não foi enviado para assinatura.',
                    'status': 'nao_enviado'
                }
            
            # Verificar status no D4Sign
            result = self.get_envelope_status(contrato.envelope_id)
            
            if result['success']:
                # Atualizar status no banco se mudou
                if contrato.status_assinatura != result['status']:
                    contrato.status_assinatura = result['status']
                    
                    # Se foi assinado, registrar data
                    if result['status'] == 'assinado' and not contrato.data_assinatura:
                        contrato.data_assinatura = datetime.now()
                    
                    db.session.commit()
                
                return {
                    'success': True,
                    'status': result['status'],
                    'message': f'Status da assinatura: {result["status"]}'
                }
            else:
                return result
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Erro ao verificar status: {str(e)}',
                'status': 'erro'
            }
    
    def cancel_signature_process(self, contrato):
        """Cancela processo de assinatura"""
        try:
            if not contrato.envelope_id:
                return {
                    'success': False,
                    'message': 'Contrato não foi enviado para assinatura.'
                }
            
            # Cancelar no D4Sign
            result = self.cancel_envelope(contrato.envelope_id)
            
            if result['success']:
                # Atualizar status no banco
                contrato.status_assinatura = 'cancelado'
                db.session.commit()
                
                return {
                    'success': True,
                    'message': 'Processo de assinatura cancelado.'
                }
            else:
                return result
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Erro ao cancelar assinatura: {str(e)}'
            }

# Instância global do serviço
d4sign_service = D4SignService() 