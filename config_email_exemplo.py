"""
Configuração de E-mail - Exemplo
Copie este arquivo para .env e configure suas credenciais
"""

# Configurações de E-mail
# Descomente e configure as linhas abaixo para usar e-mail real

# SMTP_SERVER=smtp.gmail.com
# SMTP_PORT=587
# EMAIL_USER=seu_email@gmail.com
# EMAIL_PASSWORD=sua_senha_de_app

"""
INSTRUÇÕES PARA CONFIGURAR E-MAIL REAL:

1. Para Gmail:
   - Ative a verificação em duas etapas
   - Gere uma senha de app: https://myaccount.google.com/apppasswords
   - Use a senha de app no EMAIL_PASSWORD

2. Para Outlook/Hotmail:
   - SMTP_SERVER=smtp-mail.outlook.com
   - SMTP_PORT=587

3. Para Yahoo:
   - SMTP_SERVER=smtp.mail.yahoo.com
   - SMTP_PORT=587

4. Para outros provedores:
   - Consulte a documentação do seu provedor de e-mail

EXEMPLO DE CONFIGURAÇÃO:
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=seu_email@gmail.com
EMAIL_PASSWORD=abcd efgh ijkl mnop

NOTA: Sem essas configurações, o sistema usa modo simulado
(apenas exibe as mensagens no console)
""" 