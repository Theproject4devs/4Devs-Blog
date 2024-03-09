from app.models.users_db import Users
from app import app
from flask import render_template, redirect, request, abort, session
from flask_login import LoginManager, login_user, current_user, \
    logout_user, login_required
from app.controllers.databases import get_db_connection, get_post_details
from app.controllers.time_calculator import calculate_time_since_creation
from app.controllers.images_config import image_converter, inserir_imgs
from app.controllers.filtrar_nome import filtrar_nome_arquivo


login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    print("Carregando usuario\n")
    conn = get_db_connection("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE username = ?", (user_id,))
    user_data = cursor.fetchone()
    if user_data:
        name = user_data[1]
        email = user_data[2]
        username = user_data[3]
        password = user_data[4]
        is_admin = user_data[5]
        print("Usuario carregado")
        if is_admin == "True":
            return Users(username=username, email=email, name=name,
                         password=password, trouth=True)
        else:
            return Users(username=username, email=email, name=name,
                         password=password, trouth=False)
    else:
        return None


@app.route("/")
def index():
    conn = get_db_connection("posts.db")
    posts = conn.execute('SELECT * FROM posts').fetchall()
    img_data = []
    for post in posts:
        img_data.append(image_converter(post["imgs"]))
    conn.close()
    logged_in = current_user.is_authenticated
    return render_template("index.html\
", logged_in=logged_in, posts=posts, img_data=img_data,
                           calculate_time_since_creation=calculate_time_since_creation)


@app.route("/login", methods=["GET"])
def log():
    return render_template("login.html")


@app.route("/verify_login", methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        username = request.form.get("name")
        senha = request.form.get("senha")

        conn = get_db_connection("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user WHERE username = ? \
                    AND password = ?", (username, senha))
        user_data = cursor.fetchone()

        if user_data:
            name, _ = user_data[3], user_data[4]
            user = load_user(name)
            login_user(user)
            return redirect("/")
        else:
            msg = "Usuario e/ou senha inválidos."
            render_template("login.html")
            return render_template("login.html", msg=msg)
    else:
        return abort(404)


@app.route("/logout", methods=["POST", "GET"])
def logout():
    session.clear()
    logout_user()
    return redirect("/")


@app.route("/posts/make")
def teste(id: str | None = None):
    if id:
        conn = get_db_connection("posts.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM posts WHERE id = ?", (id))
        post = cursor.fetchone()
        if post:
            id, titulo, descricao, imagem = post
            imagem_base64 = image_converter(imagem)
            post_base64 = (titulo, descricao, imagem_base64)

        else:
            post_base64 = None

            conn.close()

        return render_template("test.html", post=post_base64)
    try:
        name = current_user.name
        return render_template("posts.html", name=name)
    except AttributeError:
        return render_template("teste.html")


@app.route("/profile")
@login_required
def profile():
    msg = f"""Nome: {current_user.name} <br>
Email: {current_user.email}<br>
Username: {current_user.username}<br>
Senha: {current_user.password}"""
    return msg


@app.route("/register", methods=["POST"])
def register():
    name_register = request.form.get("name-register")
    username_register = request.form.get("username-register")
    email_register = request.form.get("email-register")
    password_register = request.form.get("senha-register")

    conn = get_db_connection("users.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO user (name, email, username, password,\
        is_admin) VALUES (?, ?, ?, ?, False)", (name_register,
                                                email_register,
                                                username_register,
                                                password_register))

    conn.commit()
    conn.close()

    return render_template("login.html")


@app.route("/make_post")
def make_post():
    return render_template("make_post.html")


@app.route("/submit_post", methods=["POST"])
def submit_post():
    titulo = request.form.get("titulo")
    descricao = request.form.get("conteudo")
    input_ = request.files.get("imagem-video")

    titulo_filtrado = filtrar_nome_arquivo(titulo)
    descricao_filtrado = filtrar_nome_arquivo(descricao)

    if input_:
        img_bytes = input_.read()

    inserir_imgs(path_img=img_bytes, titulo=titulo_filtrado,
                 descricao=descricao_filtrado, file_db="instance\\posts.db")
    return redirect("/")


@app.route('/search')
def search():
    query = request.args.get('query')

    conn = get_db_connection("posts.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts WHERE titulo LIKE ? OR descricao \
        LIKE ?", ('%' + query + '%', '%' + query + '%'))
    search_results = cursor.fetchall()
    img_data = []
    for result in search_results:
        img_data.append(image_converter(result["imgs"]))
    conn.close()

    if query == "":
        return redirect("/")

    elif search_results:
        return render_template('index.html', query=query,
                               results=search_results,
                               img_data=img_data,
                               calculate_time_since_creation=calculate_time_since_creation)

    else:
        return render_template("index.html", msgerro="Nada Encontrado")


@app.route('/posts/<int:post_id>')
def post_details(post_id):

    post = get_post_details(post_id)

    titulo = post[1]
    descricao = post[2]
    img_data = (image_converter(post[3]))
    created_at = post[4]
    try:
        return render_template("lermais.html", post=post, titulo=titulo,
                               descricao=descricao,
                               img_data=img_data, created_at=created_at,
                               nome=current_user.name,
                               calculate_time_since_creation=calculate_time_since_creation)
    except AttributeError:
        return render_template("lermais.html", post=post, titulo=titulo,
                               descricao=descricao,
                               img_data=img_data, created_at=created_at,
                               calculate_time_since_creation=calculate_time_since_creation)
