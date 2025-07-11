#!/usr/bin/env python3
"""
Teste completo de fluxo de assinatura D4Sign usando inquilino já cadastrado
"""

from app import app, db
from app.models import Inquilino, Contrato
from app.d4sign_service import D4SignService
import os
from datetime import datetime

def main():
    email_teste = "nivaldoteles38@gmail.com"
    print(f"🔍 Buscando inquilino com e-mail: {email_teste}")
    
    with app.app_context():
        inquilino = Inquilino.query.filter_by(email=email_teste).first()
        if not inquilino:
            print("❌ Inquilino não encontrado!")
            return
        print(f"✅ Inquilino encontrado: {inquilino.nome} (ID: {inquilino.id})")
        
        contrato = Contrato.query.filter_by(inquilino_id=inquilino.id, situacao='Ativo').first()
        if not contrato:
            print("❌ Nenhum contrato ativo encontrado para este inquilino!")
            return
        print(f"✅ Contrato ativo encontrado (ID: {contrato.id})")
        
        # Verifica se já existe um PDF do contrato
        pdf_path = contrato.arquivo_contrato or "teste_d4sign.pdf"
        if not os.path.exists(pdf_path):
            # Cria um PDF de teste se não existir
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter
            c = canvas.Canvas(pdf_path, pagesize=letter)
            c.drawString(100, 750, f"Contrato de Teste para {inquilino.nome}")
            c.drawString(100, 700, f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
            c.save()
            print(f"📄 PDF de teste criado: {pdf_path}")
        else:
            print(f"📄 Usando PDF existente: {pdf_path}")
        
        # Envia para assinatura via D4Sign
        d4sign = D4SignService()
        print("🚀 Enviando contrato para assinatura digital...")
        resultado = d4sign.send_contract_for_signature(contrato)
        if resultado.get('success'):
            print(f"✅ Contrato enviado para assinatura! Envelope ID: {resultado.get('envelope_id')}")
            print(f"Mensagem: {resultado.get('message')}")
        else:
            print(f"❌ Falha ao enviar para assinatura: {resultado.get('message')}")
            if resultado.get('details'):
                print(f"Detalhes: {resultado.get('details')}")

if __name__ == "__main__":
    main() 