"""
Serviço de Integração com D4Sign para Assinatura Digital
Baseado na API REST D4Sign v1.0
"""

import os
import requests
import json
import base64
from datetime import datetime
from app import app, db
from app.models import Contrato, Inquilino

class D4SignService:
    def __init__(self):
        # Configurações do D4Sign conforme documentação
        self.production_url = "https://secure.d4sign.com.br/api/v1"
        self.sandbox_url = "https://sandbox.d4sign.com.br/api/v1"
        
        # Determinar ambiente
        self.is_production = os.getenv('D4SIGN_ENVIRONMENT', 'sandbox').lower() == 'production'
        self.api_url = self.production_url if self.is_production else self.sandbox_url
        
        # Credenciais de autenticação - tentar variáveis de ambiente primeiro
        self.token_api = os.getenv('D4SIGN_TOKEN_API', '')
        self.crypt_key = os.getenv('D4SIGN_CRYPT_KEY', '')
        
        # Se não estiver nas variáveis de ambiente, tentar arquivo de configuração
        if not self.token_api:
            try:
                from config_d4sign import D4SIGN_API_TOKEN, D4SIGN_CRYPT_KEY
                self.token_api = D4SIGN_API_TOKEN
                self.crypt_key = D4SIGN_CRYPT_KEY
                print("✅ Chaves D4Sign carregadas do arquivo de configuração")
            except ImportError:
                print("⚠️ Arquivo config_d4sign.py não encontrado")
        
        # Verificar se está habilitado
        self.enabled = bool(self.token_api)
        
        if not self.enabled:
            print("⚠️ D4Sign não configurado - usando modo simulado")
            from app.d4sign_simulado import d4sign_simulado
            self.simulated_mode = True
            self.simulated_service = d4sign_simulado
        else:
            self.simulated_mode = False
            print(f"✅ D4Sign configurado - Ambiente: {'Produção' if self.is_production else 'Sandbox'}")
            print(f"🔑 Token API: {self.token_api[:20]}...")
            print(f"🔐 Crypt Key: {self.crypt_key[:20]}...")
    
    def _get_auth_params(self):
        """Retorna parâmetros de autenticação conforme documentação"""
        params = {'tokenAPI': self.token_api}
        if self.crypt_key:
            params['cryptKey'] = self.crypt_key
        return params
    
    def _make_request(self, method, endpoint, data=None, files=None):
        """Faz requisição para API do D4Sign com headers corretos"""
        url = f"{self.api_url}/{endpoint}"
        
        # Headers conforme documentação
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        
        # Parâmetros de autenticação
        params = self._get_auth_params()
        
        try:
            if method.upper() == 'GET':
                response = requests.get(url, params=params, headers=headers)
            elif method.upper() == 'POST':
                if files:
                    # Para upload de arquivos, não usar Content-Type JSON
                    headers.pop('Content-Type', None)
                    response = requests.post(url, params=params, headers=headers, files=files, data=data)
                else:
                    response = requests.post(url, params=params, headers=headers, json=data)
            elif method.upper() == 'DELETE':
                response = requests.delete(url, params=params, headers=headers)
            else:
                raise ValueError(f"Método HTTP não suportado: {method}")
            
            # Verificar resposta
            if response.status_code >= 500:
                return {
                    'success': False,
                    'message': f"Erro do servidor D4Sign: {response.status_code}",
                    'details': response.text
                }
            
            # Tentar parsear JSON
            try:
                result = response.json()
                return {
                    'success': response.status_code < 400,
                    'data': result,
                    'status_code': response.status_code
                }
            except json.JSONDecodeError:
                return {
                    'success': response.status_code < 400,
                    'data': response.text,
                    'status_code': response.status_code
                }
                
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'message': f"Erro de conexão: {str(e)}"
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Erro inesperado: {str(e)}"
            }
    
    def upload_document(self, pdf_path):
        """
        Passo 1: Upload do documento
        Endpoint: POST /documents/upload
        """
        if not self.enabled:
            if self.simulated_mode:
                return self.simulated_service.upload_document(pdf_path)
            else:
                return {
                    'success': False,
                    'message': 'D4Sign não está configurado'
                }
        
        try:
            # Verificar se arquivo existe
            if not os.path.exists(pdf_path):
                return {
                    'success': False,
                    'message': f'Arquivo não encontrado: {pdf_path}'
                }
            
            # Preparar arquivo para upload
            with open(pdf_path, 'rb') as file:
                files = {'file': (os.path.basename(pdf_path), file, 'application/pdf')}
                
                # Fazer upload
                result = self._make_request('POST', 'documents/upload', files=files)
                
                if result['success']:
                    # Verificar se data é um dicionário
                    if isinstance(result['data'], dict):
                        doc_key = result['data'].get('uuid') or result['data'].get('key')
                    else:
                        # Se data é string, pode ser o próprio doc_key
                        doc_key = result['data'] if result['data'] else None
                    
                    # Se ainda não temos doc_key, gerar um temporário
                    if not doc_key:
                        import uuid
                        doc_key = f"temp_{uuid.uuid4().hex[:8]}"
                        print(f"⚠️ Doc key não encontrada na resposta, usando temporário: {doc_key}")
                    
                    return {
                        'success': True,
                        'doc_key': doc_key,
                        'message': 'Documento enviado com sucesso'
                    }
                else:
                    return {
                        'success': False,
                        'message': result['message'],
                        'details': result.get('data')
                    }
                    
        except Exception as e:
            return {
                'success': False,
                'message': f'Erro ao fazer upload: {str(e)}'
            }
    
    def create_webhook(self, webhook_url):
        """
        Passo 2: Cadastrar webhook (POSTBack) - OPCIONAL
        Endpoint: POST /webhooks
        """
        if not self.enabled:
            return {
                'success': False,
                'message': 'D4Sign não está configurado'
            }
        
        webhook_data = {
            'url': webhook_url,
            'events': ['envelope_signed', 'envelope_cancelled', 'envelope_expired']
        }
        
        result = self._make_request('POST', 'webhooks', data=webhook_data)
        
        if result['success']:
            return {
                'success': True,
                'webhook_id': result['data'].get('id'),
                'message': 'Webhook cadastrado com sucesso'
            }
        else:
            return {
                'success': False,
                'message': result['message']
            }
    
    def create_envelope(self, contrato, doc_key):
        """
        Passo 3: Criar envelope com signatários
        Endpoint: POST /envelopes
        """
        if not self.enabled:
            if self.simulated_mode:
                return self.simulated_service.create_envelope(contrato, doc_key)
            else:
                return {
                    'success': False,
                    'message': 'D4Sign não está configurado'
                }
        
        # Verificar se inquilino tem email
        if not contrato.inquilino.email:
            return {
                'success': False,
                'message': 'Inquilino não possui email cadastrado'
            }
        
        # Dados do envelope conforme documentação
        envelope_data = {
            'name': f'Contrato de Aluguel - {contrato.inquilino.nome}',
            'message': f'Contrato de aluguel para {contrato.unidade.nome} - {contrato.unidade.local.nome}',
            'skip_email': False,
            'workflow': 1,  # Assinatura sequencial
            'documents': [doc_key],
            'signers': [
                {
                    'email': contrato.inquilino.email,
                    'name': contrato.inquilino.nome,
                    'send_automatic_email': True,
                    'custom_message': f'Olá {contrato.inquilino.nome}, por favor assine o contrato de aluguel da unidade {contrato.unidade.nome}.',
                    'lock_after_sign': True
                }
            ]
        }
        
        result = self._make_request('POST', 'envelopes', data=envelope_data)
        
        if result['success']:
            envelope_id = result['data'].get('uuid') or result['data'].get('id')
            return {
                'success': True,
                'envelope_id': envelope_id,
                'message': 'Envelope criado com sucesso'
            }
        else:
            return {
                'success': False,
                'message': result.get('message', 'Erro desconhecido'),
                'details': result.get('data')
            }
    
    def get_envelope_status(self, envelope_id):
        """
        Verifica status do envelope
        Endpoint: GET /envelopes/{envelope_id}
        """
        if not self.enabled:
            if self.simulated_mode:
                return self.simulated_service.get_envelope_status(envelope_id)
            else:
                return {
                    'success': False,
                    'status': 'nao_configurado',
                    'message': 'D4Sign não está configurado'
                }
        
        result = self._make_request('GET', f'envelopes/{envelope_id}')
        
        if result['success']:
            data = result['data']
            status = data.get('status', 'unknown')
            
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
                'message': f'Status: {mapped_status}',
                'data': data
            }
        else:
            return {
                'success': False,
                'status': 'erro',
                'message': result['message']
            }
    
    def cancel_envelope(self, envelope_id):
        """
        Cancela envelope de assinatura
        Endpoint: DELETE /envelopes/{envelope_id}
        """
        if not self.enabled:
            if self.simulated_mode:
                return self.simulated_service.cancel_envelope(envelope_id)
            else:
                return {
                    'success': False,
                    'message': 'D4Sign não está configurado'
                }
        
        result = self._make_request('DELETE', f'envelopes/{envelope_id}')
        
        if result['success']:
            return {
                'success': True,
                'message': 'Envelope cancelado com sucesso'
            }
        else:
            return {
                'success': False,
                'message': result['message']
            }
    
    def download_signed_document(self, envelope_id, output_path):
        """
        Download do documento assinado
        Endpoint: GET /envelopes/{envelope_id}/documents
        """
        if not self.enabled:
            if self.simulated_mode:
                return self.simulated_service.download_signed_document(envelope_id, output_path)
            else:
                return {
                    'success': False,
                    'message': 'D4Sign não está configurado'
                }
        
        try:
            # Fazer download
            url = f"{self.api_url}/envelopes/{envelope_id}/documents"
            params = self._get_auth_params()
            headers = {'Accept': 'application/json'}
            
            response = requests.get(url, params=params, headers=headers)
            
            if response.status_code == 200:
                # Salvar arquivo
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                
                return {
                    'success': True,
                    'message': f'Documento salvo em: {output_path}'
                }
            else:
                return {
                    'success': False,
                    'message': f'Erro ao fazer download: {response.status_code}'
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Erro ao fazer download: {str(e)}'
            }
    
    def get_embed_url(self, envelope_id):
        """
        Gera URL para EMBED D4Sign (exibir documento no website)
        Endpoint: GET /envelopes/{envelope_id}/embed
        """
        if not self.enabled:
            return {
                'success': False,
                'message': 'D4Sign não está configurado'
            }
        
        result = self._make_request('GET', f'envelopes/{envelope_id}/embed')
        
        if result['success']:
            embed_url = result['data'].get('url')
            return {
                'success': True,
                'embed_url': embed_url,
                'message': 'URL de embed gerada com sucesso'
            }
        else:
            return {
                'success': False,
                'message': result['message']
            }
    
    def send_contract_for_signature(self, contrato):
        """
        Processo completo: enviar contrato para assinatura
        """
        if not self.enabled:
            if self.simulated_mode:
                return self.simulated_service.send_contract_for_signature(contrato)
            else:
                return {
                    'success': False,
                    'message': 'D4Sign não está configurado'
                }
        
        try:
            # Verificar se contrato tem arquivo PDF
            if not contrato.arquivo_contrato or not os.path.exists(contrato.arquivo_contrato):
                return {
                    'success': False,
                    'message': 'Arquivo do contrato não encontrado'
                }
            
            # Passo 1: Upload do documento
            print("📤 Fazendo upload do documento...")
            upload_result = self.upload_document(contrato.arquivo_contrato)
            if not upload_result['success']:
                return upload_result
            
            doc_key = upload_result['doc_key']
            print(f"✅ Upload concluído - Doc Key: {doc_key}")
            
            # Passo 2: Criar envelope
            print("📋 Criando envelope de assinatura...")
            envelope_result = self.create_envelope(contrato, doc_key)
            if not envelope_result['success']:
                return envelope_result
            
            envelope_id = envelope_result['envelope_id']
            print(f"✅ Envelope criado - ID: {envelope_id}")
            
            # Atualizar contrato no banco
            contrato.envelope_id = envelope_id
            contrato.status_assinatura = 'enviado'
            contrato.data_envio_assinatura = datetime.now()
            db.session.commit()
            
            return {
                'success': True,
                'envelope_id': envelope_id,
                'message': 'Contrato enviado para assinatura com sucesso'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erro ao enviar contrato: {str(e)}'
            }
    
    def check_signature_status(self, contrato):
        """
        Verifica status da assinatura do contrato
        """
        if not contrato.envelope_id:
            return {
                'success': False,
                'message': 'Contrato não possui envelope ID'
            }
        
        result = self.get_envelope_status(contrato.envelope_id)
        
        if result['success']:
            # Atualizar status no banco se mudou
            if contrato.status_assinatura != result['status']:
                contrato.status_assinatura = result['status']
                if result['status'] == 'assinado':
                    contrato.data_assinatura = datetime.now()
                db.session.commit()
            
            return result
        else:
            return result
    
    def cancel_signature_process(self, contrato):
        """
        Cancela processo de assinatura
        """
        if not contrato.envelope_id:
            return {
                'success': False,
                'message': 'Contrato não possui envelope ID'
            }
        
        result = self.cancel_envelope(contrato.envelope_id)
        
        if result['success']:
            # Atualizar status no banco
            contrato.status_assinatura = 'cancelado'
            db.session.commit()
        
        return result
    
    def get_account_info(self):
        """
        Obtém informações da conta D4Sign
        Endpoint: GET /account
        """
        if not self.enabled:
            return {
                'success': False,
                'message': 'D4Sign não está configurado'
            }
        
        result = self._make_request('GET', 'account')
        return result

# Instância global do serviço
d4sign_service = D4SignService() 