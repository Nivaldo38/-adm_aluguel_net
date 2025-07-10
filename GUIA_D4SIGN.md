# 🖋️ Guia Completo - Integração D4Sign

## 📋 Visão Geral

Este guia explica como configurar e usar a integração com o D4Sign para assinatura digital de contratos no sistema de administração de aluguel.

## 🔧 Configuração Inicial

### 1. Criar Conta D4Sign

**Para Desenvolvimento (Sandbox):**
- Acesse: https://sandbox.d4sign.com.br/criar.html
- Crie uma conta gratuita
- Não possui validade jurídica

**Para Produção:**
- Acesse: https://secure.d4sign.com.br/criar.html
- Crie uma conta paga
- Possui validade jurídica completa

### 2. Obter Credenciais de API

1. Faça login na sua conta D4Sign
2. Acesse o menu **'Dev API'**
3. Copie sua **Chave de API (tokenAPI)**
4. Se o **cryptKey** estiver habilitado, copie também

### 3. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```bash
# Ambiente (sandbox ou production)
D4SIGN_ENVIRONMENT=sandbox

# Credenciais de API (obrigatórias)
D4SIGN_TOKEN_API=sua_chave_api_aqui
D4SIGN_CRYPT_KEY=sua_crypt_key_aqui  # Opcional
```

## 🚀 Testando a Integração

### 1. Teste Básico

Execute o script de teste:

```bash
python testar_d4sign.py
```

Este script irá:
- ✅ Verificar configuração
- ✅ Testar conexão com API
- ✅ Fazer upload de documento
- ✅ Criar envelope de assinatura
- ✅ Verificar status
- ✅ Testar webhooks (opcional)

### 2. Teste Manual

1. Acesse o sistema: http://localhost:5000
2. Crie um contrato
3. Gere o PDF do contrato
4. Clique em "Enviar para Assinatura"
5. Verifique o status da assinatura

## 📋 Funcionalidades Implementadas

### 1. **Upload de Documentos**
```python
result = d4sign_service.upload_document(pdf_path)
if result['success']:
    doc_key = result['doc_key']
```

### 2. **Criação de Envelopes**
```python
result = d4sign_service.create_envelope(contrato, doc_key)
if result['success']:
    envelope_id = result['envelope_id']
```

### 3. **Verificação de Status**
```python
result = d4sign_service.get_envelope_status(envelope_id)
status = result['status']  # enviado, assinado, cancelado, expirado
```

### 4. **Cancelamento de Assinatura**
```python
result = d4sign_service.cancel_envelope(envelope_id)
```

### 5. **Download de Documentos Assinados**
```python
result = d4sign_service.download_signed_document(envelope_id, output_path)
```

### 6. **Webhooks (Opcional)**
```python
result = d4sign_service.create_webhook(webhook_url)
```

### 7. **Embed D4Sign**
```python
result = d4sign_service.get_embed_url(envelope_id)
embed_url = result['embed_url']  # URL para iframe
```

## 🔄 Fluxo Completo de Assinatura

### Passo 1: Upload do Documento
```python
upload_result = d4sign_service.upload_document(contrato.arquivo_contrato)
doc_key = upload_result['doc_key']
```

### Passo 2: Criar Envelope
```python
envelope_result = d4sign_service.create_envelope(contrato, doc_key)
envelope_id = envelope_result['envelope_id']
```

### Passo 3: Enviar para Assinatura
- O D4Sign envia email automaticamente para o inquilino
- O inquilino acessa o link e assina digitalmente
- O sistema recebe notificação via webhook (se configurado)

### Passo 4: Verificar Status
```python
status_result = d4sign_service.check_signature_status(contrato)
if status_result['status'] == 'assinado':
    # Contrato foi assinado
    # Enviar credenciais automaticamente
```

## 📧 Configuração de Email

### Variáveis de Ambiente para Email
```bash
# Configuração SMTP
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=seu_email@gmail.com
SMTP_PASSWORD=sua_senha_app
SMTP_USE_TLS=True

# Email do administrador
ADMIN_EMAIL=admin@seudominio.com
```

### Templates de Email

O sistema envia emails automáticos para:
- ✅ Notificação de contrato enviado para assinatura
- ✅ Lembrete de assinatura pendente
- ✅ Confirmação de assinatura realizada
- ✅ Credenciais de acesso (quando aplicável)

## 🔗 Webhooks (Opcional)

### Configurar Webhook

1. Crie uma rota no seu servidor:
```python
@app.route('/webhook/d4sign', methods=['POST'])
def d4sign_webhook():
    data = request.json
    # Processar notificação do D4Sign
    return jsonify({'success': True})
