from app import app
from flask_pymongo import PyMongo

app.config['AFFECTANALYSIS_DBNAME'] = 'affect-analysis'
affect_analysis = PyMongo(app, config_prefix='AFFECTANALYSIS')

app.config['ROLEANALYSIS_DBNAME'] = 'role-analysis'
role_analysis = PyMongo(app, config_prefix='ROLEANALYSIS')

app.config['PERCEPTANALYSIS_DBNAME'] = 'percept-analysis'
percept_analysis = PyMongo(app, config_prefix='PERCEPTANALYSIS')
