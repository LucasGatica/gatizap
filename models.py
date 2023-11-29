from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Conta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)
    telefone = db.Column(db.String(20), unique=True, nullable=False)
    mensagens = db.relationship('Mensagem', backref='conta', lazy=True)

class Mensagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.String(200), nullable=False)
    conta_id = db.Column(db.Integer, db.ForeignKey('conta.id'), nullable=False)
