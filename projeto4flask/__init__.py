from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

#------------------ criar instancia do app Flask
appSite = Flask(__name__)

#----------------- definicao de chave (token) para segurança de formularios
# chave-token gerada pela funcao secrets.token_hex(16) do python
# será usada no formulario com o metodo csrf.token. Ex.: form_criarconta.csrf_token
appSite.config['SECRET_KEY'] = '3f0bdc99e942ccb11f7ca8658b982f0b'

#---------------- configurar o acesso ao banco de dados remoto (Railway) - nao funcionou, nao encontra a variavel DATABASE_URL
# if os.getenv("DATABASE_URL"):
#     appSite.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
# # ---------------- configurar o acesso ao banco de dados local
# else:
#     appSite.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projeto4.db'
print('-='*30)
print(os.environ.get('DATABASE_URL'))
print('.='*30)
print(os.environ)
print('-='*30)
appSite.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:pVnBnqbIUBkVBSFTKywutHTEwBXnytAE@postgres.railway.internal:5432/railway"

#para criar o banco de dados
database = SQLAlchemy(appSite)



#----------------- cria instancia do bcrypt para usar no aplicativo
# será aplicado no routes "criarconta" para criacao do usuario e no "login" para validar senha
bcrypt = Bcrypt(appSite)

#----------------- cria instancia do login_manager para controle de login usuario ---
login_manager = LoginManager(appSite)
#parametro para indicar a pagina (do routes.html) que o usuario será direcionado quando exigido login_required
login_manager.login_view = 'login'
#categoria para a mensagem = pode ser customizada com login_manager.login_message
login_manager.login_message_category = 'alert-info'

##----- verificar se o database existe. Se nao existir, criar o DB com todas as
#        tabelas do models.py
# import sqlalchemy
# from projeto4flask import models
# engine = sqlalchemy.create_engine(appSite.config['SQLALCHEMY_DATABASE_URI'])
# inspector = sqlalchemy.inspect(engine)
# ## ------verifica se existe a tabela de usuarios no banco de dados
# if not inspector.has_table('usuario'):
#     with appSite.app_context():
#         database.drop_all()
#         database.create_all()
#         print('Banco de dados criado com sucesso')
# else:
#     print('Base de Dados já existe')

#deve ser importado nessa posicao pois as rotas precisam do appSite criado acima
from projeto4flask import routes
