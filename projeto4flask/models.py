from projeto4flask import database, login_manager
from datetime import datetime
from flask_login import UserMixin    #parametro para passar para a classe do Usuario


#--Definir funcao para ser utilizada no gerenciamento do login
@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))


class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    foto_perfil = database.Column(database.String, nullable=False, default='default.jpg')
    cursos = database.Column(database.String, nullable=False, default="Não Informado")
    posts = database.relationship('Post', backref='autor', lazy=True)

    #Metodo para contar posts do usuario
    def contar_posts(self):
        return len(self.posts)

class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    corpo =  database.Column(database.Text, nullable=False)
    # "datetime.utcnow" em formato de funcao e nao como resultado da funcao ou seja, com os
    # parentesis no final. Exemplo datetime.utcnow() -> dessa forma nao executa a funcao para
    # descobrir a data e hora atual antes de gravar o registro do Post na tabela
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    # note que, para construcao da chave estrangeira, o nome da classe tem que estar em letra minuscula
    # esse argumento Foreignkey é argumento de posicao, tem que ser sempre o segundo
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
