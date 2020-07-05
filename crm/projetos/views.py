from flask import Blueprint, render_template, request, redirect, url_for
from crm import db
from crm.projetos.models import Projeto
import os

projeto = Blueprint('projeto', __name__, template_folder="templates")

@projeto.route('/', methods=['POST', 'GET'])
def index():

    projetos = Projeto.query.all()
    projetos.sort(key=lambda x: x.data, reverse=False)
    
    if request.method == 'POST' and 'nome' in request.form:
        projetos = Projeto(request.form['nome'], 
                           request.form['tipo'], 
                           request.form['cliente'], 
                           request.form['url'], 
                           request.form['valor'], 
                           request.form['po'], 
                           request.form['prazo'], 
                           request.form['inicio'], 
                           request.form['status'])
        db.session.add(projetos)
        db.session.commit()
        
        return redirect(url_for('projeto.index'))
    
    return render_template('projetos.html', projetos=projetos)

    

@projeto.route('/especifico/<_id>', methods=['POST', 'GET'])
def especifico(_id):

    separador = 0

    projeto = Projeto.query.get_or_404(_id)
    projeto_comentarios = projeto.comentarios.split('|')

    if request.method == 'POST' and 'nome' in request.form:
        

        nome = request.form['nome']
        tipo = request.form['tipo']
        cliente = request.form['cliente']
        url = request.form['url']
        valor = request.form['valor']
        po = request.form['po']
        prazo = request.form['prazo']
        inicio = request.form['inicio']
        status = request.form['status']
        nota = request.form['nota']

        separador = 1
        data = int(0)

        if(nota != "Sem nota"):
            projeto.nota = nota
        if('-' in prazo):
            projeto.prazo = prazo.replace('-', '/')
            projeto.prazo = projeto.prazo[8:] + '/' + projeto.prazo[5:7] + '/' + projeto.prazo[:4]
            data = int(prazo.replace('-', ''))
            projeto.data = data
        if('-' in inicio):
            projeto.inicio = inicio.replace('-', '/')
            projeto.inicio = projeto.inicio[8:] + '/' + projeto.inicio[5:7] + '/' + projeto.inicio[:4]

        projeto.nome = nome
        projeto.tipo = tipo
        projeto.cliente = cliente
        projeto.url = url
        projeto.valor = valor
        projeto.po = po
        projeto.status = status
        

        db.session.commit()

        return redirect(url_for('projeto.especifico', _id = projeto.id))
    
    if request.method == 'POST' and 'comentario' in request.form:

        separador = 1

        if(projeto.comentarios == "Sem comentarios Ainda!"):
            projeto.comentarios = request.form['comentario']
        else:
            projeto.comentarios = projeto.comentarios + "|" + request.form['comentario']

        db.session.commit()
        
        return redirect(url_for('projeto.especifico', _id = _id))

    if request.method == 'POST' and separador == 0:
        db.session.delete(projeto)
        db.session.commit()
        
        return redirect(url_for('projeto.index'))
    
    return render_template('especifico_projetos.html', projeto = projeto, 
                                                       projeto_comentarios = projeto_comentarios,
                                                       )
@projeto.route('/pesquisa', methods=['GET', 'POST'])
def pesquisa():
    pesquisa = request.form['pesquisa']
    projetos_pesquisados = Projeto.query.filter(Projeto.nome.contains(str(pesquisa)))

    return render_template('pesquisa-projeto.html', projetos=projetos_pesquisados)