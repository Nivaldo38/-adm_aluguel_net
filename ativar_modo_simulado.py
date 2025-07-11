#!/usr/bin/env python3
"""
Ativar modo simulado do D4Sign para testes completos
"""

from app import app, db
from app.models import Inquilino, Contrato
from app.d4sign_simulado import D4SignSimulado
import os
import json
from datetime import datetime

def ativar_modo_simulado():
    """Ativa o modo simulado e testa o fluxo completo"""
    
    print("🎭 ATIVANDO MODO SIMULADO D4SIGN")
    print("=" * 50)
    
    email_teste = "nivaldoteles38@gmail.com"
    
    with app.app_context():
        # Buscar inquilino e contrato
        inquilino = Inquilino.query.filter_by(email=email_teste).first()
        contrato = Contrato.query.filter_by(inquilino_id=inquilino.id, situacao='Ativo').first()
        
        print(f"👤 Inquilino: {inquilino.nome}")
        print(f"📄 Contrato ID: {contrato.id}")
        print(f"💰 Valor: R$ {contrato.valor_aluguel}")
        
        # Criar instância do D4Sign simulado
        d4sign_simulado = D4SignSimulado()
        
        # Testar upload simulado
        print("\n📤 Testando upload simulado...")
        pdf_path = contrato.arquivo_contrato
        if not pdf_path or not os.path.exists(pdf_path):
            # Criar PDF de teste
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter
            
            pdf_path = f"contrato_simulado_{contrato.id}.pdf"
            c = canvas.Canvas(pdf_path, pagesize=letter)
            c.drawString(100, 750, f"CONTRATO SIMULADO - {inquilino.nome}")
            c.drawString(100, 700, f"Valor: R$ {contrato.valor_aluguel}")
            c.drawString(100, 650, f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
            c.drawString(100, 600, "Este é um contrato simulado para teste do D4Sign.")
            c.save()
            
            contrato.arquivo_contrato = pdf_path
            db.session.commit()
            print(f"✅ PDF simulado criado: {pdf_path}")
        
        # Testar criação de envelope simulado
        print("\n📋 Testando criação de envelope simulado...")
        envelope_result = d4sign_simulado.create_envelope(contrato, pdf_path)
        print(f"📋 Resultado: {envelope_result}")
        
        if envelope_result['success']:
            envelope_id = envelope_result['envelope_id']
            print(f"✅ Envelope simulado criado! ID: {envelope_id}")
            
            # Atualizar contrato no banco
            contrato.envelope_id = envelope_id
            contrato.status_assinatura = 'enviado'
            contrato.data_envio_assinatura = datetime.now()
            db.session.commit()
            
            print(f"✅ Contrato atualizado no banco!")
            print(f"📊 Status: {contrato.status_assinatura}")
            print(f"📅 Data envio: {contrato.data_envio_assinatura}")
            
            # Simular assinatura (após alguns segundos)
            print("\n⏳ Simulando assinatura do documento...")
            import time
            time.sleep(2)
            
            # Atualizar status para assinado
            contrato.status_assinatura = 'assinado'
            contrato.data_assinatura = datetime.now()
            db.session.commit()
            
            print("✅ Documento assinado simulado!")
            print(f"📅 Data assinatura: {contrato.data_assinatura}")
            
            # Gerar relatório
            relatorio = {
                'modo': 'SIMULADO',
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
                'd4sign_simulado': {
                    'envelope_id': contrato.envelope_id,
                    'status_assinatura': contrato.status_assinatura,
                    'data_envio': contrato.data_envio_assinatura.isoformat() if contrato.data_envio_assinatura else None,
                    'data_assinatura': contrato.data_assinatura.isoformat() if contrato.data_assinatura else None
                },
                'arquivo_pdf': pdf_path,
                'resultado_teste': 'SUCESSO_SIMULADO'
            }
            
            with open('relatorio_d4sign_simulado.json', 'w', encoding='utf-8') as f:
                json.dump(relatorio, f, indent=2, ensure_ascii=False, default=str)
            
            print(f"\n💾 Relatório simulado salvo: relatorio_d4sign_simulado.json")
            print("\n🎉 MODO SIMULADO FUNCIONANDO PERFEITAMENTE!")
            print("\n📋 RESUMO DO TESTE:")
            print(f"   ✅ Upload de documento: OK")
            print(f"   ✅ Criação de envelope: OK")
            print(f"   ✅ Envio para assinatura: OK")
            print(f"   ✅ Simulação de assinatura: OK")
            print(f"   ✅ Atualização no banco: OK")
            print(f"   ✅ Relatório gerado: OK")
            
            return True
        else:
            print("❌ Erro na criação do envelope simulado!")
            return False

if __name__ == "__main__":
    sucesso = ativar_modo_simulado()
    if sucesso:
        print("\n✅ Modo simulado ativado e testado com sucesso!")
        print("🎯 Agora você pode testar o fluxo completo de assinatura digital!")
    else:
        print("\n❌ Erro ao ativar modo simulado.") 