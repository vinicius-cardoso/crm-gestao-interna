import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'qualquercoisa'

#######################################################
################# BANCO DE DADOS ######################
#######################################################

baseDir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(baseDir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

#######################################################
################### BLUEPRINTS ########################
#######################################################

from crm.home.views import home
from crm.clientes.views import cliente
from crm.projetos.views import projeto
from crm.posvenda.views import pos_venda

app.register_blueprint(home)
app.register_blueprint(cliente, url_prefix="/clientes")
app.register_blueprint(projeto, url_prefix="/projetos")
app.register_blueprint(pos_venda, url_prefix="/pos_venda")

