# Plano de Regressão Limpa - Sistema de Aluguel

## Objetivo
Criar uma versão limpa e funcional do sistema, focando em:
- ✅ Layout moderno e responsivo
- ✅ Funcionalidades básicas (CRUD completo)
- ✅ Sistema estável para deploy
- ❌ Remover funcionalidades complexas temporariamente

## Funcionalidades a MANTER
- ✅ Dashboard moderno
- ✅ CRUD de Locais
- ✅ CRUD de Unidades  
- ✅ CRUD de Inquilinos
- ✅ CRUD de Contratos
- ✅ Geração básica de PDF (sem assinatura digital)
- ✅ Sistema de login para inquilinos
- ✅ Backup básico (sem agendamento)
- ✅ Interface mobile responsiva

## Funcionalidades a REMOVER/Simplificar
- ❌ DocuSign (DS4) - remover completamente
- ❌ Assinatura digital - remover
- ❌ Boletos com conexão real - simplificar
- ❌ Email automático - simplificar
- ❌ Agendamento de backups - remover
- ❌ Módulos problemáticos (PyPDF2, docusign-esign, schedule)

## Passos da Regressão

### 1. Limpar Dependências
- Remover módulos problemáticos do requirements.txt
- Manter apenas dependências essenciais
- Testar instalação limpa

### 2. Simplificar Código
- Remover imports de módulos problemáticos
- Simplificar geração de PDF (usar apenas reportlab)
- Remover funcionalidades de assinatura digital
- Simplificar sistema de boletos

### 3. Manter Layout Moderno
- Manter todos os templates modernos
- Manter CSS/JS responsivo
- Manter dashboard com estatísticas
- Manter interface mobile

### 4. Testar Funcionalidades Básicas
- Testar CRUD completo
- Testar geração de PDF simples
- Testar login de inquilinos
- Testar backup manual

### 5. Preparar para Deploy
- Configurar para Railway/Render
- Testar deploy
- Documentar funcionalidades

## Benefícios
- ✅ Sistema estável e confiável
- ✅ Deploy sem problemas
- ✅ Interface moderna mantida
- ✅ Base sólida para futuras melhorias
- ✅ Foco nas funcionalidades essenciais

## Próximos Passos
1. Executar script de limpeza
2. Testar funcionalidades básicas
3. Fazer deploy
4. Documentar sistema
5. Planejar melhorias futuras 