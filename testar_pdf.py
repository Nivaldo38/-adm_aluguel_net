#!/usr/bin/env python3
"""
Script para testar a geração de PDFs no sistema de administração de aluguel
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from app.models import Contrato, Inquilino, Unidade, Local
from app.contract_generator import ContractGenerator

def testar_geracao_pdf():
    """Testa a geração de PDFs"""
    print("🧪 Testando geração de PDFs...")
    
    try:
        with app.app_context():
            # Verificar se há contratos no banco
            contratos = Contrato.query.all()
            print(f"📋 Encontrados {len(contratos)} contratos no banco")
            
            if not contratos:
                print("⚠️  Nenhum contrato encontrado. Criando contrato de teste...")
                
                # Criar dados de teste se necessário
                local = Local.query.first()
                if not local:
                    local = Local(nome="Local Teste", endereco="Rua Teste, 123")
                    db.session.add(local)
                    db.session.commit()
                
                unidade = Unidade.query.first()
                if not unidade:
                    unidade = Unidade(numero="101", local_id=local.id)
                    db.session.add(unidade)
                    db.session.commit()
                
                inquilino = Inquilino.query.first()
                if not inquilino:
                    inquilino = Inquilino(
                        nome="João Teste",
                        email="joao.teste@email.com",
                        telefone="(11) 99999-9999",
                        cpf="123.456.789-00"
                    )
                    db.session.add(inquilino)
                    db.session.commit()
                
                # Criar contrato de teste
                contrato = Contrato(
                    inquilino_id=inquilino.id,
                    unidade_id=unidade.id,
                    data_inicio="2025-01-01",
                    data_fim="2025-12-31",
                    valor_aluguel=1500.00,
                    valor_caucao=3000.00,
                    status="ativo"
                )
                db.session.add(contrato)
                db.session.commit()
                print(f"✅ Contrato de teste criado com ID: {contrato.id}")
            
            # Testar geração de PDF
            contrato = Contrato.query.first()
            if contrato:
                print(f"📄 Testando geração de PDF para contrato ID: {contrato.id}")
                
                generator = ContractGenerator()
                pdf_path = generator.generate_contract_pdf(contrato)
                
                if pdf_path and os.path.exists(pdf_path):
                    print(f"✅ PDF gerado com sucesso: {pdf_path}")
                    print(f"📏 Tamanho do arquivo: {os.path.getsize(pdf_path)} bytes")
                else:
                    print("❌ Erro na geração do PDF")
                    return False
            
            print("🎉 Todos os testes de PDF passaram!")
            return True
            
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()
        return False

def testar_manipulacao_pdf():
    """Testa a manipulação de PDFs"""
    print("\n🔧 Testando manipulação de PDFs...")
    
    try:
        from PyPDF2 import PdfReader, PdfWriter
        
        with app.app_context():
            # Criar um PDF de teste simples
            generator = ContractGenerator()
            contrato = Contrato.query.first()
            
            if contrato:
                pdf_path = generator.generate_contract_pdf(contrato)
                
                if pdf_path and os.path.exists(pdf_path):
                    # Testar leitura do PDF
                    with open(pdf_path, 'rb') as file:
                        reader = PdfReader(file)
                        print(f"✅ PDF lido com sucesso: {len(reader.pages)} páginas")
                    
                    # Testar criação de novo PDF
                    writer = PdfWriter()
                    with open(pdf_path, 'rb') as file:
                        reader = PdfReader(file)
                        for page in reader.pages:
                            writer.add_page(page)
                    
                    test_output = "teste_manipulacao.pdf"
                    with open(test_output, 'wb') as output_file:
                        writer.write(output_file)
                    
                    if os.path.exists(test_output):
                        print(f"✅ Manipulação de PDF testada com sucesso: {test_output}")
                        os.remove(test_output)  # Limpar arquivo de teste
                        return True
                    else:
                        print("❌ Erro na manipulação do PDF")
                        return False
                else:
                    print("❌ PDF não encontrado para teste de manipulação")
                    return False
            else:
                print("❌ Nenhum contrato encontrado para teste")
                return False
                
    except Exception as e:
        print(f"❌ Erro durante teste de manipulação: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Iniciando testes de PDF...")
    
    # Testar geração
    geracao_ok = testar_geracao_pdf()
    
    # Testar manipulação
    manipulacao_ok = testar_manipulacao_pdf()
    
    if geracao_ok and manipulacao_ok:
        print("\n🎉 Todos os testes passaram! Sistema de PDF funcionando corretamente.")
    else:
        print("\n❌ Alguns testes falharam. Verifique os erros acima.") 