# 🚀 Guia de Deploy no Railway

## ✅ Status Atual

O sistema está **pronto para deploy** no Railway! Todas as correções foram feitas:

- ✅ Erro do scheduler corrigido
- ✅ Sistema de backup funcionando
- ✅ D4Sign configurado (aguardando credenciais)
- ✅ Sistema de notificações ativo
- ✅ Interface moderna e responsiva

## 📋 Pré-requisitos

1. **Conta no Railway**: [https://railway.app](https://railway.app)
2. **Conta no GitHub**: Para conectar o repositório
3. **Credenciais de Email**: Para notificações

## 🔧 Configuração no Railway

### 1. Conectar Repositório

1. Acesse [https://railway.app](https://railway.app)
2. Clique em "New Project"
3. Selecione "Deploy from GitHub repo"
4. Conecte sua conta GitHub
5. Selecione o repositório `adm_aluguel_net`

### 2. Configurar Variáveis de Ambiente

No Railway, vá para "Variables" e adicione:

```env
# Configurações de Email (OBRIGATÓRIO)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=seu_email@gmail.com
EMAIL_PASSWORD=sua_senha_app

# Configurações D4Sign (OPCIONAL - configurar depois)
D4SIGN_API_URL=https://api.d4sign.com.br
D4SIGN_API_TOKEN=seu_token_aqui
D4SIGN_SAFE_KEY=sua_safe_key_aqui

# Configurações do Sistema
FLASK_ENV=production
SECRET_KEY=sua_chave_secreta_aqui
```

### 3. Configurar Domínio

1. Vá para "Settings" no Railway
2. Em "Domains", clique em "Generate Domain"
3. Copie o domínio gerado (ex: `adm-aluguel-net-production.up.railway.app`)

## 🚀 Deploy Automático

O Railway fará deploy automático sempre que você fizer push para o repositório.

### Arquivos de Configuração

- ✅ `requirements.txt` - Dependências Python
- ✅ `Procfile` - Configuração do Railway
- ✅ `runtime.txt` - Versão do Python
- ✅ `gunicorn.conf.py` - Configuração do servidor

## 📊 Monitoramento

### 1. Logs do Railway

- Acesse "Deployments" no Railway
- Clique em "View Logs" para ver os logs em tempo real
- Monitore erros e avisos

### 2. Métricas do Sistema

- **Uptime**: Verificado automaticamente
- **Performance**: Logs de resposta
- **Erros**: Capturados nos logs

## 🔍 Testando o Deploy

### 1. Verificar Funcionalidades

Após o deploy, teste:

- ✅ Página inicial carrega
- ✅ Login funciona
- ✅ Cadastro de locais/inquilinos
- ✅ Geração de contratos
- ✅ Sistema de boletos
- ✅ Backup automático

### 2. Testar Notificações

1. Configure email no Railway
2. Teste envio de notificação
3. Verifique logs de email

## 🛠️ Solução de Problemas

### Erro: "Module not found"
- Verifique se todas as dependências estão no `requirements.txt`
- Execute `pip install -r requirements.txt` localmente

### Erro: "Database not found"
- O Railway criará o banco automaticamente
- Verifique se as migrações estão aplicadas

### Erro: "Email not working"
- Verifique as variáveis de ambiente
- Teste com Gmail App Password

### Erro: "D4Sign not configured"
- Normal, aguarde configuração das credenciais
- Sistema funciona sem D4Sign

## 📈 Próximos Passos

### 1. Pós-Deploy
- [ ] Testar todas as funcionalidades
- [ ] Configurar domínio personalizado (opcional)
- [ ] Configurar backup automático

### 2. Configuração D4Sign
- [ ] Obter credenciais da API
- [ ] Configurar variáveis no Railway
- [ ] Testar assinatura digital

### 3. Monitoramento
- [ ] Configurar alertas
- [ ] Monitorar performance
- [ ] Backup regular

## 🎯 Vantagens do Railway

- ✅ **Deploy Automático**: Push para GitHub = deploy automático
- ✅ **SSL Gratuito**: Certificado HTTPS automático
- ✅ **Escalabilidade**: Ajusta recursos automaticamente
- ✅ **Logs Detalhados**: Monitoramento completo
- ✅ **Variáveis de Ambiente**: Configuração segura
- ✅ **Domínio Personalizado**: Suporte a domínios próprios

## 📞 Suporte

- **Railway**: [https://railway.app/support](https://railway.app/support)
- **Documentação**: [https://docs.railway.app](https://docs.railway.app)
- **Status**: [https://status.railway.app](https://status.railway.app)

---

**🎉 Sistema pronto para produção!**

O deploy no Railway é simples e rápido. Após configurar as variáveis de ambiente, o sistema estará funcionando em produção com todas as funcionalidades ativas. 