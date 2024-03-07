from app.models.users_db import Users
from app import app
from flask import render_template, redirect, request, abort, session
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
import sqlite3
import base64
import re
from datetime import datetime


login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    print("ENTROU")
    conn = sqlite3.connect('instance\\users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE username = ?", (user_id,))
    user_data = cursor.fetchone()
    if user_data:
        name = user_data[1]
        email = user_data[2]
        username = user_data[3]
        password = user_data[4]
        is_admin = user_data[5]
        print("CHEGOU ATÈ AQUI")
        if is_admin == "True":
            return Users(username=username, email=email, name=name,
                         password=password, trouth=True)
        else:
            return Users(username=username, email=email, name=name,
                         password=password, trouth=False)
    else:
        print("CHEGOU ATÈ AQUI")
        return None


def get_db_connection(path_db):
    conn = sqlite3.connect(f'instance\\{path_db}')
    conn.row_factory = sqlite3.Row
    return conn

def calculate_time_since_creation(created_at):
    created_at_datetime = datetime.strptime(created_at, '%d/%m/%Y %H:%M')
    current_datetime = datetime.now()
    difference = current_datetime - created_at_datetime
    days = difference.days
    hours = difference.seconds // 3600
    minutes = (difference.seconds % 3600) // 60
    return hours, minutes, days


@app.route("/")
def index():
    conn = get_db_connection("posts.db")
    posts = conn.execute('SELECT * FROM posts').fetchall()
    img_data =[]
    for post in posts:
        img_data.append(base64.b64encode(post["imgs"]).decode('utf-8'))
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

        conn = sqlite3.connect('instance\\users.db')
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


def obter_dados_imagem(id_imagem):
    conn = sqlite3.connect('instance\\posts.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts WHERE id = ?", (id_imagem))
    imagem = cursor.fetchone()
    conn.close()
    if imagem:
        return True
    else:
        return None


@app.route("/posts/<id>")
@app.route("/posts/make")
def teste(id: str | None = None):
    if id:
        conn = sqlite3.connect("instance\\posts.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM posts WHERE id = ?", (id))
        post = cursor.fetchone()
        if post:
            id, titulo, descricao, imagem = post
            imagem_base64 = base64.b64encode(imagem).decode('utf-8')
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
    password_register = request.form.get("register-password")
    
    conn = get_db_connection("users.db")
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO user (name, email, username, password, is_admin)\
        VALUES (?, ?, ?, ?, False)", (name_register, email_register, 
                                      username_register, password_register))
    
    conn.commit()
    conn.close()
    
    return render_template("login.html")

@app.route("/make_post")
def make_post():
    return render_template("make_post.html")

def inserir_imgs(path_img, titulo, descricao, file_db):
    conn = sqlite3.connect(file_db)
    cursor = conn.cursor()

    # with open(path_img, 'rb') as file:
    #     img_bytes = file.read()
    date = datetime.now().strftime('%d/%m/%Y %H:%M')
    cursor.execute("""INSERT INTO posts (titulo, descricao, imgs\
                   , created_at) VALUES (?, ?, ?, ?)\
                   """, (titulo, descricao, sqlite3.Binary(path_img), date,))
    conn.commit()
    conn.close()


def filtrar_nome_arquivo(nome_arquivo):
    return re.sub(r'\W+', ' ', nome_arquivo)

@app.route("/submit_post", methods=["POST"])
def submit_post():
    titulo = request.form.get("titulo")
    descricao = request.form.get("conteudo")
    input_ = request.files.get("imagem-video")
    
    titulo_filtrado = filtrar_nome_arquivo(titulo)
    descricao_filtrado = filtrar_nome_arquivo(descricao)
    
    if input_:
        img_bytes = input_.read()
    

    inserir_imgs(path_img=img_bytes, titulo=titulo_filtrado, descricao=descricao_filtrado, file_db="instance\\posts.db")
    return redirect("/")

@app.route('/search')
def search():
    query = request.args.get('query')
    
    conn = get_db_connection("posts.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts WHERE titulo LIKE ? OR descricao LIKE ?", ('%' + query + '%', '%' + query + '%'))
    search_results = cursor.fetchall()
    img_data = []
    for result in search_results:
        img_data.append(base64.b64encode(result["imgs"]).decode('utf-8'))
    conn.close()
    
    if query == "":
        return redirect("/")
    
    elif search_results:
        return render_template('index.html', query=query, results=search_results, img_data=img_data,
                                calculate_time_since_creation=calculate_time_since_creation)

    else:
        return render_template("index.html", msgerro="Nada Encontrado")
    
    
@app.route("/see_more")
def see_more():
    ...