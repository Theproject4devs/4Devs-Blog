import sqlite3


# nome = "Rennan"
# senha = "123"
# with sqlite3.connect('instance\\users.db') as conexao:
#     cursor = conexao.cursor()

#     conexao.commit()s


# nome = "Felipe"
# senha = "123"

# conn = sqlite3.connect("instance\\users.db")
# cursor = conn.cursor()
# cursor.execute("INSERT INTO user (username, password, is_admin)
#  VALUES ('Felipe', '123', 'True')")
# conn.commit()
# conn.close()

# cursor.execute("INSERT INTO user (username, password, is_admin)\
#                 VALUES (?, ?, ?)", (nome, senha, "True"))
# with sqlite3.connect('instance\\users.db') as conexao:
#     cursor = conexao.cursor()
#     cursor.execute("SELECT * FROM users WHERE username = ? \
#                     AND password = ?", (nome, senha))
#     user_data = cursor.fetchone()
#     print(user_data)

# Abrindo a conexão com o banco de dados
# conn = sqlite3.connect('instance\\users.db')
# cursor = conn.cursor()

# # Criando a tabela se não existir
# cursor.execute('''CREATE TABLE IF NOT EXISTS user
#                     (id INTEGER PRIMARY KEY,
#                username TEXT,
#                password TEXT,
#                is_admin TEXT)''')
# # Inserindo a imagem na tabela
# cursor.execute("INSERT INTO user (username, password, is_admin) VALUES \
#                ('Jorge', '111', 'False')\
#                 ")
# conn.commit()

# # Fechando a conexão com o banco de dados
# conn.close()


# insert_image('app\\controllers\\imgtest.jpg', "instance\\imgaes.db")


def inserir_imgs(path_img, titulo, descricao, file_db):
    conn = sqlite3.connect(file_db)
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS images (
                   id INTEGER PRIMARY KEY,
                   titulo TEXT,
                   descricao TEXT,
                   imgs BLOB
                   )""")

    with open(path_img, 'rb') as file:
        img_bytes = file.read()

    cursor.execute("""INSERT INTO images (titulo, descricao, imgs\
                   ) VALUES (?, ?, ?)\
                   """, (titulo, descricao, sqlite3.Binary(img_bytes),))
    conn.commit()
    conn.close()


inserir_imgs(path_img="app\\controllers\\cipolas.jpg\
             ", file_db="instance\\imgs.db", titulo="Cipolas\
                ", descricao="Agora é o cipolas que da\
                     o bumbum na delfia")
