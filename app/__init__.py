import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'chave_secreta_segura'

# Configuração do banco de dados
if os.environ.get('DATABASE_URL'):
    # Para produção (Railway)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
else:
    # Para desenvolvimento local
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, '..', 'adm_aluguel.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # evitar warning

db = SQLAlchemy(app)
migrate = Migrate(app, db)  # adiciona o Flask-Migrate

from app import routes, models
