import os
import base64
import requests
from datetime import datetime, timedelta
from docusign_esign import ApiClient, EnvelopesApi, EnvelopeDefinition, Document, Signer, SignHere, Tabs, ApiException

class DS4Integration:
    def __init__(self):
        # Configurações DS4 - você precisará configurar essas variáveis
        self.account_id = os.getenv('DS4_ACCOUNT_ID', '')
        self.integration_key = os.getenv('DS4_INTEGRATION_KEY', '')
        self.user_id = os.getenv('DS4_USER_ID', '')
        self.private_key_path = os.getenv('DS4_PRIVATE_KEY_PATH', '')
        self.base_path = 'https://demo.docusign.net/restapi'  # Use 'https://www.docusign.net/restapi' para produção
        
    def get_access_token(self):
        """Obtém token de acesso do DS4"""
        try:
            # Para produção, você precisará implementar OAuth2
            # Por enquanto, vamos usar uma implementação básica
            return "demo_token"  # Placeholder
        except Exception as e:
            print(f"Erro ao obter token: {e}")
            return None
    
    def create_envelope(self, contrato, pdf_path):
        """Cria envelope para assinatura digital"""
        try:
            # Ler o PDF
            with open(pdf_path, "rb") as file:
                document_content = file.read()
            
            # Criar documento
            document = Document(
                document_base64=base64.b64encode(document_content).decode('utf-8'),
                name='Contrato de Locação',
                file_extension='pdf',
                document_id='1'
            )
            
            # Criar envelope
            envelope_definition = EnvelopeDefinition(
                email_subject="Contrato de Locação - Assinatura Digital",
                documents=[document],
                recipients=self._create_recipients(contrato),
                status="sent"
            )
            
            # Configurar API client
            api_client = ApiClient()
            api_client.set_base_path(self.base_path)
            api_client.set_oauth_header_token(self.get_access_token())
            
            # Criar envelope
            envelope_api = EnvelopesApi(api_client)
            results = envelope_api.create_envelope(
                account_id=self.account_id,
                envelope_definition=envelope_definition
            )
            
            return results.envelope_id
            
        except Exception as e:
            print(f"Erro ao criar envelope: {e}")
            return None
    
    def _create_recipients(self, contrato):
        """Cria lista de destinatários para assinatura"""
        # Locador (assinatura automática)
        signer1 = Signer(
            email=contrato.proprietario_email or "admin@exemplo.com",
            name=contrato.proprietario_nome,
            recipient_id="1",
            routing_order="1"
        )
        
        # Inquilino (assinatura manual)
        signer2 = Signer(
            email=contrato.inquilino.email or "inquilino@exemplo.com",
            name=contrato.inquilino.nome,
            recipient_id="2",
            routing_order="2"
        )
        
        # Configurar posições de assinatura
        sign_here1 = SignHere(
            anchor_string="/sn1/",
            anchor_units="pixels",
            anchor_y_offset="10",
            anchor_x_offset="20"
        )
        
        sign_here2 = SignHere(
            anchor_string="/sn2/",
            anchor_units="pixels",
            anchor_y_offset="10",
            anchor_x_offset="20"
        )
        
        # Criar tabs
        signer1.tabs = Tabs(sign_here_tabs=[sign_here1])
        signer2.tabs = Tabs(sign_here_tabs=[sign_here2])
        
        return [signer1, signer2]
    
    def get_envelope_status(self, envelope_id):
        """Obtém status do envelope"""
        try:
            api_client = ApiClient()
            api_client.set_base_path(self.base_path)
            api_client.set_oauth_header_token(self.get_access_token())
            
            envelope_api = EnvelopesApi(api_client)
            envelope = envelope_api.get_envelope(
                account_id=self.account_id,
                envelope_id=envelope_id
            )
            
            return envelope.status
            
        except Exception as e:
            print(f"Erro ao obter status: {e}")
            return None
    
    def download_signed_document(self, envelope_id, output_path):
        """Baixa documento assinado"""
        try:
            api_client = ApiClient()
            api_client.set_base_path(self.base_path)
            api_client.set_oauth_header_token(self.get_access_token())
            
            envelope_api = EnvelopesApi(api_client)
            document = envelope_api.get_document(
                account_id=self.account_id,
                envelope_id=envelope_id,
                document_id='1'
            )
            
            with open(output_path, 'wb') as f:
                f.write(document)
            
            return True
            
        except Exception as e:
            print(f"Erro ao baixar documento: {e}")
            return False
    
    def send_contract_for_signature(self, contrato, pdf_path):
        """Envia contrato para assinatura digital"""
        try:
            # Criar envelope
            envelope_id = self.create_envelope(contrato, pdf_path)
            
            if envelope_id:
                # Salvar envelope_id no banco
                contrato.envelope_id = envelope_id
                contrato.status_assinatura = 'enviado'
                
                # Atualizar banco de dados
                from app import db
                db.session.commit()
                
                return {
                    'success': True,
                    'envelope_id': envelope_id,
                    'message': 'Contrato enviado para assinatura digital'
                }
            else:
                return {
                    'success': False,
                    'message': 'Erro ao criar envelope'
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Erro: {str(e)}'
            }
    
    def check_signature_status(self, contrato):
        """Verifica status da assinatura"""
        if not contrato.envelope_id:
            return {'status': 'nao_enviado'}
        
        status = self.get_envelope_status(contrato.envelope_id)
        
        if status == 'completed':
            # Baixar documento assinado
            signed_path = pdf_path.replace('.pdf', '_assinado.pdf')
            if self.download_signed_document(contrato.envelope_id, signed_path):
                contrato.arquivo_contrato_assinado = signed_path
                contrato.status_assinatura = 'assinado'
                from app import db
                db.session.commit()
        
        return {'status': status} 