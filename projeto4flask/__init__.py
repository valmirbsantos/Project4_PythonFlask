from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


#------------------ criar instancia do app Flask
appSite = Flask(__name__)

#----------------- definicao de chave (token) para segurança de formularios
# chave-token gerada pela funcao secrets.token_hex(16) do python
# será usada no formulario com o metodo csrf.token. Ex.: form_criarconta.csrf_token
appSite.config['SECRET_KEY'] = '3f0bdc99e942ccb11f7ca8658b982f0b'

#---------------- configurar o acesso ao banco de dados
appSite.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projeto4.db'
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

#deve ser importado nessa posicao pois as rotas precisam do appSite criado acima
from projeto4flask import routes

