from flask import Blueprint
from flask import render_template, redirect, url_for, jsonify, request

import requests, json

from . import controllers
import authentication.controllers

# mongo dependencies
import pymongo
from flask_pymongo import ObjectId

# bson
import json
from bson import json_util

scorer = Blueprint('scorer', __name__)

@scorer.route('/')
def default():
    return controllers.default()

###
#
# Affective Computing
#
###

@scorer.route('/analyze_emotion_set/', methods=['POST'])
def analyze_emotion_set():
    data = request.get_json()
    return controllers.analyze_emotion_set(data=data)

###
#
# Role Computing
#
###

@scorer.route('/analyze_role_set/', methods=['POST'])
def analyze_role_set():
    data = request.get_json()
    return controllers.analyze_role_set(data=data)

###
#
# Role Computing
#
###

@scorer.route('/analyze_percept_set/', methods=['POST'])
def analyze_percept_set():
    data = request.get_json()
    return controllers.analyze_percept_set(data=data)

###
#
# Old Data Management View
#
# Supports the brittle endpoint structure - only good for 'affect'.
#
###

'''
The rational for keeping the old data management is to support the 8 users on Android
who may decide they do not want to update their apps on their phone. (April 4th 2018)

The only difference between old and new versions of data management are that the database
is specified in the request in the newer version. (04-04-18)
'''
@scorer.route('/analyses/<collection>/<page>/<count_per_page>/', methods=['GET'])
def _old_retrieve_all_run_analyses(collection=None, page=None, count_per_page=None):
    token = request.headers['Authorization']
    user_id = authentication.controllers.authenticate_user(token)
    if user_id: # Passes check - this is a valid token.
        return controllers.retrieve_all_run_analyses(
            database='affect', # Only works with 'affect analysis'
            collection=collection,
            page=page,
            count_per_page=count_per_page,
            user_id=user_id
            )
    else:
        return jsonify({
            "status": 'Unauthorized'
        })

@scorer.route('/analyses/<collection>/<analysis_id>/', methods=['GET'])
def _old_retrieve_single_run_analysis(collection=None, analysis_id=None):
    token = request.headers['Authorization']
    user_id = authentication.controllers.authenticate_user(token)
    if user_id: # Passes check - this is a valid token.
        return controllers.retrieve_single_run_analysis(
            database='affect', # Only works with 'affect analysis'
            collection=collection,
            analysis_id=analysis_id,
            user_id=user_id
            )
    else:
        return jsonify({
            "status": 'Unauthorized'
        })

@scorer.route('/analyses/<collection>/stats/', methods=['GET'])
def _old_retrieve_all_run_analyses_statistics(database=None, collection=None):
    token = request.headers['Authorization']
    user_id = authentication.controllers.authenticate_user(token)
    if user_id: # Passes check - this is a valid token.
        return controllers.retrieve_all_run_analyses_statistics(
            database='affect', # Only works with 'affect analysis'
            collection=collection,
            user_id=user_id
            )
    else:
        return jsonify({
            "status": 'Unauthorized'
        })

###
#
# New  Data Management View
#
# Supports a more flexible endpoint structure.
#
###

@scorer.route('/<database>/analyses/<collection>/<page>/<count_per_page>/', methods=['GET'])
def retrieve_all_run_analyses(database=None, collection=None, page=None, count_per_page=None):
    token = request.headers['Authorization']
    user_id = authentication.controllers.authenticate_user(token)
    if user_id: # Passes check - this is a valid token.
        return controllers.retrieve_all_run_analyses(
            database=database,
            collection=collection,
            page=page,
            count_per_page=count_per_page,
            user_id=user_id
            )
    else:
        return jsonify({
            "status": 'Unauthorized'
        })

@scorer.route('/<database>/analyses/<collection>/<analysis_id>/', methods=['GET'])
def retrieve_single_run_analysis(database=None, collection=None, analysis_id=None):
    token = request.headers['Authorization']
    user_id = authentication.controllers.authenticate_user(token)
    if user_id: # Passes check - this is a valid token.
        return controllers.retrieve_single_run_analysis(
            database=database,
            collection=collection,
            analysis_id=analysis_id,
            user_id=user_id
            )
    else:
        return jsonify({
            "status": 'Unauthorized'
        })

@scorer.route('/<database>/analyses/<collection>/stats/', methods=['GET'])
def retrieve_all_run_analyses_statistics(database=None, collection=None):
    token = request.headers['Authorization']
    user_id = authentication.controllers.authenticate_user(token)
    if user_id: # Passes check - this is a valid token.
        return controllers.retrieve_all_run_analyses_statistics(
            database=database,
            collection=collection,
            user_id=user_id
            )
    else:
        return jsonify({
            "status": 'Unauthorized'
        })
