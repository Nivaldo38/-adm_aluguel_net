"""
Configurações para Produção (Railway)
"""

import os

# Configurações do Railway
RAILWAY_ENVIRONMENT = os.getenv('RAILWAY_ENVIRONMENT', 'production')

# Configurações do banco de dados
if RAILWAY_ENVIRONMENT == 'production':
    # Usar PostgreSQL no Railway
    DATABASE_URL = os.getenv('DATABASE_URL')
    if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
else:
    # Usar SQLite local
    DATABASE_URL = 'sqlite:///adm_aluguel.db'

# Configurações de email
EMAIL_CONFIG = {
    'SMTP_SERVER': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
    'SMTP_PORT': int(os.getenv('SMTP_PORT', '587')),
    'EMAIL_USER': os.getenv('EMAIL_USER', ''),
    'EMAIL_PASSWORD': os.getenv('EMAIL_PASSWORD', ''),
}

# Configurações D4Sign
D4SIGN_CONFIG = {
    'TOKEN_API': os.getenv('D4SIGN_TOKEN_API', ''),
    'CRYPT_KEY': os.getenv('D4SIGN_CRYPT_KEY', ''),
    'ENVIRONMENT': os.getenv('D4SIGN_ENVIRONMENT', 'sandbox'),
}

# Configurações de segurança
SECRET_KEY = os.getenv('SECRET_KEY', 'chave_secreta_segura_producao')

# Configurações de backup
BACKUP_CONFIG = {
    'ENABLED': os.getenv('BACKUP_ENABLED', 'true').lower() == 'true',
    'MAX_BACKUPS': int(os.getenv('MAX_BACKUPS', '10')),
}

print(f"🔧 Configuração para ambiente: {RAILWAY_ENVIRONMENT}")
print(f"📊 Database URL: {DATABASE_URL[:50]}..." if DATABASE_URL else "❌ Database URL não configurada")
print(f"📧 Email configurado: {'Sim' if EMAIL_CONFIG['EMAIL_USER'] else 'Não'}")
print(f"🔐 D4Sign configurado: {'Sim' if D4SIGN_CONFIG['TOKEN_API'] else 'Não'}") 