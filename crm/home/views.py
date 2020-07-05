from flask import Blueprint, render_template, request, redirect, url_for
from crm import db
from crm.clientes.models import Cliente
from crm.projetos.models import Projeto
from datetime import *
from sqlalchemy.sql import func
import copy

home = Blueprint('home', __name__, template_folder="templates")

@home.route("/index", methods=['GET', 'POST'])
@home.route('/', methods=['GET', 'POST'])
def index():

    clientes = Cliente.query.all()
    projetos = Projeto.query.all()

    projetos.sort(key=lambda x: x.data, reverse=False)

    listadoida = list()
    listadoida2 = list()
    totprojetos = int(0)
    nota = int(0)
    razaoMedia = int(0)
    media = int(0)
    i = 0
    
    for c in clientes:
        d1 = datetime.today()
        d2 = datetime.strptime(c.datainsercao, '%Y-%m-%d')

        delta = abs((d1 - d2).days)
        
        if delta <= 5:
           listadoida.append(copy.deepcopy(c))
           print(listadoida[i].nome)
           listadoida[i].datainsercao = listadoida[i].datainsercao[8:] + '/' + listadoida[i].datainsercao[5:7] + '/' + listadoida[i].datainsercao[:4]
           i += 1

    
    i = 0
    

    for p in projetos:
        if p.status != "Cancelado":
            totprojetos += 1
            listadoida2.append(copy.deepcopy(p)) 
    
        if(p.nota >= 0):
            nota = nota + p.nota
            razaoMedia = razaoMedia + 1

        i = i + 1

    if(nota > 0):
        media = round(nota / razaoMedia, 2)
    else:
        media = 0

    print(media)
    print(nota)
    print(razaoMedia)

    faturamento = Projeto.query.with_entities(func.sum(Projeto.valor)).all()

    

        
    data = date.today()
    ano = data.strftime('%Y')

    if request.method == 'POST' and "nomeprojeto" in request.form:
        projeto = Projeto(request.form['nomeprojeto'], 
                            request.form['tipo'],
                            request.form['cliente'], 
                            request.form['url'], 
                            request.form['valor'], 
                            request.form['po'], 
                            request.form['prazo'], 
                            request.form['inicio'], 
                            request.form['status'])
        
        db.session.add(projeto)
        db.session.commit()
        
        
        return redirect(url_for('home.index'))
    
    if request.method == 'POST' and "nome" in request.form:
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        status = request.form['status']
        endereco = request.form['endereco']
        datainsercao = request.form['datainsercao']
        prospeccao = request.form.get('prospeccao')

        clientes = Cliente(nome = nome,
                            email = email,
                            telefone = telefone,
                            status = status,
                            endereco = endereco,
                            datainsercao = datainsercao,
                            prospeccao = prospeccao)

        db.session.add(clientes)
        db.session.commit()

        return redirect(url_for('home.index'))

    return render_template('index.html', clientes=clientes, 
                                         listadoida2=listadoida2,  
                                         faturamento=faturamento,
                                         media=media,
                                         ano=ano,
                                         totprojetos=totprojetos,
                                         listadoida=listadoida)