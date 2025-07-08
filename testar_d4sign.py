#!/usr/bin/env python3
"""
Script para testar a configuração do D4Sign
"""

import os
import sys
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

def testar_configuracao_d4sign():
    """Testa se as variáveis do D4Sign estão configuradas"""
    print("🔍 Testando configuração do D4Sign...")
    print("=" * 50)
    
    # Verificar variáveis de ambiente
    api_url = os.getenv('D4SIGN_API_URL')
    api_token = os.getenv('D4SIGN_API_TOKEN')
    safe_key = os.getenv('D4SIGN_SAFE_KEY')
    
    print(f"📡 API URL: {'✅ Configurado' if api_url else '❌ Não configurado'}")
    print(f"🔑 API Token: {'✅ Configurado' if api_token else '❌ Não configurado'}")
    print(f"🔐 Safe Key: {'✅ Configurado' if safe_key else '❌ Não configurado'}")
    
    if not all([api_url, api_token, safe_key]):
        print("\n❌ Configuração incompleta!")
        print("\nPara configurar o D4Sign:")
        print("1. Crie uma conta em https://www.d4sign.com.br")
        print("2. Obtenha suas credenciais de API")
        print("3. Configure as variáveis de ambiente:")
        print("   - D4SIGN_API_URL=https://api.d4sign.com.br")
        print("   - D4SIGN_API_TOKEN=seu_token_aqui")
        print("   - D4SIGN_SAFE_KEY=sua_safe_key_aqui")
        return False
    
    print("\n✅ Todas as variáveis estão configuradas!")
    return True

def testar_conectividade_d4sign():
    """Testa a conectividade com a API do D4Sign"""
    print("\n🌐 Testando conectividade com D4Sign...")
    print("=" * 50)
    
    try:
        import requests
        from app.d4sign_service import D4SignService
        
        d4sign = D4SignService()
        
        if not d4sign.enabled:
            print("❌ D4Sign não está habilitado")
            return False
        
        # Testar conexão básica
        response = requests.get(
            f"{d4sign.api_url}/documents",
            headers=d4sign.headers,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Conexão com D4Sign estabelecida com sucesso!")
            return True
        else:
            print(f"❌ Erro na conexão: {response.status_code}")
            print(f"Resposta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao conectar com D4Sign: {e}")
        return False

def testar_servico_d4sign():
    """Testa o serviço D4Sign local"""
    print("\n🔧 Testando serviço D4Sign...")
    print("=" * 50)
    
    try:
        from app.d4sign_service import d4sign_service
        
        print(f"✅ Serviço D4Sign carregado: {d4sign_service.enabled}")
        
        if d4sign_service.enabled:
            print("✅ D4Sign está habilitado e pronto para uso!")
            return True
        else:
            print("❌ D4Sign não está habilitado")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao carregar serviço D4Sign: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 Teste de Configuração do D4Sign")
    print("=" * 50)
    
    # Testar configuração
    config_ok = testar_configuracao_d4sign()
    
    if config_ok:
        # Testar conectividade
        conectividade_ok = testar_conectividade_d4sign()
        
        # Testar serviço
        servico_ok = testar_servico_d4sign()
        
        if all([config_ok, conectividade_ok, servico_ok]):
            print("\n🎉 Todos os testes passaram!")
            print("✅ D4Sign está configurado e funcionando corretamente")
            print("\nPróximos passos:")
            print("1. Acesse o sistema em http://localhost:5000")
            print("2. Crie um contrato de teste")
            print("3. Teste o envio para assinatura")
        else:
            print("\n⚠️ Alguns testes falharam")
            print("Verifique a configuração e tente novamente")
    else:
        print("\n❌ Configuração incompleta")
        print("Configure as variáveis de ambiente primeiro")

if __name__ == "__main__":
    main() 