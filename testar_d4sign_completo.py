#!/usr/bin/env python3
"""
Teste completo do D4Sign com validações detalhadas
"""

from app import app, db
from app.models import Inquilino, Contrato
from app.d4sign_service import D4SignService
import os
import json
from datetime import datetime

def testar_d4sign_completo():
    """Teste completo com validações detalhadas"""
    
    print("🔍 TESTE COMPLETO D4SIGN - VALIDAÇÕES DETALHADAS")
    print("=" * 60)
    
    email_teste = "nivaldoteles38@gmail.com"
    
    with app.app_context():
        # 1. VALIDAR INQUILINO
        print("\n📋 1. VALIDANDO INQUILINO...")
        inquilino = Inquilino.query.filter_by(email=email_teste).first()
        if not inquilino:
            print("❌ ERRO: Inquilino não encontrado!")
            return False
        
        print(f"✅ Inquilino encontrado: {inquilino.nome}")
        print(f"📧 Email: {inquilino.email}")
        print(f"📱 Telefone: {inquilino.telefone}")
        print(f"🏠 Endereço: {inquilino.endereco}")
        
        # 2. VALIDAR CONTRATO
        print("\n📋 2. VALIDANDO CONTRATO...")
        contrato = Contrato.query.filter_by(inquilino_id=inquilino.id, situacao='Ativo').first()
        if not contrato:
            print("❌ ERRO: Contrato ativo não encontrado!")
            return False
        
        print(f"✅ Contrato encontrado: ID {contrato.id}")
        print(f"💰 Valor aluguel: R$ {contrato.valor_aluguel}")
        print(f"📅 Data início: {contrato.data_inicio}")
        print(f"📅 Data fim: {contrato.data_fim}")
        print(f"🏢 Unidade: {contrato.unidade.nome if contrato.unidade else 'N/A'}")
        print(f"🏢 Local: {contrato.unidade.local.nome if contrato.unidade and contrato.unidade.local else 'N/A'}")
        
        # 3. VALIDAR ARQUIVO PDF
        print("\n📋 3. VALIDANDO ARQUIVO PDF...")
        pdf_path = contrato.arquivo_contrato
        if not pdf_path or not os.path.exists(pdf_path):
            print("⚠️ PDF não encontrado, criando PDF de teste...")
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter
            
            pdf_path = f"contrato_teste_{contrato.id}.pdf"
            c = canvas.Canvas(pdf_path, pagesize=letter)
            c.drawString(100, 750, f"CONTRATO DE ALUGUEL - {inquilino.nome}")
            c.drawString(100, 700, f"Valor: R$ {contrato.valor_aluguel}")
            c.drawString(100, 650, f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
            c.drawString(100, 600, "Este é um contrato de teste para validação do D4Sign.")
            c.save()
            
            # Atualizar contrato com o novo PDF
            contrato.arquivo_contrato = pdf_path
            db.session.commit()
            print(f"✅ PDF de teste criado: {pdf_path}")
        else:
            print(f"✅ PDF encontrado: {pdf_path}")
            print(f"📏 Tamanho: {os.path.getsize(pdf_path)} bytes")
        
        # 4. TESTAR SERVIÇO D4SIGN
        print("\n📋 4. TESTANDO SERVIÇO D4SIGN...")
        d4sign = D4SignService()
        
        # Verificar configuração
        print(f"🔧 D4Sign habilitado: {d4sign.enabled}")
        print(f"🔧 Modo simulado: {d4sign.simulated_mode}")
        print(f"🌍 Ambiente: {'Produção' if d4sign.is_production else 'Sandbox'}")
        
        # 5. TESTAR UPLOAD
        print("\n📋 5. TESTANDO UPLOAD DE DOCUMENTO...")
        upload_result = d4sign.upload_document(pdf_path)
        print(f"📤 Resultado upload: {upload_result}")
        
        if not upload_result['success']:
            print("❌ ERRO: Falha no upload!")
            return False
        
        doc_key = upload_result.get('doc_key')
        print(f"✅ Upload bem-sucedido! Doc Key: {doc_key}")
        
        # 6. TESTAR CRIAÇÃO DE ENVELOPE
        print("\n📋 6. TESTANDO CRIAÇÃO DE ENVELOPE...")
        envelope_result = d4sign.create_envelope(contrato, doc_key)
        print(f"📋 Resultado envelope: {envelope_result}")
        
        if not envelope_result['success']:
            print("❌ ERRO: Falha na criação do envelope!")
            return False
        
        envelope_id = envelope_result.get('envelope_id')
        print(f"✅ Envelope criado! ID: {envelope_id}")
        
        # 7. TESTAR ENVIO PARA ASSINATURA
        print("\n📋 7. TESTANDO ENVIO PARA ASSINATURA...")
        signature_result = d4sign.send_contract_for_signature(contrato)
        print(f"✍️ Resultado assinatura: {signature_result}")
        
        if not signature_result['success']:
            print("❌ ERRO: Falha no envio para assinatura!")
            return False
        
        print(f"✅ Contrato enviado para assinatura! Envelope ID: {signature_result.get('envelope_id')}")
        
        # 8. VERIFICAR STATUS NO BANCO
        print("\n📋 8. VERIFICANDO STATUS NO BANCO DE DADOS...")
        db.session.refresh(contrato)
        print(f"📊 Status assinatura: {contrato.status_assinatura}")
        print(f"📊 Envelope ID: {contrato.envelope_id}")
        print(f"📅 Data envio: {contrato.data_envio_assinatura}")
        
        # 9. TESTAR VERIFICAÇÃO DE STATUS
        print("\n📋 9. TESTANDO VERIFICAÇÃO DE STATUS...")
        status_result = d4sign.check_signature_status(contrato)
        print(f"📊 Status atual: {status_result}")
        
        # 10. GERAR RELATÓRIO FINAL
        print("\n📋 10. RELATÓRIO FINAL...")
        print("=" * 60)
        print("✅ TESTE COMPLETO CONCLUÍDO COM SUCESSO!")
        print("=" * 60)
        print(f"👤 Inquilino: {inquilino.nome}")
        print(f"📧 Email: {inquilino.email}")
        print(f"📄 Contrato ID: {contrato.id}")
        print(f"💰 Valor: R$ {contrato.valor_aluguel}")
        print(f"📄 PDF: {pdf_path}")
        print(f"📋 Envelope ID: {contrato.envelope_id}")
        print(f"📊 Status: {contrato.status_assinatura}")
        print(f"📅 Enviado em: {contrato.data_envio_assinatura}")
        
        # Salvar relatório
        relatorio = {
            'teste_realizado_em': datetime.now().isoformat(),
            'inquilino': {
                'nome': inquilino.nome,
                'email': inquilino.email,
                'telefone': inquilino.telefone
            },
            'contrato': {
                'id': contrato.id,
                'valor_aluguel': float(contrato.valor_aluguel),
                'data_inicio': contrato.data_inicio.isoformat() if contrato.data_inicio else None,
                'data_fim': contrato.data_fim.isoformat() if contrato.data_fim else None
            },
            'd4sign': {
                'envelope_id': contrato.envelope_id,
                'status_assinatura': contrato.status_assinatura,
                'data_envio': contrato.data_envio_assinatura.isoformat() if contrato.data_envio_assinatura else None
            },
            'arquivo_pdf': pdf_path,
            'resultado_teste': 'SUCESSO'
        }
        
        with open('relatorio_d4sign_teste.json', 'w', encoding='utf-8') as f:
            json.dump(relatorio, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\n💾 Relatório salvo: relatorio_d4sign_teste.json")
        print("\n🎉 SISTEMA D4SIGN FUNCIONANDO CORRETAMENTE!")
        
        return True

if __name__ == "__main__":
    sucesso = testar_d4sign_completo()
    if sucesso:
        print("\n✅ Todos os testes passaram! O sistema está funcionando.")
    else:
        print("\n❌ Alguns testes falharam. Verifique os logs acima.") 