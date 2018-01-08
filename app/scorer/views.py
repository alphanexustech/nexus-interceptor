from flask import Blueprint
from flask import render_template, redirect, url_for, jsonify, request

import requests, json

from . import controllers
import authentication.controllers

# Databases
from config.databases import affect_analysis

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

@scorer.route('/analyze_emotion_set/', methods=['POST'])
def analyze_emotion_set():
    data = request.get_json()
    return controllers.analyze_emotion_set(data=data)

@scorer.route('/analyses/<collection>/<page>/<count_per_page>/', methods=['GET'])
def retrieve_all_run_analyses(collection=None, page=None, count_per_page=None):
    token = request.headers['Authorization']
    user_id = authentication.controllers.authenticate_user(token)
    if user_id: # Passes check - this is a valid token.
        return controllers.retrieve_all_run_analyses(
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
def retrieve_single_run_analysis(collection=None, analysis_id=None):
    token = request.headers['Authorization']
    user_id = authentication.controllers.authenticate_user(token)
    if user_id: # Passes check - this is a valid token.
        return controllers.retrieve_single_run_analysis(
            collection=collection,
            analysis_id=analysis_id,
            user_id=user_id
            )
    else:
        return jsonify({
            "status": 'Unauthorized'
        })

@scorer.route('/analyses/<collection>/stats/', methods=['GET'])
def retrieve_all_run_analyses_statistics(collection=None):
    token = request.headers['Authorization']
    user_id = authentication.controllers.authenticate_user(token)
    if user_id: # Passes check - this is a valid token.
        return controllers.retrieve_all_run_analyses_statistics(
            collection=collection,
            user_id=user_id
            )
    else:
        return jsonify({
            "status": 'Unauthorized'
        })
