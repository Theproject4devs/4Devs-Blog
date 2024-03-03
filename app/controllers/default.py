from app.models.users_db import Users
from app import app
from flask import render_template, redirect, request, abort, session
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
import sqlite3
import base64


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


def get_db_connection():
    conn = sqlite3.connect('instance\\imgs.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM images').fetchall()
    for post in posts:
        img = base64.b64encode(post["imgs"]).decode('utf-8')
    conn.close()
    logged_in = current_user.is_authenticated
    return render_template("index.html\
                           ", logged_in=logged_in, posts=posts, img=img)
    return render_template("index.html")


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


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    logout_user()
    return redirect("/")


def obter_dados_imagem(id_imagem):
    conn = sqlite3.connect('instance\\imgs.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM images WHERE id = ?", (id_imagem))
    imagem = cursor.fetchone()
    conn.close()
    if imagem:
        return True
    else:
        return None


@app.route("/teste/<id>")
def teste(id):
    conn = sqlite3.connect("instance\\imgs.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM images WHERE id = ?", (id))
    post = cursor.fetchone()
    if post:
        id, titulo, descricao, imagem = post
        imagem_base64 = base64.b64encode(imagem).decode('utf-8')
        post_base64 = (titulo, descricao, imagem_base64)

    else:
        post_base64 = None

    conn.close()

    return render_template("test.html", post=post_base64)


@app.route("/profile")
@login_required
def profile():
    msg = f"""Nome: {current_user.name} <br>
Email: {current_user.email}<br>
Username: {current_user.username}<br>
Senha: {current_user.password}"""
    return msg
