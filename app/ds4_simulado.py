"""
DS4 Simulado para testes de desenvolvimento
"""

import os
import base64
import time
from datetime import datetime, timedelta
import uuid

class DS4Simulado:
    def __init__(self):
        self.base_path = 'https://demo.docusign.net/restapi'
        self.simulated_envelopes = {}
        
    def get_access_token(self):
        """Simula obtenção de token"""
        return "simulated_token_" + str(int(time.time()))
    
    def create_envelope(self, contrato, pdf_path):
        """Simula criação de envelope"""
        try:
            # Gerar ID único para o envelope
            envelope_id = f"sim_{uuid.uuid4().hex[:8]}"
            
            # Simular dados do envelope
            envelope_data = {
                'envelope_id': envelope_id,
                'status': 'sent',
                'created': datetime.now(),
                'recipients': [
                    {
                        'name': contrato.proprietario_nome,
                        'email': contrato.proprietario_email or 'admin@exemplo.com',
                        'status': 'completed'  # Locador assina automaticamente
                    },
                    {
                        'name': contrato.inquilino.nome,
                        'email': contrato.inquilino.email or 'inquilino@exemplo.com',
                        'status': 'sent'  # Inquilino recebe email
                    }
                ]
            }
            
            # Salvar dados simulados
            self.simulated_envelopes[envelope_id] = envelope_data
            
            print(f"✅ Envelope simulado criado: {envelope_id}")
            return envelope_id
            
        except Exception as e:
            print(f"❌ Erro ao criar envelope simulado: {e}")
            return None
    
    def get_envelope_status(self, envelope_id):
        """Simula verificação de status"""
        if envelope_id in self.simulated_envelopes:
            envelope = self.simulated_envelopes[envelope_id]
            
            # Simular progresso da assinatura
            time_elapsed = datetime.now() - envelope['created']
            
            if time_elapsed.seconds < 30:  # Primeiros 30 segundos
                return 'sent'
            elif time_elapsed.seconds < 60:  # Entre 30 e 60 segundos
                # Simular assinatura do inquilino
                envelope['recipients'][1]['status'] = 'completed'
                return 'completed'
            else:
                return 'completed'
        
        return 'not_found'
    
    def download_signed_document(self, envelope_id, output_path):
        """Simula download do documento assinado"""
        try:
            # Simular geração de PDF assinado
            with open(output_path, 'w') as f:
                f.write(f"CONTRATO ASSINADO DIGITALMENTE\n")
                f.write(f"Envelope ID: {envelope_id}\n")
                f.write(f"Data de Assinatura: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
                f.write(f"Status: Assinado por todas as partes\n")
                f.write(f"\n--- CONTEÚDO DO CONTRATO ---\n")
                f.write(f"[Aqui estaria o PDF original com as assinaturas digitais]\n")
            
            print(f"✅ Documento simulado salvo em: {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao baixar documento simulado: {e}")
            return False
    
    def send_contract_for_signature(self, contrato, pdf_path):
        """Simula envio para assinatura"""
        try:
            # Criar envelope simulado
            envelope_id = self.create_envelope(contrato, pdf_path)
            
            if envelope_id:
                # Simular email enviado para inquilino
                print(f"📧 Email simulado enviado para: {contrato.inquilino.email or 'inquilino@exemplo.com'}")
                print(f"📋 Link simulado: https://demo.docusign.net/signing/{envelope_id}")
                
                return {
                    'success': True,
                    'envelope_id': envelope_id,
                    'message': 'Contrato enviado para assinatura digital (SIMULADO)'
                }
            else:
                return {
                    'success': False,
                    'message': 'Erro ao criar envelope simulado'
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Erro: {str(e)}'
            }
    
    def check_signature_status(self, contrato):
        """Simula verificação de status"""
        if not contrato.envelope_id:
            return {'status': 'nao_enviado'}
        
        status = self.get_envelope_status(contrato.envelope_id)
        
        if status == 'completed':
            # Simular download do documento assinado
            signed_path = pdf_path.replace('.pdf', '_assinado.pdf')
            if self.download_signed_document(contrato.envelope_id, signed_path):
                print(f"✅ Contrato assinado simulado: {signed_path}")
        
        return {'status': status}

# Função para usar DS4 simulado
def get_ds4_instance():
    """Retorna instância do DS4 (real ou simulado)"""
    # Verificar se as credenciais estão configuradas
    account_id = os.getenv('DS4_ACCOUNT_ID', '')
    integration_key = os.getenv('DS4_INTEGRATION_KEY', '')
    
    if account_id and integration_key:
        # Usar DS4 real
        from app.ds4_integration import DS4Integration
        return DS4Integration()
    else:
        # Usar DS4 simulado
        print("🔧 Usando DS4 Simulado (configure as credenciais para usar DS4 real)")
        return DS4Simulado() 