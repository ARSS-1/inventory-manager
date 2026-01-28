import os
from flask import Flask
from app.database import db
from app.models import User, Product
from app.controllers import product_bp, user_bp
from flask_jwt_extended import JWTManager

# INSTANCIA A CLASSE DO FRAMEWORK
app = Flask(__name__)

# SELECIONA A PASTA RAIZ
basedir = os.path.abspath(os.path.dirname(__file__))
root_dir = os.path.dirname(basedir)

# CONFIGURACAO DO DB. ELE É CRIADO NA PASTA RAIZ.
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"sqlite:///{os.path.join(root_dir, 'inventory.db')}"
)

# CONFIGURACAO DO GERENCIADOR DE TOKEN
app.config["JWT_SECRET_KEY"] = "admin"

# CONECTA O SQLALCHEMY E O FLASK
db.init_app(app)

# CONECTA O GERENCIADOR DE TOKEN A APLICACAO
jwt = JWTManager(app)

# REGISTO DE BLUEPRINTS
app.register_blueprint(product_bp)
app.register_blueprint(user_bp)

# CRIA AS TABELAS DO DB, SE NÃO EXISTIREM
with app.app_context():
    db.create_all()
