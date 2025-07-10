"""
Configuração do D4Sign - Arquivo de Exemplo
Copie este arquivo para .env e configure suas credenciais
"""

# ===== CONFIGURAÇÃO D4SIGN =====

# Ambiente (sandbox ou production)
D4SIGN_ENVIRONMENT=sandbox

# Credenciais de API (obrigatórias)
D4SIGN_TOKEN_API=seu_token_api_aqui
D4SIGN_CRYPT_KEY=sua_crypt_key_aqui  # Opcional, só se estiver habilitado na conta

# URLs dos ambientes
# Sandbox: https://sandbox.d4sign.com.br/api/v1
# Produção: https://secure.d4sign.com.br/api/v1

# ===== COMO OBTER AS CREDENCIAIS =====

"""
1. Acesse sua conta D4Sign:
   - Sandbox: https://sandbox.d4sign.com.br/criar.html
   - Produção: https://secure.d4sign.com.br/criar.html

2. Faça login e acesse o menu 'Dev API'

3. Copie sua Chave de API (tokenAPI)

4. Se o cryptKey estiver habilitado, copie também

5. Configure as variáveis de ambiente:
"""

# ===== EXEMPLO DE CONFIGURAÇÃO =====

# Para desenvolvimento (Sandbox)
D4SIGN_ENVIRONMENT=sandbox
D4SIGN_TOKEN_API=abc123def456ghi789
D4SIGN_CRYPT_KEY=xyz789uvw456rst123  # Opcional

# Para produção
# D4SIGN_ENVIRONMENT=production
# D4SIGN_TOKEN_API=seu_token_producao
# D4SIGN_CRYPT_KEY=sua_crypt_key_producao

# ===== LIMITES DA API =====

"""
Limite padrão: 10 requisições por hora
Para aumentar o limite, entre em contato: comercial@d4sign.com.br

Para suporte técnico: suporte@d4sign.com.br
"""

# ===== TESTE DE CONFIGURAÇÃO =====

"""
Para testar se a configuração está correta:

1. Configure as variáveis acima
2. Execute: python testar_d4sign.py
3. Verifique se a conexão está funcionando
"""

# ===== WEBHOOKS (OPCIONAL) =====

"""
Para receber notificações automáticas quando documentos forem assinados:

1. Configure uma URL de webhook no seu servidor
2. Use o método create_webhook() do D4SignService
3. O D4Sign enviará POST para sua URL quando houver mudanças

Exemplo:
webhook_url = "https://seudominio.com/webhook/d4sign"
d4sign_service.create_webhook(webhook_url)
"""

# ===== EMBED D4SIGN =====

"""
Para exibir documentos diretamente no seu website:

1. Use o método get_embed_url() do D4SignService
2. A URL retornada pode ser incorporada em um iframe
3. O usuário pode assinar diretamente no seu site

Exemplo:
embed_result = d4sign_service.get_embed_url(envelope_id)
if embed_result['success']:
    embed_url = embed_result['embed_url']
    # Usar embed_url em um iframe
""" 