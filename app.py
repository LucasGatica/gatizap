from flask import Flask, render_template, request, redirect, url_for
from models import db, Conta, Mensagem

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mensagens.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/criar_conta', methods=['GET', 'POST'])
def criar_conta():
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        nova_conta = Conta(nome=nome, telefone=telefone)
        db.session.add(nova_conta)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('criar_conta.html')

@app.route('/listar_mensagens')
def listar_mensagens():
    ultima_mensagem_id = db.session.query(
        db.func.max(Mensagem.id).label('max_id')
    ).group_by(Mensagem.conta_id).subquery()

    mensagens = db.session.query(
        Conta.id, Conta.nome, Mensagem.conteudo
    ).join(Mensagem, Conta.id == Mensagem.conta_id)\
     .join(ultima_mensagem_id, Mensagem.id == ultima_mensagem_id.c.max_id)\
     .all()

    return render_template('listar_mensagens.html', mensagens=mensagens)


@app.route('/listar_contas')
def listar_contas():
    contas = Conta.query.all()
    return render_template('lista_contas.html', contas=contas)

@app.route('/atualizar_conta/<int:id>', methods=['GET', 'POST'])
def atualizar_conta(id):
    conta = Conta.query.get_or_404(id)
    if request.method == 'POST':
        conta.nome = request.form['nome']
        conta.telefone = request.form['telefone']
        db.session.commit()
        return redirect(url_for('listar_contas'))
    return render_template('atualizar_conta.html', conta=conta)

@app.route('/deletar_conta/<int:id>')
def deletar_conta(id):
    conta = Conta.query.get_or_404(id)
    db.session.delete(conta)
    db.session.commit()
    return redirect(url_for('listar_contas'))


@app.route('/enviar_mensagem', methods=['GET', 'POST'])
def enviar_mensagem():
    if request.method == 'POST':
        conteudo = request.form['mensagem']
        conta_id = request.form['conta_id']
        nova_mensagem = Mensagem(conteudo=conteudo, conta_id=conta_id)
        db.session.add(nova_mensagem)
        db.session.commit()
        return redirect(url_for('home'))
    contas = Conta.query.all()
    return render_template('enviar_mensagem.html', contas=contas)


@app.route('/conversa/<int:conta_id>')
def conversa(conta_id):
    conversa_mensagens = Mensagem.query.filter_by(conta_id=conta_id).all()
    conta_nome = Conta.query.get(conta_id).nome
    return render_template('conversa.html', mensagens=conversa_mensagens, conta_nome=conta_nome)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

