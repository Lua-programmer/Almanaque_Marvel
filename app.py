from flask import Flask, Blueprint, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
bp = Blueprint('app', __name__)

#database

user = 'ciechjpy'
password = 'JAGrOSsMPm2Ad1lQRB7tCX8A8CwTRdyQ'
host = 'tuffi.db.elephantsql.com'
database = 'ciechjpy'

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{host}/{database}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Personagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_ = db.Column(db.String(255), nullable=False)
    imagem_url_ = db.Column(db.String(255), nullable=False)
    biografia_ = db.Column(db.String(), nullable=False)

    def __init__(self, nome_, imagem_url_, biografia_):
        self.nome_ = nome_
        self.imagem_url_ = imagem_url_
        self.biografia_ = biografia_

    @staticmethod
    def read_all():
        return Personagem.query.all()   

    @staticmethod
    def read(personagem_id):
        return Personagem.query.get(personagem_id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, new_data):
        print(new_data)
        self.nome_ = new_data.nome_
        self.imagem_url_ = new_data.imagem_url_
        self.biografia_ = new_data.biografia_
        self.save()

    def delete(self):
        db.session.delete(self) 
        db.session.commit()



@bp.route('/')
def home():
    return render_template(
        "home.html"
)

@bp.route('/read')
def listaDePersonagens():
    personagem = Personagem.read_all() 
    return render_template(
        "read.html", listaDePersonagens = personagem, personagem = personagem
)


@bp.route('/read/<personagem_id>')
def biografia(personagem_id,):
    personagem = Personagem.read(personagem_id)

    

    return render_template(
        'biografia.html', personagem = personagem
)

@bp.route('/create', methods=('GET', 'POST'))
def create():

    id_atribuido = None

    if request.method == 'POST':
        form = request.form
        personagem = Personagem(form['nome_'], form['imagem_url_'], form['biografia_'])
        personagem.save()
        id_atribuido = personagem.id

    return render_template(
        'create.html', id_atribuido = id_atribuido
)

@bp.route('/update/<personagem_id>', methods=('GET', 'POST'))
def update(personagem_id):
  sucesso = None
  personagem = Personagem.read(personagem_id)

  if request.method == 'POST':
    form = request.form
    print(form)

    new_data = Personagem(form['nome_'], form['imagem_url_'], form['biografia_'])

    personagem.update(new_data)

    sucesso = True

  return render_template(
    'update.html', personagem = personagem , sucesso = sucesso
)

@bp.route('/delete/<personagem_id>')
def delete(personagem_id):
  personagem = Personagem.read(personagem_id)
  return render_template(
    'delete.html', personagem = personagem
)

@bp.route('/delete/<personagem_id>/confirmed')
def delete_confirmed(personagem_id):
  sucesso = None

  personagem = Personagem.read(personagem_id)

  if personagem:
    personagem.delete()
    sucesso = True

  return render_template(
    "delete.html", sucesso = sucesso, personagem=personagem
)

@bp.route('/sobre')
def sobre():
    return render_template(
        "criadoras.html"
)










app.register_blueprint(bp)
if __name__ == '__main__':
    app.run(debug=True)