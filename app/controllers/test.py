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

def inserir_imgs(path_img, titulo, descricao, file_db):
    conn = sqlite3.connect(file_db)
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS posts (
                   id INTEGER PRIMARY KEY,
                   titulo TEXT,
                   descricao TEXT,
                   imgs BLOB
                   )""")

    with open(path_img, 'rb') as file:
        img_bytes = file.read()

    cursor.execute("""INSERT INTO posts (titulo, descricao, imgs\
                   ) VALUES (?, ?, ?)\
                   """, (titulo, descricao, sqlite3.Binary(img_bytes),))
    conn.commit()
    conn.close()


inserir_imgs(path_img="app\\controllers\\cipolas.jpg\
             ", file_db="instance\\posts.db", titulo="Rennan\
                ", descricao="Agora é o rennan que da\
                     o bumbum na delfia")
