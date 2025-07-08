# 🚀 Guia Rápido - Deploy Railway

## ✅ Status Atual
O sistema está **pronto para deploy**! Só falta configurar as variáveis de ambiente no Railway.

## 🔧 Variáveis Obrigatórias para o Railway

### 1. Acesse o Railway
- Vá para: https://railway.app
- Entre no seu projeto
- Clique em **"Variables"**

### 2. Adicione estas variáveis:

#### **OBRIGATÓRIAS:**
```env
SECRET_KEY=chave_secreta_muito_segura_aqui_123456789
```

#### **OPCIONAIS (para funcionalidades completas):**
```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=seu_email@gmail.com
EMAIL_PASSWORD=sua_senha_app

D4SIGN_API_URL=https://api.d4sign.com.br
D4SIGN_API_TOKEN=seu_token_aqui
D4SIGN_SAFE_KEY=sua_safe_key_aqui
```

### 3. O Railway criará automaticamente:
- `DATABASE_URL` (PostgreSQL)
- `PORT` (porta do servidor)

## 🚀 Como Fazer o Deploy

### Passo 1: Configure as Variáveis
1. No Railway, vá em "Variables"
2. Adicione pelo menos a `SECRET_KEY`
3. As outras são opcionais

### Passo 2: Faça Deploy
1. Clique em "Deploy" no Railway
2. Aguarde o deploy completar
3. Copie a URL gerada

### Passo 3: Teste
1. Acesse a URL do Railway
2. O sistema deve estar funcionando!

## 🔍 Se Ainda Não Funcionar

### Verificar Logs:
1. No Railway, vá em "Deployments"
2. Clique no último deploy
3. Veja os logs para identificar erros

### Problemas Comuns:
- **Workers saindo**: Falta `SECRET_KEY`
- **Erro de banco**: `DATABASE_URL` não configurado
- **App não inicia**: Verificar logs completos

## 📱 URLs Importantes

Após o deploy, você terá acesso a:
- **Web**: `https://seu-app.railway.app`
- **Mobile**: `https://seu-app.railway.app/mobile/`

## 🎯 Próximos Passos

1. **Configure as variáveis** (pelo menos SECRET_KEY)
2. **Faça deploy** no Railway
3. **Teste a URL** gerada
4. **Configure email** (opcional) para notificações
5. **Configure D4Sign** (opcional) para assinaturas

---

## 💡 Dicas Importantes

- **SECRET_KEY é obrigatória** - sem ela o app não inicia
- **Email é opcional** - sistema funciona sem notificações
- **D4Sign é opcional** - sistema funciona sem assinaturas
- **Banco PostgreSQL** é criado automaticamente pelo Railway

## 🆘 Suporte

Se ainda não funcionar:
1. Verifique os logs do Railway
2. Confirme se `SECRET_KEY` está configurada
3. Aguarde o deploy completar (pode demorar alguns minutos)

---

**🎉 Com essas configurações, seu sistema estará online em minutos!** 