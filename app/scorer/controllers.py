from flask import Blueprint
from flask import render_template, redirect, url_for, jsonify, request

import requests, json

# Configuration
from config import configurations

# Databases
from config.databases import affect_analysis

# mongo dependecies
import pymongo
from flask_pymongo import ObjectId

# bson
import json
from bson import json_util

def default():
    return 'Hello Scorer!'

def save_record(collection_name, content, data):

    # IDEA: Not the best way to create a collection if it doesn't exist
    try:
        affect_analysis.db.create_collection(collection_name)
    except Exception as e:
        print(e)

    collection = affect_analysis.db[collection_name]

    # Make sure the username and id are matched, if present
    try:
        content['id'] = data['id']
        content['username'] = data['username']
    except Exception as e:
        content['id'] = None
        content['username'] = None
        print(e)
    collection.insert(content)

    return "Record Saved"

def analyze_emotion_set(data=None):

    data = request.get_json()
    endpoint = 'http://' + configurations.api_ip + ':' + configurations.port + '/core/analyze_emotion_set/' + data.get('emotion_set') + '/'
    r = requests.post(endpoint, json=data)

    # save content
    save_record('beta_records-07jan2018', json.loads(r.content), data)
    # return content
    return jsonify(status="success", data=json.loads(r.content))

def get_total_analysis_count(collection):

    cursor = affect_analysis.db[collection].find().sort('_id', pymongo.DESCENDING); # find all
    data = {}
    data['corpus_length'] = cursor.count()

    return data

def retrieve_all_run_analyses(collection=None, page=None, count_per_page=None):

    x = (int(page) - 1) * int(count_per_page)
    y = int(page) * int(count_per_page)

    cursor = affect_analysis.db[collection].find().sort('_id', pymongo.DESCENDING); # find all
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

    total_analyses = get_total_analysis_count(collection)['corpus_length']

    return jsonify(
            status="success",
            date=configurations.utc,
            stats='stats',
            total_analyses=total_analyses,
            count_per_page=count_per_page,
            data=json.loads(json.dumps(data, default=json_util.default)),
            )

def retrieve_all_run_analyses_statistics(collection=None):

    data = get_total_analysis_count(collection)

    return jsonify(
            status="success",
            date=configurations.utc,
            data=json.loads(json.dumps(data, default=json_util.default)),
            )

def retrieve_single_run_anlysis(collection=None, analysis_id=None):

    result = affect_analysis.db[collection].find_one({"_id": ObjectId(analysis_id)})

    return jsonify(
            status="success",
            date=configurations.utc,
            data=json.loads(json.dumps(result, default=json_util.default)),
            )
