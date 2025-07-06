# 🏠 Sistema de Administração de Aluguel por Temporada

Sistema completo para gerenciamento de locações por temporada, desenvolvido em Flask com SQLite.

## ✨ Funcionalidades Implementadas

### ✅ **Gestão de Locais e Unidades**
- Cadastro e edição de locais
- Cadastro de unidades por local
- Controle de status das unidades (livre, ocupada, manutenção)
- Filtros dinâmicos

### ✅ **Gestão de Inquilinos**
- Cadastro completo com validações (CPF, email, telefone)
- Validação de inquilino único por unidade
- Edição e exclusão de inquilinos

### ✅ **Gestão de Contratos**
- Cadastro de contratos com dados completos
- Geração automática de PDF do contrato
- Validações e controle de status
- Filtros por local e situação

### ✅ **Gestão de Boletos**
- Geração individual e em lote
- Controle de status (pendente, pago, vencido, cancelado)
- Códigos de barras simulados
- Estatísticas e relatórios

### ✅ **Assinatura Digital DS4** 🆕
- Integração com DocuSign (DS4)
- Envio automático para assinatura
- Acompanhamento de status
- Download de contratos assinados
- Assinatura automática do locador
- Email automático para inquilino

## 🚀 Como Usar

### 1. **Instalação**
```bash
# Clone o repositório
git clone [url-do-repositorio]
cd adm_aluguel_net

# Instale as dependências
pip install -r requirements.txt

# Configure o banco de dados
flask db upgrade
```

### 2. **Configuração DS4 (Assinatura Digital)**

Para usar a assinatura digital, siga estes passos:

#### A. Criar conta no DS4
1. Acesse https://www.docusign.com.br/
2. Crie uma conta gratuita
3. Vá para Settings > API and Keys
4. Crie uma nova Integration Key

#### B. Gerar chaves RSA
```bash
# Gerar par de chaves (Linux/Mac)
openssl genrsa -out private_key.pem 2048
openssl rsa -in private_key.pem -pubout -out public_key.pem

# No Windows, use o Git Bash ou WSL
```

#### C. Configurar variáveis de ambiente

**Windows (PowerShell):**
```powershell
$env:DS4_ACCOUNT_ID="sua_account_id"
$env:DS4_INTEGRATION_KEY="sua_integration_key"
$env:DS4_USER_ID="seu_user_id"
$env:DS4_PRIVATE_KEY_PATH="C:\caminho\para\private_key.pem"
```

**Linux/Mac:**
```bash
export DS4_ACCOUNT_ID="sua_account_id"
export DS4_INTEGRATION_KEY="sua_integration_key"
export DS4_USER_ID="seu_user_id"
export DS4_PRIVATE_KEY_PATH="/caminho/para/private_key.pem"
```

#### D. Verificar configuração
```bash
python config_ds4.py
```

### 3. **Executar o Sistema**
```bash
python run.py
```

Acesse: http://127.0.0.1:5000

## 📋 Fluxo de Assinatura Digital

### **Passo a Passo:**

1. **Cadastrar Contrato**
   - Preencha todos os dados do contrato
   - O PDF é gerado automaticamente

2. **Enviar para Assinatura**
   - Clique em "✍️ Enviar para Assinatura"
   - O sistema envia o PDF para o DS4
   - O locador assina automaticamente
   - Email é enviado para o inquilino

3. **Acompanhar Status**
   - Clique em "📊 Verificar Status"
   - Veja o progresso da assinatura

4. **Download do Contrato Assinado**
   - Quando assinado, clique em "✅ Ver Assinado"
   - Baixe o PDF com todas as assinaturas

## 🎯 Próximos Passos

### **Fase 1 - Implementado ✅**
- [x] Gestão básica (locais, unidades, inquilinos)
- [x] Contratos com PDF automático
- [x] Boletos e pagamentos
- [x] Assinatura digital DS4

### **Fase 2 - Planejado**
- [ ] Área do inquilino (login)
- [ ] Notificações por email
- [ ] Relatórios avançados
- [ ] Dashboard com gráficos
- [ ] Backup automático

### **Fase 3 - Futuro**
- [ ] App mobile
- [ ] Integração com sistemas de pagamento
- [ ] API REST para integrações
- [ ] Múltiplos usuários/permissões

## 🔧 Estrutura do Projeto

```
adm_aluguel_net/
├── app/
│   ├── __init__.py
│   ├── models.py          # Modelos do banco
│   ├── routes.py          # Rotas da aplicação
│   ├── contract_generator.py  # Gerador de PDFs
│   ├── ds4_integration.py     # Integração DS4
│   └── templates/         # Templates HTML
├── contracts/            # PDFs gerados
├── migrations/           # Migrações do banco
├── config_ds4.py        # Configuração DS4
├── requirements.txt      # Dependências
└── run.py              # Arquivo principal
```

## 📊 Tecnologias Utilizadas

- **Backend:** Flask, SQLAlchemy, SQLite
- **Frontend:** HTML, CSS, JavaScript
- **PDF:** ReportLab
- **Assinatura Digital:** DocuSign API
- **Validações:** Regex, validações customizadas

## 🛠️ Comandos Úteis

```bash
# Criar nova migração
flask db migrate -m "descrição"

# Aplicar migrações
flask db upgrade

# Verificar configuração DS4
python config_ds4.py

# Regenerar todos os contratos
python regenerar_contratos_em_lote.py
```

## 📞 Suporte

Para dúvidas sobre:
- **Configuração DS4:** Consulte `config_ds4.py`
- **Assinatura Digital:** Verifique as variáveis de ambiente
- **Geração de PDFs:** Verifique a pasta `contracts/`

## 🚀 Deploy

Para produção:
1. Configure as variáveis DS4 para produção
2. Use um servidor WSGI (Gunicorn, uWSGI)
3. Configure um banco PostgreSQL
4. Configure HTTPS
5. Implemente backup automático

---

**Desenvolvido com ❤️ para facilitar a gestão de aluguel por temporada!** 