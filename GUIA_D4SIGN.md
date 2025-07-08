# Guia de Configuração e Uso do D4Sign

## 📋 Visão Geral

Este guia explica como configurar e usar o sistema de assinatura digital D4Sign no sistema de administração de aluguel.

## 🔧 Configuração das Variáveis de Ambiente

### 1. Obter Credenciais do D4Sign

1. Acesse [https://www.d4sign.com.br](https://www.d4sign.com.br)
2. Crie uma conta ou faça login
3. Vá para "Configurações" > "API"
4. Copie suas credenciais:
   - **API Token**: Token de acesso à API
   - **Safe Key**: Chave de segurança

### 2. Configurar Variáveis de Ambiente

#### Para Desenvolvimento Local:
Crie um arquivo `.env` na raiz do projeto:

```env
# Configurações D4Sign
D4SIGN_API_URL=https://api.d4sign.com.br
D4SIGN_API_TOKEN=seu_token_aqui
D4SIGN_SAFE_KEY=sua_safe_key_aqui

# Configurações de Email (já existentes)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=seu_email@gmail.com
EMAIL_PASSWORD=sua_senha_app
```

#### Para Deploy no Railway:
1. Acesse o dashboard do Railway
2. Vá para "Variables"
3. Adicione as variáveis:
   - `D4SIGN_API_URL`: `https://api.d4sign.com.br`
   - `D4SIGN_API_TOKEN`: Seu token da API
   - `D4SIGN_SAFE_KEY`: Sua safe key

## 🚀 Como Usar o Sistema de Assinatura

### 1. Enviar Contrato para Assinatura

1. Acesse a lista de contratos
2. Clique em "Enviar para Assinatura" no contrato desejado
3. O sistema irá:
   - Gerar o PDF do contrato
   - Fazer upload para o D4Sign
   - Criar um envelope de assinatura
   - Enviar email para o inquilino

### 2. Verificar Status da Assinatura

1. Na lista de contratos, clique em "Verificar Status"
2. O sistema consultará o D4Sign e atualizará o status

### 3. Baixar Contrato Assinado

1. Após a assinatura, clique em "Visualizar Contrato Assinado"
2. O sistema baixará o PDF assinado do D4Sign

## 📊 Status da Assinatura

- **Não Enviado**: Contrato ainda não foi enviado para assinatura
- **Enviado**: Contrato enviado, aguardando assinatura
- **Assinado**: Contrato foi assinado pelo inquilino
- **Cancelado**: Processo de assinatura foi cancelado

## 🔄 Fluxo Completo

### 1. Criação do Contrato
```
Cadastrar Contrato → Gerar PDF → Enviar para D4Sign → Email para Inquilino
```

### 2. Processo de Assinatura
```
Inquilino recebe email → Acessa link → Assina documento → D4Sign notifica sistema
```

### 3. Finalização
```
Sistema verifica status → Baixa PDF assinado → Salva no sistema
```

## 🛠️ Testando o Sistema

### 1. Teste Local
```bash
# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
# (criar arquivo .env)

# Executar sistema
python run.py
```

### 2. Teste de Assinatura
1. Crie um contrato de teste
2. Use o email `vanedijuliao@gmail.com` para assinatura
3. Verifique se o email é recebido
4. Teste o processo de assinatura

## 📧 Configuração de Email

O sistema usa o email configurado para enviar notificações sobre assinaturas:

- **Email de Envio**: Configurado nas variáveis de ambiente
- **Templates**: Personalizados para cada tipo de notificação
- **Logs**: Todas as notificações são registradas

## 🔍 Monitoramento

### Logs do Sistema
- Verifique os logs para acompanhar o processo
- Erros são registrados com detalhes
- Status das assinaturas é atualizado automaticamente

### Dashboard
- Acesse `/dashboard` para ver estatísticas
- Status dos contratos é exibido em tempo real
- Notificações automáticas são enviadas

## 🚨 Solução de Problemas

### Erro: "D4Sign não está configurado"
- Verifique se as variáveis de ambiente estão configuradas
- Confirme se o token e safe key estão corretos

### Erro: "Falha no upload do documento"
- Verifique a conexão com a internet
- Confirme se o arquivo PDF existe
- Verifique as permissões do arquivo

### Email não recebido
- Verifique a configuração de email
- Confirme se o email do inquilino está correto
- Verifique a pasta de spam

## 📞 Suporte

Para problemas com o D4Sign:
- Documentação: [https://docs.d4sign.com.br](https://docs.d4sign.com.br)
- Suporte: [https://www.d4sign.com.br/suporte](https://www.d4sign.com.br/suporte)

Para problemas com o sistema:
- Verifique os logs do sistema
- Confirme as configurações de ambiente
- Teste a conectividade com a API

## 🔄 Próximos Passos

1. **Configurar as variáveis de ambiente**
2. **Testar o envio de um contrato**
3. **Verificar o recebimento do email**
4. **Testar o processo de assinatura**
5. **Monitorar os logs do sistema**

---

**Nota**: Este sistema mantém os contratos como PDF conforme sua preferência, garantindo que todos os documentos sejam preservados no formato original. 