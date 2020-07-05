from flask import Blueprint, render_template, request, redirect, url_for
from crm import db
from crm.clientes.models import Cliente
from sqlalchemy.sql import func
from datetime import *

cliente = Blueprint('cliente', __name__, template_folder="templates")

@cliente.route("/", methods=['GET', 'POST'])
def index():

    clientes = Cliente.query.all()

    
    
    if request.method == 'POST'and 'nome' in request.form:
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        status = request.form['status']
        endereco = request.form['endereco']
        datainsercao = request.form['datainsercao']
        prospeccao = request.form.get('prospeccao')
        print(str(prospeccao))
        clientes = Cliente(nome = nome,
                            email = email,
                            telefone = telefone,
                            status = status,
                            endereco = endereco,
                            datainsercao = datainsercao,
                            prospeccao = prospeccao)


        atualizacaoHistorico = clientes.historico_status.split(",")

        if(request.form['status'] == "Lead"):
            atualizacaoHistorico[0] = str(datainsercao).replace("-", "")
        elif(request.form['status'] == "Qualificado"):
            atualizacaoHistorico[1] = str(datainsercao).replace("-", "")
        elif(request.form['status'] == "Proposta Enviada"):
            atualizacaoHistorico[2] = str(datainsercao).replace("-", "")
        elif(request.form['status'] == "Em Negociação"):
            atualizacaoHistorico[3] = str(datainsercao).replace("-", "")
        elif(request.form['status'] == "Ativo"):
            atualizacaoHistorico[4] = str(datainsercao).replace("-", "")
        elif(request.form['status'] == "Perdido"):
            atualizacaoHistorico[5] = str(datainsercao).replace("-", "")

        clientes.historico_status = ",".join(atualizacaoHistorico)

        db.session.add(clientes)
        db.session.commit()
        
        return redirect(url_for('cliente.index'))

   

    return render_template('clientes.html', clientes=clientes)

@cliente.route('/especifico/<_id>', methods=['GET', 'POST'])
def especifico(_id):

    cliente = Cliente.query.get_or_404(_id)

    separador = 0

    if(request.method == 'POST' and 'nome' in request.form):
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        endereco = request.form['endereco']
        status = request.form['status']
        datainsercao = request.form['datainsercao']
        prospeccao = request.form['prospeccao']

        separador = 1

        if(cliente.status != request.form['status']):

            atualizacaoHistorico = cliente.historico_status.split(",")

            if(request.form['status'] == "Lead"):
                atualizacaoHistorico[0] = str(date.today()).replace("-", "")
            elif(request.form['status'] == "Qualificado"):
                atualizacaoHistorico[1] = str(date.today()).replace("-", "")
            elif(request.form['status'] == "Proposta Enviada"):
                atualizacaoHistorico[2] = str(date.today()).replace("-", "")
            elif(request.form['status'] == "Em Negociação"):
                atualizacaoHistorico[3] = str(date.today()).replace("-", "")
            elif(request.form['status'] == "Ativo"):
                atualizacaoHistorico[4] = str(date.today()).replace("-", "")
            elif(request.form['status'] == "Perdido"):
                atualizacaoHistorico[5] = str(date.today()).replace("-", "")

            cliente.historico_status = ",".join(atualizacaoHistorico)
            print(cliente.historico_status)

        status = request.form['status']

        cliente.nome = nome
        cliente.email = email
        cliente.telefone = telefone
        cliente.endereco = endereco
        cliente.status = status
        cliente.datainsercao = datainsercao
        cliente.prospeccao = prospeccao

        db.session.commit()

        
    if request.method == 'POST' and 'comentario' in request.form:

        print("teste")

        separador = 1

        if(cliente.observacoes == "Sem comentarios Ainda!"):
            cliente.observacoes = request.form['comentario']
        else:
            cliente.observacoes = cliente.observacoes + "|" + request.form['comentario']

        db.session.commit()
        
        return redirect(url_for('cliente.especifico', _id = _id))

    if request.method == 'POST' and separador == 0:
        db.session.delete(cliente)
        db.session.commit()
        
        return redirect(url_for('cliente.index'))

    i = 0
    cliente_dts_status = cliente.historico_status
    cliente_dts_status = cliente_dts_status.split(',')
    cliente_observacoes = cliente.observacoes.split('|')

    

    

    

    while(i < len(cliente_dts_status)):
        cliente_dts_status[i] = cliente_dts_status[i][-2:] + '/' + cliente_dts_status[i][4:-2] + '/' + cliente_dts_status[i][:4]
        i = i + 1
    
    return render_template('especifico_cliente.html', cliente = cliente, 
                                                    cliente_dts_status = cliente_dts_status, 
                                                    cliente_observacoes = cliente_observacoes)

@cliente.route('/pesquisa',  methods=['GET', 'POST'])
def pesquisa():
    pesquisa = request.form['pesquisa']
    clientes_pesquisados = Cliente.query.filter(Cliente.nome.contains(str(pesquisa)))

    
    return render_template('pesquisa-cliente.html', clientes=clientes_pesquisados)





    