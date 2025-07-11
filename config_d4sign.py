# Configuração D4Sign
# Ambiente: Sandbox

# Chaves de API
D4SIGN_API_TOKEN = "live_cd026d4be49abf7c543b913e6f4514aed6c3506874617e07e352fc77fcb3cf2d"
D4SIGN_CRYPT_KEY = "live_crypt_MTU7hgVkgnXn2L6ajNa8t1hf6rqnDpRd"

# Configurações do ambiente
D4SIGN_ENVIRONMENT = "sandbox"  # sandbox ou production
D4SIGN_BASE_URL = "https://sandbox.d4sign.com.br/api/v1"

# Configurações de webhook
D4SIGN_WEBHOOK_ENABLED = True
D4SIGN_WEBHOOK_CONTENT_TYPE = "json"  # json ou form-data
D4SIGN_WEBHOOK_HMAC_ENABLED = True
D4SIGN_WEBHOOK_HMAC_KEY = "1bc7c7646b439aa305dbd3ec1bdc02e6da26285c40db3b0c77eca4153aa3e0cd"

# Limites
D4SIGN_RATE_LIMIT = 50  # requisições por hora

# URLs de documentação
D4SIGN_DOCS_URL = "http://docapi.d4sign.com.br/"
D4SIGN_SDK_URL = "https://github.com/d4sign/d4sign-php"

print("✅ Configuração D4Sign carregada!")
print(f"🌍 Ambiente: {D4SIGN_ENVIRONMENT}")
print(f"🔗 Base URL: {D4SIGN_BASE_URL}")
print(f"📊 Rate Limit: {D4SIGN_RATE_LIMIT} req/hora")
print(f"🔐 Webhook HMAC: {'Ativado' if D4SIGN_WEBHOOK_HMAC_ENABLED else 'Desativado'}") 