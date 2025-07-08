# Sistema de Notificações Automáticas

## 📋 Visão Geral

O sistema de notificações automáticas foi implementado para enviar alertas e lembretes importantes aos inquilinos e administradores do sistema de aluguel.

## 🔔 Funcionalidades Implementadas

### 1. **Notificações de Boletos Vencendo**
- **Quando**: 3 dias antes do vencimento
- **Para**: Inquilinos com email cadastrado
- **Conteúdo**: Detalhes do boleto, valor, data de vencimento
- **Template**: Email HTML responsivo com design moderno

### 2. **Notificações de Contratos Vencendo**
- **Quando**: 30 dias antes do vencimento
- **Para**: Inquilinos com email cadastrado
- **Conteúdo**: Detalhes do contrato, datas, valor do aluguel
- **Template**: Email HTML com informações de renovação

### 3. **Alertas de Manutenção**
- **Quando**: Unidades em manutenção há mais de 7 dias
- **Para**: Administrador do sistema
- **Conteúdo**: Lista de unidades afetadas
- **Template**: Email de alerta com ações necessárias

### 4. **Relatórios Mensais**
- **Quando**: Primeiro dia do mês
- **Para**: Administrador
- **Conteúdo**: Resumo financeiro e estatísticas

## 🛠️ Componentes do Sistema

### 1. **NotificationService** (`app/notification_service.py`)
```python
# Principais métodos:
- check_boletos_vencendo()
- check_contratos_vencendo()
- check_unidades_manutencao()
- send_boleto_vencimento_notification()
- send_contrato_vencimento_notification()
- send_manutencao_notification()
- log_notification()
- get_notification_stats()
```

### 2. **Agendador** (`scheduler.py`)
```python
# Funcionalidades:
- Verificações diárias às 8:00
- Verificações semanais aos domingos às 9:00
- Verificações mensais no primeiro dia do mês às 10:00
- Execução em background
```

### 3. **Interface Web** (`app/templates/notificacoes.html`)
- Dashboard de estatísticas
- Configurações de notificação
- Log de notificações
- Botões para teste manual

## 📊 Estatísticas e Logs

### Log de Notificações
- **Arquivo**: `notifications/notification_log.json`
- **Campos**: tipo, item_id, email, success, timestamp, error_message
- **Limite**: Últimos 1000 registros

### Estatísticas Disponíveis
- Total de notificações
- Sucessos vs falhas
- Distribuição por tipo
- Histórico de envios

## ⚙️ Configuração

### 1. **Dependências**
```bash
pip install schedule==1.2.0
```

### 2. **Variáveis de Ambiente**
```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=seu-email@gmail.com
EMAIL_PASSWORD=sua-senha-app
```

### 3. **Integração com Flask**
```python
# Em run.py
from scheduler import run_scheduler_in_background

if __name__ == '__main__':
    run_scheduler_in_background()
    app.run(host='0.0.0.0', port=5000)
```

## 🧪 Testes

### Script de Teste (`testar_notificacoes.py`)
```bash
python testar_notificacoes.py
```

**Funcionalidades do teste:**
- Cria dados de teste se necessário
- Testa envio de email
- Executa verificações automáticas
- Mostra estatísticas

## 🎨 Templates de Email

### 1. **Boletos Vencendo**
- Design responsivo
- Informações do boleto
- Alertas visuais por urgência
- Botões de ação

### 2. **Contratos Vencendo**
- Detalhes do contrato
- Informações de renovação
- Links para documentos

### 3. **Manutenção**
- Lista de unidades afetadas
- Alertas de ação necessária
- Status de manutenção

## 🔧 Rotas da API

### 1. **Página de Notificações**
```
GET /notificacoes
```

### 2. **Enviar Teste**
```
GET /enviar_notificacao_teste
```

### 3. **Executar Verificações**
```
GET /executar_verificacoes
```

## 📱 Interface do Usuário

### Dashboard de Notificações
- **Cards de estatísticas**: Total, sucessos, falhas, tipos
- **Configurações**: Switches para ativar/desativar tipos
- **Agendamento**: Informações sobre verificações automáticas
- **Log**: Visualização de histórico

### Menu de Navegação
- Link "Notificações" adicionado ao menu principal
- Ícone de sino para identificação visual

## 🚀 Deploy

### Railway
- O agendador é iniciado automaticamente com a aplicação
- Logs são preservados entre deploys
- Configurações via variáveis de ambiente

### Local
```bash
python run.py
```

## 📈 Monitoramento

### Logs do Sistema
- Todas as notificações são logadas
- Erros são capturados e registrados
- Estatísticas em tempo real

### Alertas de Erro
- Falhas de envio são registradas
- Emails sem cadastro são identificados
- Problemas de configuração são reportados

## 🔮 Próximas Melhorias

### 1. **Configurações Avançadas**
- Interface para configurar horários
- Personalização de templates
- Configuração de destinatários

### 2. **Notificações Push**
- Integração com web push
- Notificações em tempo real
- Alertas no navegador

### 3. **Relatórios Detalhados**
- Gráficos de performance
- Análise de taxa de abertura
- Métricas de engajamento

### 4. **Integração com WhatsApp**
- API do WhatsApp Business
- Notificações via WhatsApp
- Templates personalizados

## ✅ Status Atual

- ✅ Sistema básico implementado
- ✅ Templates de email criados
- ✅ Agendador funcionando
- ✅ Interface web implementada
- ✅ Logs e estatísticas funcionando
- ✅ Testes automatizados
- ✅ Integração com Flask
- ✅ Deploy no Railway

## 🎯 Benefícios

1. **Automatização**: Reduz trabalho manual
2. **Prevenção**: Evita vencimentos esquecidos
3. **Comunicação**: Melhora relacionamento com inquilinos
4. **Gestão**: Facilita administração
5. **Relatórios**: Fornece insights importantes

O sistema está pronto para uso em produção e pode ser expandido conforme necessário! 