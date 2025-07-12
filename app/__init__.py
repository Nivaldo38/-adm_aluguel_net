import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

print("🚀 Iniciando aplicação Flask...")

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'chave_secreta_segura')

print("📊 Configurando banco de dados...")

# Configuração do banco de dados
# Forçar uso do banco local para desenvolvimento
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, '..', 'adm_aluguel.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
print("✅ Usando banco SQLite local")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # evitar warning

print("🔧 Inicializando SQLAlchemy...")
db = SQLAlchemy(app)
migrate = Migrate(app, db)  # adiciona o Flask-Migrate

# Endpoint de healthcheck para o Railway
@app.route('/health')
def health_check():
    return {'status': 'healthy'}, 200

print("📁 Importando rotas e modelos...")
try:
    from app import routes, models
    print("✅ Rotas e modelos importados com sucesso")
except Exception as e:
    print(f"❌ Erro ao importar rotas/modelos: {e}")
    raise e

print("🎉 Aplicação Flask inicializada com sucesso!")
