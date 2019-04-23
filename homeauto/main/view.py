'''
Created on Nov 26, 2018

@author: iaskarov
'''

import sys;
from flask import jsonify;
from flask import flash;
from . import main;
from flask import request;
from flask import redirect, g;
from flask import url_for;
from flask import session;
from flask import Response;
from flask import current_app;
from flask import render_template;
from flask import g;
from homeauto import db;
from types import NoneType;
from flask import jsonify;

@main.before_request
def check_db_connection():
    if('db' not in sys.modules):
        from homeauto import db;
    db.validate_connection();

@main.route('/login', methods=['POST', 'GET'])
def login():
    return render_template('login.html');

@main.route('/index', methods=['POST', 'GET'])
def index():
    events = db.get_current_status();
    return render_template('index.html',events=events);

@main.route('/control', methods=['POST', 'GET'])
def control():
    modules = db.get_all_devices();
    return render_template('control.html', modules=modules);

@main.route('/history', methods=['POST', 'GET'])
def history():
    events = db.get_all_activity();
    return render_template('history.html', events=events);

@main.route('/action', methods=['POST'])
def action():

    
    device_id = int(request.form.get('device_id'));
    action = int(request.form.get('action'));
    for idx in current_app.gpio:
        if(device_id == idx.device_id):
            if(action):
                idx.signal();
            else:
                idx.signal(False);
            if(db.toggle_device(device_id, action)):
                db.register_activity(device_id, action);
                return jsonify(error=200);