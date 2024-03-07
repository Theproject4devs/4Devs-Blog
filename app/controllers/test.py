import sqlite3

# ////////////////////// ADICIONANDO USUARIOS ////////////////////////////////
# nome = "Jorge"
# email = "jorge@gmail.com"
# username = "jorginn"
# senha = "111"
# is_admin = "False"
# conn = sqlite3.connect('instance\\users.db')
# cursor = conn.cursor()

# cursor.execute('''CREATE TABLE IF NOT EXISTS user
#                     (id INTEGER PRIMARY KEY,
#                username TEXT,
#                password TEXT,
#                is_admin TEXT)''')

# cursor.execute("INSERT INTO user (name, email, username, password, is_admin)\
# VALUES (?, ?, ?, ?, ?)", (nome, email, username, senha, is_admin))
# conn.commit()

# conn.close()


# ///////////////////////////// INSERINDO IMAGENS ////////////////////////////

# def inserir_imgs(path_img = None, titulo = None, descricao = None, file_db = None):
#     conn = sqlite3.connect(file_db)
#     cursor = conn.cursor()

#     cursor.execute("""CREATE TABLE IF NOT EXISTS posts (
#                    id INTEGER PRIMARY KEY,
#                    titulo TEXT,
#                    descricao TEXT,
#                    imgs BLOB,
#                    created_at TEXT
#                    )""")

    # with open(path_img, 'rb') as file:
    #     img_bytes = file.read()

    # cursor.execute("""INSERT INTO posts (titulo, descricao, imgs\
    #                ) VALUES (?, ?, ?)\
    #                """, (titulo, descricao, sqlite3.Binary(img_bytes),))
    # conn.commit()
    # conn.close()


# inserir_imgs(file_db="instance\\posts.db")

# //////////////////////////////// DELETANDO POSTS /////////////////////////////////////////////

# conn = sqlite3.connect("instance\\posts.db")
# cursor = conn.cursor()

# id_para_excluir = 1

# # Executar a instrução SQL DELETE
# cursor.execute("DELETE FROM posts WHERE id = ?", (id_para_excluir,))

# conn.commit()
# conn.close()






# from datetime import datetime

# date = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
# print(date, type(date))