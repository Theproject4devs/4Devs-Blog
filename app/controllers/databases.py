import sqlite3


def get_db_connection(path_db):
    conn = sqlite3.connect(f'instance\\{path_db}')
    conn.row_factory = sqlite3.Row
    return conn


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


def get_post_details(post_id):
    conn = get_db_connection("posts.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM posts WHERE id=?", (post_id,))
    post = cursor.fetchone()
    conn.close()
    return post
