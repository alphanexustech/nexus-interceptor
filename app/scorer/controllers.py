from flask import Blueprint
from flask import render_template, redirect, url_for, jsonify, request

import requests, json

# Configuration
from config import configurations

# Databases
from config.databases import affect_analysis
from config.databases import role_analysis

# mongo dependencies
import pymongo
from flask_pymongo import ObjectId

# bson
import json
from bson import json_util

# Date
from datetime import datetime

def default():
    return 'Hello Scorer!'

###
#
# Affective Computing
#
###

def analyze_emotion_set(data=None):

    data = request.get_json()
    endpoint = 'http://' + configurations.api_ip + ':' + configurations.port + '/core/analyze_emotion_set/' + data.get('emotion_set') + '/'
    r = requests.post(endpoint, json=data)

    # save content
    save_record('affect', configurations.analysis_collection, json.loads(r.content), data)
    # return content
    return jsonify(status="success", data=json.loads(r.content))

###
#
# Role Computing
#
###

def analyze_role_set(data=None):

    data = request.get_json()
    endpoint = 'http://' + configurations.api_ip + ':' + configurations.role_port + '/scorer/' + data.get('role_set') + '/'
    r = requests.post(endpoint, json=data)

    # save content
    save_record('role', configurations.role_analysis_collection, json.loads(r.content), data)
    # return content
    return jsonify(status="success", data=json.loads(r.content))

###
#
# Data Management
#
###

def save_record(database, collection_name, content, data):

    # IDEA: Not the best way to create a collection if it doesn't exist
    collection = ''
    if database == 'affect':
        try:
            affect_analysis.db.create_collection(collection_name)
        except Exception as e:
            print(e)
        collection = affect_analysis.db[collection_name]
    elif database == 'role':
        try:
            role_analysis.db.create_collection(collection_name)
        except Exception as e:
            print(e)
        collection = role_analysis.db[collection_name]
    else:
        return "Record Save Failed"


    # Make sure the username and id are matched, if present
    try:
        content['user_id'] = data['id']
        content['username'] = data['username']
    except Exception as e:
        content['user_id'] = None
        content['username'] = None
        print(e)
    collection.insert(content)

    return "Record Saved"

def get_total_analysis_count(database, collection, user_id):

    cursor = []
    if database == 'affect':
        cursor = affect_analysis.db[collection].find({"user_id": user_id}).sort('_id', pymongo.DESCENDING); # find all
    elif database == 'role':
        cursor = role_analysis.db[collection].find({"user_id": user_id}).sort('_id', pymongo.DESCENDING); # find all
    else:
        return {}
    data = {}
    data['corpus_length'] = cursor.count()

    return data


def retrieve_all_run_analyses_statistics(database=None, collection=None, user_id=None):

    data = get_total_analysis_count(database, collection, user_id)
    utc = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

    return jsonify(
            status="success",
            date=utc,
            data=json.loads(json.dumps(data, default=json_util.default)),
            )

def retrieve_all_run_analyses(database=None, collection=None, page=None, count_per_page=None, user_id=None):

    x = (int(page) - 1) * int(count_per_page)
    y = int(page) * int(count_per_page)
    cursor = []
    if database == 'affect':
        cursor = affect_analysis.db[collection].find({"user_id": user_id}).sort('_id', pymongo.DESCENDING); # find all
    elif database == 'role':
        cursor = role_analysis.db[collection].find({"user_id": user_id}).sort('_id', pymongo.DESCENDING); # find all
    else:
        return jsonify(
                status="failure"
               )

    data = []
    for i in cursor[x:y]:
        truncated_emotion_set = []
        for affect in i['emotion_set']:
            truncated_emotion_set.append({
                "emotion": affect['emotion'],
                "normalized_r_score": affect['normalized_r_score'],
            })
        # Improve run time by only returning back a subset of the emotion_set scoring
        i['emotion_set'] = truncated_emotion_set
        # Return back only the first 100 at most characters
        if len(i['doc']) > 400:
            i['doc'] = i['doc'][0:400] + '...'
        data.append(i)

    total_analyses = get_total_analysis_count(collection, user_id)['corpus_length']
    utc = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

    return jsonify(
            status="success",
            date=utc,
            stats='stats',
            total_analyses=total_analyses,
            count_per_page=count_per_page,
            data=json.loads(json.dumps(data, default=json_util.default)),
            )

def retrieve_single_run_analysis(database=None, collection=None, analysis_id=None, user_id=None):

    result = []
    if database == 'affect':
        result = affect_analysis.db[collection].find_one({"_id": ObjectId(analysis_id), "user_id": user_id})
    elif database == 'role':
        result = role_analysis.db[collection].find_one({"_id": ObjectId(analysis_id), "user_id": user_id})
    else:
        return jsonify(
                status="failure"
               )

    utc = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    return jsonify(
            status="success",
            date=utc,
            data=json.loads(json.dumps(result, default=json_util.default)),
            )
