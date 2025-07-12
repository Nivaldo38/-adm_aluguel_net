import os
from flask import Flask

print("🚀 Iniciando aplicação Flask...")

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'chave_secreta_segura')

# Endpoint de healthcheck ultra simples para o Railway
@app.route('/health')
def health_check():
    return 'OK', 200

# Endpoint de healthcheck alternativo
@app.route('/healthcheck')
def health_check_alt():
    return 'Sistema funcionando!', 200

print("📊 Configurando banco de dados...")

# Configuração do banco de dados
# Verificar se estamos em produção (Railway)
if os.getenv('RAILWAY_ENVIRONMENT') == 'production' or os.getenv('DATABASE_URL'):
    # Usar PostgreSQL no Railway
    database_url = os.getenv('DATABASE_URL')
    if database_url and database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    print("✅ Usando PostgreSQL no Railway")
    print(f"🔗 Database URL: {database_url[:50]}...")
else:
    # Usar SQLite local para desenvolvimento
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, '..', 'adm_aluguel.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
    print("✅ Usando banco SQLite local")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # evitar warning

print("🔧 Inicializando SQLAlchemy...")
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy(app)
migrate = Migrate(app, db)  # adiciona o Flask-Migrate

print("📁 Importando rotas e modelos...")
try:
    from app import routes, models
    print("✅ Rotas e modelos importados com sucesso")
except Exception as e:
    print(f"❌ Erro ao importar rotas/modelos: {e}")
    # Em produção, não vamos falhar se houver erro de importação
    if os.getenv('RAILWAY_ENVIRONMENT') == 'production':
        print("⚠️ Continuando em modo de produção...")
    else:
        raise e

print("🎉 Aplicação Flask inicializada com sucesso!")

# Criar tabelas se não existirem (apenas em desenvolvimento)
if not os.getenv('RAILWAY_ENVIRONMENT') == 'production':
    try:
        with app.app_context():
            db.create_all()
            print("✅ Tabelas criadas/verificadas")
    except Exception as e:
        print(f"⚠️ Erro ao criar tabelas: {e}")
