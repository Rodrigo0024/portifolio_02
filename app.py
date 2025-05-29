# app.py
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
class Projeto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    imagem = db.Column(db.String(200), nullable=True)  # Nome do arquivo da imagem
    link = db.Column(db.String(200))  # Link do projeto (opcional)
    descricao = db.Column(db.Text, nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)

class Mensagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    texto = db.Column(db.Text, nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def index():
    projetos = Projeto.query.order_by(Projeto.data.desc()).all()
    return render_template('index.html', projetos=projetos)
@app.route('/loginpagina',  methods=["GET", "POST"])
def loginpagina():
    
    return render_template('login.html')
@app.route('/sobre')
def sobre():
    return render_template('sobre.html')


@app.route('/sistemaloginexplicacao')
def sistemaloginexplicacao():
    return render_template('sistema_login_explicacao.html')

@app.route('/blogexplicacao')
def blogexplicacao():
    return render_template('blogexplicacao.html')
@app.route('/projetos')
def projetos():
    projetos = Projeto.query.order_by(Projeto.data.desc()).all()
    return render_template('projetos.html', projetos=projetos)

@app.route('/contato', methods=['GET', 'POST'])
def contato():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        texto = request.form['texto']

        nova_mensagem = Mensagem(nome=nome, email=email, texto=texto)
        db.session.add(nova_mensagem)
        db.session.commit()

        return redirect(url_for('contato'))

    mensagens = Mensagem.query.order_by(Mensagem.data.desc()).all()
    return render_template('contato.html', mensagens=mensagens)
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/img/projetos'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(file):
    return '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/projeto/novo', methods=['GET', 'POST'])
def novo_projeto():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        link = request.form['link']

        # Upload da imagem
        imagem = request.files['imagem']
        imagem_filename = None

        if imagem and allowed_file(imagem):
            filename = secure_filename(imagem.filename)
            imagem.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            imagem_filename = filename

        novo_projeto = Projeto(
            titulo=titulo,
            descricao=descricao,
            imagem=imagem_filename,
            link=link
        )

        db.session.add(novo_projeto)
        db.session.commit()

        return redirect(url_for('projetos'))

    return render_template('novo_projeto.html')



@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "adm" and password == "brasil":
            return render_template('novo_projeto.html')
        else:
            error = "Usuário ou senha incorretos!"

    return render_template("index.html", error=error)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)