```

2. Registre o webhook:
```python
webhook_url = "https://seudominio.com/webhook/d4sign"
d4sign_service.create_webhook(webhook_url)
```

### Eventos de Webhook
- `envelope_signed`: Contrato foi assinado
- `envelope_cancelled`: Assinatura foi cancelada
- `envelope_expired`: Envelope expirou

## 🌐 Embed D4Sign

### Exibir Documento no Website

```html
<!-- Exibir documento para assinatura -->
<iframe src="{{ embed_url }}" width="100%" height="600px"></iframe>
```

### Implementação no Sistema

```python
@app.route('/visualizar_contrato_embed/<int:contrato_id>')
def visualizar_contrato_embed(contrato_id):
    contrato = Contrato.query.get_or_404(contrato_id)
    
    if contrato.envelope_id:
        result = d4sign_service.get_embed_url(contrato.envelope_id)
        if result['success']:
            return render_template('visualizar_contrato_embed.html', 
                                contrato=contrato, 
                                embed_url=result['embed_url'])
    
    flash('Contrato não possui envelope de assinatura.', 'warning')
    return redirect(url_for('listar_contratos'))
```

## 🔒 Segurança

### Validação de Documentos
- ✅ Verificação de integridade do PDF
- ✅ Validação de assinatura digital
- ✅ Log de todas as operações
- ✅ Backup automático de documentos

### Controle de Acesso
- ✅ Apenas inquilinos autorizados podem assinar
- ✅ Verificação de email do signatário
- ✅ Timeout automático de envelopes
- ✅ Cancelamento de assinaturas

## 📊 Monitoramento

### Logs de Atividade
```python
# Verificar logs do D4Sign
@app.route('/logs_d4sign')
def logs_d4sign():
    logs = d4sign_service.get_activity_logs()
    return render_template('logs_d4sign.html', logs=logs)
```

### Estatísticas
- 📈 Total de contratos enviados
- ✅ Contratos assinados
- ❌ Contratos cancelados
- ⏰ Tempo médio de assinatura

## 🛠️ Troubleshooting

### Problemas Comuns

**1. "D4Sign não configurado"**
- Verifique se as variáveis de ambiente estão configuradas
- Confirme se o arquivo `.env` existe
- Reinicie o servidor após configurar

**2. "Erro de conexão com API"**
- Verifique se as credenciais estão corretas
- Confirme se está usando o ambiente correto (sandbox/production)
- Verifique a conectividade com a internet

**3. "Arquivo não encontrado"**
- Confirme se o PDF do contrato foi gerado
- Verifique se o caminho do arquivo está correto
- Gere novamente o contrato se necessário

**4. "Email não enviado"**
- Verifique se o inquilino tem email cadastrado
- Confirme a configuração SMTP
- Teste o envio de email manualmente

### Logs de Debug

Ative logs detalhados:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📞 Suporte

### Contatos D4Sign
- **Comercial**: comercial@d4sign.com.br
- **Suporte**: suporte@d4sign.com.br
- **Documentação**: https://docs.d4sign.com.br

### Limites da API
- **Padrão**: 10 requisições por hora
- **Para aumentar**: Entre em contato com o comercial
- **Suporte 24/7**: Disponível para contas pagas

## 🎯 Próximos Passos

1. **Configure as credenciais reais** do D4Sign
2. **Teste com documentos reais** de contratos
3. **Implemente webhooks** para notificações automáticas
4. **Configure o ambiente de produção**
5. **Treine os usuários** no uso da assinatura digital

## ✅ Checklist de Configuração

- [ ] Criar conta D4Sign (sandbox/production)
- [ ] Obter credenciais de API
- [ ] Configurar variáveis de ambiente
- [ ] Testar conexão com API
- [ ] Testar upload de documentos
- [ ] Testar criação de envelopes
- [ ] Configurar webhooks (opcional)
- [ ] Testar fluxo completo
- [ ] Configurar emails automáticos
- [ ] Treinar usuários

---

**🎉 Parabéns!** Sua integração com D4Sign está pronta para uso! 