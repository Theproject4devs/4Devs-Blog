from app import db


class Postagens():
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(50))
    descricao = db.Column(db.String(50))
    imagem = db.Column(db.LargeBinary)
