import base64
import sqlite3
from datetime import datetime


def image_converter(imagem):
    img_converter = base64.b64encode(imagem).decode('utf-8')
    return img_converter


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
