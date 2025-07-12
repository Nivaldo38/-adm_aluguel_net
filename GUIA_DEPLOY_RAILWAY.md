# 🚀 Guia de Deploy no Railway

## 📋 Pré-requisitos

1. **Conta no Railway**
   - Acesse: https://railway.app/
   - Crie uma conta gratuita

2. **Node.js e NPM**
   - Instale: https://nodejs.org/
   - Verifique: `node --version` e `npm --version`

3. **Git**
   - Instale: https://git-scm.com/
   - Configure: `git config --global user.name 'Seu Nome'`

## 🔧 Instalação do Railway CLI

```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Fazer login
railway login
```

## 🚀 Deploy Automático

### Opção 1: Script Automático
```bash
python deploy_railway.py
```

### Opção 2: Deploy Manual

1. **Inicializar Git (se necessário)**
```bash
git init
git add .
git commit -m "Primeiro commit"
```

2. **Fazer deploy**
```bash
railway deploy
```

## ⚙️ Configuração no Railway

### 1. Acessar o Dashboard
- Vá para: https://railway.app/dashboard
- Selecione seu projeto

### 2. Configurar Variáveis de Ambiente

No Railway Dashboard, vá em **Variables** e adicione:

#### **Obrigatórias:**
```
SECRET_KEY=sua_chave_secreta_muito_segura_aqui
RAILWAY_ENVIRONMENT=production
```

#### **Opcionais (Email):**
```
EMAIL_USER=seu@email.com
EMAIL_PASSWORD=sua_senha_de_app
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

#### **Opcionais (D4Sign):**
```
D4SIGN_TOKEN_API=sua_token_api
D4SIGN_CRYPT_KEY=sua_crypt_key
D4SIGN_ENVIRONMENT=sandbox
```

### 3. Configurar Banco de Dados

1. No Railway Dashboard, clique em **New**
2. Selecione **Database** → **PostgreSQL**
3. O Railway criará automaticamente a variável `DATABASE_URL`

### 4. Executar Migrações

Após o deploy, execute as migrações:

```bash
# Via Railway CLI
railway run flask db upgrade

# Ou via Railway Dashboard → Deployments → View Logs
```

## 🔍 Verificação do Deploy

### 1. Verificar Logs
```bash
railway logs
```

### 2. Verificar Status
```bash
railway status
```

### 3. Acessar a Aplicação
- No Railway Dashboard, clique em **Deployments**
- Clique na URL gerada (ex: https://seu-projeto.railway.app)

## 🛠️ Troubleshooting

### Problema: Erro de banco de dados
```bash
# Verificar se o banco foi criado
railway run flask db upgrade
```

### Problema: Erro de dependências
```bash
# Verificar requirements.txt
railway run pip install -r requirements.txt
```

### Problema: Erro de porta
- O Railway configura automaticamente a porta
- Verifique se o `gunicorn.conf.py` está correto

## 📊 Monitoramento

### 1. Logs em Tempo Real
```bash
railway logs --follow
```

### 2. Métricas
- No Railway Dashboard → **Metrics**
- Monitore CPU, memória e requisições

### 3. Health Check
- Acesse: `https://seu-projeto.railway.app/health`
- Deve retornar: `OK`

## 🔄 Atualizações

### Deploy de Atualizações
```bash
# Fazer alterações no código
git add .
git commit -m "Atualização"

# Deploy automático
railway deploy
```

### Rollback
- No Railway Dashboard → **Deployments**
- Clique em **Revert** no deployment anterior

## 💰 Custos

### Plano Gratuito
- ✅ 500 horas/mês
- ✅ 1GB RAM
- ✅ 1GB storage
- ✅ Domínio personalizado

### Plano Pago
- $5/mês para mais recursos
- Mais horas, RAM e storage

## 🔐 Segurança

### 1. Variáveis de Ambiente
- Nunca commite senhas no código
- Use sempre variáveis de ambiente

### 2. HTTPS
- Automático no Railway
- Certificado SSL gratuito

### 3. Backup
- Configure backup automático
- Use o sistema de backup do Railway

## 📱 Domínio Personalizado

1. No Railway Dashboard → **Settings**
2. **Domains** → **Add Domain**
3. Configure DNS conforme instruções

## 🎯 Próximos Passos

1. ✅ Deploy no Railway
2. ✅ Configurar variáveis de ambiente
3. ✅ Testar todas as funcionalidades
4. ✅ Configurar domínio personalizado
5. ✅ Configurar backup automático
6. ✅ Monitorar performance

---

**🎉 Seu sistema estará online e acessível de qualquer lugar!** 