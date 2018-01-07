from app import app
from flask_pymongo import PyMongo

app.config['AFFECTANALYSIS_DBNAME'] = 'affect-analysis'
affect_analysis = PyMongo(app, config_prefix='AFFECTANALYSIS')
