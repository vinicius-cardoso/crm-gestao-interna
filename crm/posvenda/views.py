from flask import Blueprint, render_template, request, redirect, url_for
from crm.projetos.models import Projeto
from crm import db

pos_venda = Blueprint('pos_venda', __name__, template_folder="templates")

@pos_venda.route('/')
def index():
    projetos = Projeto.query.all()
    return render_template('posvenda.html', projetos = projetos)

