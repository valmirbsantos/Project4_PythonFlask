# # todos os comandos de bancos de dados devem estar dentro do contexto da aplicacao
from projeto4flask import database, appSite
from projeto4flask.models import Usuario

#
# ##--------- Criar banco de dados -------
# with appSite.app_context():
#     database.create_all()

# #--------- Gravar informacoes no banco de dados -------
# with appSite.app_context():
#     usuario = Usuario(
#         username='Valmir',
#         email='valmir.bs@gmail.com',
#         senha='123456'
#     )
#     usuario2 = Usuario(
#         username='Eric',
#         email='eric@gmail.com',
#         senha='123456'
#     )
#     database.session.add(usuario)
#     database.session.add(usuario2)
#     database.session.commit()

# #--------- Ler informacoes do banco de dados -------
with appSite.app_context():
    meus_usuarios = Usuario.query.all()
    primeiro_usuario = Usuario.query.first()
    usuario_selecionado = Usuario.query.filter_by(id=1).first()
    print(meus_usuarios)
    for usuario in meus_usuarios:
        print(f'usuario [{usuario.username}] - email [{usuario.email}] - senha [{usuario.senha}] - posts {usuario.posts}')
        print(f'Cursos [{usuario.cursos}]')
        print(f'Posts')
        for post in usuario.posts:
            print(f'Titulo: {post.titulo} - Corpo: {post.corpo}')
        print('-='*80)

# #--------- Criar um post no banco de dados -------
# with appSite.app_context():
#     meu_post = Post(
#         id_usuario=1,
#         titulo='Primeiro Post Teste',
#         corpo='Post inserido pelo programa teste.py'
#     )
#     database.session.add(meu_post)
#     database.session.commit()
#
# with appSite.app_context():
#     meus_posts = Post.query.all()
#     for post in meus_posts:
#         print(post.titulo)
#         print(post.autor.username)


# #--------- Recriar o banco de dados vazio -------
# with appSite.app_context():
#     database.drop_all()
#     database.create_all()