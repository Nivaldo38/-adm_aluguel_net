#!/usr/bin/env python3
"""
Teste rápido da configuração D4Sign
"""

import os
import sys

def testar_configuracao_atual():
    """Testa a configuração atual do D4Sign"""
    print("🔧 TESTE RÁPIDO - CONFIGURAÇÃO D4SIGN")
    print("=" * 50)
    
    # Verificar variáveis de ambiente
    print("\n1. 📋 Verificando variáveis de ambiente:")
    
    token_api = os.getenv('D4SIGN_TOKEN_API', '')
    crypt_key = os.getenv('D4SIGN_CRYPT_KEY', '')
    environment = os.getenv('D4SIGN_ENVIRONMENT', 'sandbox')
    
    print(f"   🌐 Ambiente: {environment}")
    print(f"   🔑 Token API: {'✅ Configurado' if token_api else '❌ Não configurado'}")
    print(f"   🔐 Crypt Key: {'✅ Configurado' if crypt_key else '❌ Não configurado'}")
    
    if not token_api:
        print("\n⚠️ D4Sign não configurado!")
        print("💡 Execute: python configurar_d4sign.py")
        return False
    
    # Testar importação do serviço
    print("\n2. 🔧 Testando serviço D4Sign:")
    try:
        from app.d4sign_service import d4sign_service
        
        print(f"   ✅ Serviço importado com sucesso")
        print(f"   🔧 Habilitado: {d4sign_service.enabled}")
        print(f"   🌐 Ambiente: {'Produção' if d4sign_service.is_production else 'Sandbox'}")
        print(f"   🔗 URL: {d4sign_service.api_url}")
        
        if d4sign_service.simulated_mode:
            print("   ⚠️ Modo simulado ativo")
            return False
        else:
            print("   ✅ Modo real ativo")
            
    except Exception as e:
        print(f"   ❌ Erro ao importar: {e}")
        return False
    
    # Testar conexão com API
    print("\n3. 🔗 Testando conexão com API:")
    try:
        account_info = d4sign_service.get_account_info()
        if account_info['success']:
            print("   ✅ Conexão estabelecida")
            print(f"   📊 Resposta: {account_info.get('data', 'N/A')}")
        else:
            print(f"   ❌ Erro na conexão: {account_info['message']}")
            return False
    except Exception as e:
        print(f"   ❌ Erro ao conectar: {e}")
        return False
    
    print("\n✅ Configuração D4Sign válida!")
    return True

def mostrar_proximos_passos():
    """Mostra próximos passos"""
    print("\n📋 PRÓXIMOS PASSOS:")
    print("1. Execute: python testar_d4sign.py")
    print("2. Teste o sistema: python run.py")
    print("3. Acesse: http://localhost:5000")
    print("4. Crie um contrato e teste a assinatura digital")

def main():
    """Função principal"""
    if testar_configuracao_atual():
        mostrar_proximos_passos()
    else:
        print("\n❌ D4Sign não está configurado corretamente")
        print("💡 Execute: python configurar_d4sign.py")

if __name__ == "__main__":
    main() 