#!/usr/bin/env python3
"""
Script de teste para verificar se o cadastro de inquilinos mantém os dados preenchidos
em caso de erro de validação.
"""

import requests
import time

def testar_cadastro_inquilino():
    """Testa o cadastro de inquilinos com dados inválidos para verificar se mantém os dados preenchidos."""
    
    base_url = "http://127.0.0.1:5000"
    
    print("🧪 Testando cadastro de inquilinos...")
    print("=" * 50)
    
    # Dados de teste com CPF inválido (menos de 11 dígitos)
    dados_teste = {
        'nome': 'João Silva',
        'cpf': '1234567890',  # CPF inválido - apenas 10 dígitos
        'data_nascimento': '1990-05-15',
        'idade': '33',
        'endereco': 'Rua das Flores, 123',
        'cep': '74000000',
        'telefone': '62999999999',
        'email': 'joao@email.com',
        'unidade_id': '1',
        'local_id': '1'
    }
    
    try:
        # Fazer POST para cadastrar inquilino
        print("📝 Enviando dados de teste...")
        response = requests.post(f"{base_url}/cadastrar_inquilino", data=dados_teste)
        
        if response.status_code == 200:
            print("✅ Página carregada com sucesso")
            
            # Verificar se os dados foram mantidos no formulário
            content = response.text
            
            # Verificar se os campos mantêm os valores
            campos_verificados = []
            
            if 'value="João Silva"' in content:
                campos_verificados.append("✅ Nome mantido")
            else:
                campos_verificados.append("❌ Nome não mantido")
                
            if 'value="1234567890"' in content:
                campos_verificados.append("✅ CPF mantido")
            else:
                campos_verificados.append("❌ CPF não mantido")
                
            if 'value="1990-05-15"' in content:
                campos_verificados.append("✅ Data de nascimento mantida")
            else:
                campos_verificados.append("❌ Data de nascimento não mantida")
                
            if 'value="33"' in content:
                campos_verificados.append("✅ Idade mantida")
            else:
                campos_verificados.append("❌ Idade não mantida")
                
            if 'value="Rua das Flores, 123"' in content:
                campos_verificados.append("✅ Endereço mantido")
            else:
                campos_verificados.append("❌ Endereço não mantido")
                
            if 'value="74000000"' in content:
                campos_verificados.append("✅ CEP mantido")
            else:
                campos_verificados.append("❌ CEP não mantido")
                
            if 'value="62999999999"' in content:
                campos_verificados.append("✅ Telefone mantido")
            else:
                campos_verificados.append("❌ Telefone não mantido")
                
            if 'value="joao@email.com"' in content:
                campos_verificados.append("✅ Email mantido")
            else:
                campos_verificados.append("❌ Email não mantido")
            
            print("\n📋 Resultado da verificação:")
            for campo in campos_verificados:
                print(f"  {campo}")
                
            # Verificar se há mensagem de erro
            if 'CPF inválido' in content:
                print("\n✅ Mensagem de erro exibida corretamente")
            else:
                print("\n❌ Mensagem de erro não encontrada")
                
        else:
            print(f"❌ Erro ao acessar página: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Erro de conexão. Certifique-se de que o servidor está rodando.")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

def testar_cadastro_sucesso():
    """Testa o cadastro de inquilinos com dados válidos."""
    
    base_url = "http://127.0.0.1:5000"
    
    print("\n🧪 Testando cadastro com dados válidos...")
    print("=" * 50)
    
    # Dados válidos para teste
    dados_validos = {
        'nome': 'Maria Santos',
        'cpf': '12345678909',  # CPF válido (fictício)
        'data_nascimento': '1985-08-20',
        'idade': '38',
        'endereco': 'Av. Principal, 456',
        'cep': '74000001',
        'telefone': '62988888888',
        'email': 'maria@email.com',
        'unidade_id': '1',
        'local_id': '1'
    }
    
    try:
        response = requests.post(f"{base_url}/cadastrar_inquilino", data=dados_validos)
        
        if response.status_code == 302:  # Redirecionamento após sucesso
            print("✅ Cadastro realizado com sucesso (redirecionamento)")
        elif response.status_code == 200:
            print("⚠️ Página retornada (possível erro de validação)")
        else:
            print(f"❌ Status inesperado: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Erro de conexão. Certifique-se de que o servidor está rodando.")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

if __name__ == "__main__":
    print("🚀 Iniciando testes de cadastro de inquilinos...")
    print("=" * 60)
    
    # Aguardar um pouco para o servidor inicializar
    print("⏳ Aguardando servidor inicializar...")
    time.sleep(2)
    
    # Testar cadastro com dados inválidos
    testar_cadastro_inquilino()
    
    # Testar cadastro com dados válidos
    testar_cadastro_sucesso()
    
    print("\n" + "=" * 60)
    print("🏁 Testes concluídos!")
    print("\n📝 Instruções:")
    print("1. Acesse http://127.0.0.1:5000/cadastrar_inquilino")
    print("2. Preencha alguns campos e deixe outros em branco")
    print("3. Clique em 'Cadastrar Inquilino'")
    print("4. Verifique se os dados preenchidos foram mantidos")
    print("5. Apenas os campos em branco devem mostrar erro") 