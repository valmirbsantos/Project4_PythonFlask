from flask import render_template, redirect, url_for, flash, request, abort
from projeto4flask import appSite, database, bcrypt
from projeto4flask.forms import FormLogin, FormCriarConta, FormEditarPerfil, FormCriarPost
from projeto4flask.models import Usuario, Post
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image

# pastas padroes do Flask no projeto indicadas no appSite.route em render_template
# diretorio "templates" -> onde ficam armazenados os codigos html

@appSite.route('/')
def home():
    posts = Post.query.order_by(Post.id.desc()).all()
    return render_template('home.html', posts=posts)

@appSite.route('/contato')
def contato():
    return render_template('contato.html')

@appSite.route('/usuarios')
@login_required
def usuarios():
    lista_usuarios = Usuario.query.order_by(Usuario.username).all()
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)

@appSite.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()

    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash(f'Login feito com sucesso no email {form_login.email.data}', 'alert-success')
            # verifica se o acesso a pagina de login indica que deve redirecionar para uma pagina especifica
            # indicada no parametro "next" da url
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('home'))
            #fez login com sucesso
        else:
            flash(f'Falha no login email ou senha incorretos', 'alert-danger')

    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        #criptografar a senha
        senha_crypt = bcrypt.generate_password_hash(form_criarconta.senha.data)
        # criar usuario no banco de dados
        usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data, senha=senha_crypt)
        # adicionar dados na sessao
        database.session.add(usuario)
        # dar commit na sessao
        database.session.commit()
        flash(f'Conta criada com sucesso para o email {form_criarconta.email.data}', 'alert-success')
        return redirect(url_for('home'))
        #criou conta com sucesso
    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)

@appSite.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f'Logout feito com sucesso', 'alert-success')
    return redirect(url_for('home'))

@appSite.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('perfil.html', foto_perfil=foto_perfil)

@appSite.route('/criar/post', methods=['GET', 'POST'])
@login_required
def criar_post():
    form_criarpost = FormCriarPost()
    if form_criarpost.validate_on_submit():
        post = Post(titulo=form_criarpost.titulo.data, corpo=form_criarpost.corpo.data, autor=current_user)
        # adicionar dados na sessao
        database.session.add(post)
        # dar commit na sessao
        database.session.commit()
        flash(f'Post criado com sucesso', 'alert-success')
        return redirect(url_for('home'))

    return render_template('criarpost.html', form_criarpost=form_criarpost)

def tratar_salvar_imagem(imagem):
    # ------- adicionar codigo aleatorio no nome da imagem
    cod_imagem = secrets.token_hex(8)
    nomearq, extensaoarq = os.path.splitext(imagem.filename)
    novo_nome_imagem = nomearq + cod_imagem + extensaoarq
    # ------- criar nome da imagem unico para cada usuario usando ID
    novo_nome_imagem = 'img_perfil-id_' + str(current_user.id) + extensaoarq
    path_imagem = os.path.join(appSite.root_path, 'static/fotos_perfil', novo_nome_imagem)
    # ------- reduzir o tamanho da imagem para 200px x 200px
    tamanho = (200, 200)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    # ------- salvar a imagem na pasta fotos_perfil
    imagem_reduzida.save(path_imagem)
    # ------- retorna novo nome da imagem para salvar no db do usuario
    return novo_nome_imagem

def analisar_cursos_marcados(form_editarperfil):
    lista_cursos_escolhidos = []
    for campo in form_editarperfil:
        if 'curso_' in campo.name:
            #adiciona o texto do label do campo na lista python
            if campo.data:
                lista_cursos_escolhidos.append(campo.label.text)
    if lista_cursos_escolhidos:
        cursos_marcados_csv = ';'.join(lista_cursos_escolhidos)
    else:
        cursos_marcados_csv = "Não Informado"
    return cursos_marcados_csv


@appSite.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def perfil_editar():
    form_editarperfil = FormEditarPerfil()
    if form_editarperfil.validate_on_submit():
        current_user.username = form_editarperfil.username.data
        current_user.email = form_editarperfil.email.data
        # atualiza foto de perfil
        if form_editarperfil.foto_perfil.data:
            nome_imagem = tratar_salvar_imagem(form_editarperfil.foto_perfil.data)
            # atualizar o campo foto_perfil do Db do usuario para novo nome da imagem
            current_user.foto_perfil = nome_imagem
        # atualiza cursos marcados
        current_user.cursos = analisar_cursos_marcados(form_editarperfil)
        database.session.commit()
        flash(f'Alteração de perfil executada com sucesso', 'alert-success')
        return redirect(url_for('perfil'))
    # caso esteja somente carregando a pagina preencher o formulario
    elif request.method == 'GET':
        # exibindo as informacoes do usuario para alteracao
        form_editarperfil.username.data = current_user.username
        form_editarperfil.email.data = current_user.email
        # exibindo as informacoes dos cursos para alteracao
        if current_user.cursos != "Não Informado":
            lista_cursos_atuais = current_user.cursos.split(';')
            for curso in lista_cursos_atuais:
                for campo in form_editarperfil:
                    print(campo.label.text)
                    if campo.label.text == curso:
                        campo.data = True
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form_editarperfil=form_editarperfil)

@appSite.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
def exibir_editar_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        form_editarpost = FormCriarPost()
        if request.method == 'GET':
            # exibindo as informacoes do usuario para alteracao
            form_editarpost.titulo.data = post.titulo
            form_editarpost.corpo.data = post.corpo
        else:
            if form_editarpost.validate_on_submit():
                post.titulo = form_editarpost.titulo.data
                post.corpo =form_editarpost.corpo.data
                database.session.commit()
                flash(f'Post atualizado com sucesso', 'alert-success')
                return redirect(url_for('home'))
    else:
        form_editarpost = None
    return render_template('post.html', post=post, form_editarpost=form_editarpost)


@appSite.route('/post/<post_id>/excluir', methods=['GET', 'POST'])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash(f'Post título: [{post.titulo}]. Excluído com Sucesso', 'alert-success')
        return redirect(url_for('home'))
    else:
        abort(403)
