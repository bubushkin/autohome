'''
Created on Nov 26, 2018

@author: iaskarov
'''

import logging;
from flask import Flask
from flask_bootstrap import Bootstrap;
from homeauto.config.config import config;
from homeauto.db.dbfactory import DBFactory;
from homeauto.model import GPIODevice;
from homeauto.model import Camera;
from logging.handlers import RotatingFileHandler;
from logging import Formatter;
from homeauto.engine import Visual;
from homeauto.engine import Light;

import json;
import RPi.GPIO as GPIO;

db = None;
bootstrap = Bootstrap()

def spawn_workers(app):
    
    pir = [];
    for idx in app.devices:
        if('PIR' in idx.device_name):
            pir.append(idx);
    
    thvisual = Visual("camera_worker", 0x1, app.camera, pir[0x0]);

def load_config(app):
    fp = open(app.config["DEVICE_CONF"], 'r');
    conf = json.load(fp);
    fp.close();
    return conf;
    
def register_device(json):
    db.register_device(json);
    return db.get_device_by_id(json.get('device_id'));
    
def init_devices(app):
    
    app.gpio = [];
    app.camera = None;
    app.display = None;

    GPIO.setwarnings(False);
    GPIO.setmode(GPIO.BOARD);
    
    conf = load_config(app);
    
    #init gpio devices
    for idx in conf['gpio']:
        rset = register_device(idx);
        app.gpio.append(GPIODevice(rset, GPIO));

    #init camera
    rset = register_device(conf['csi'])
    app.camera = Camera(rset);
    
def initialize(config_name):
    app = Flask(__name__);
    app.config.from_object(config[config_name])

    global db;
    with app.app_context():
        db = DBFactory(app.config);
        db.reset_db();
        
    handler = RotatingFileHandler('homeauto_execution.log', maxBytes=1000000, backupCount=5);
    handler.setFormatter(Formatter("[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s"));
    handler.setLevel(config[config_name].LOG_LEVEL);

    app.logger.addHandler(handler);
    
    bootstrap.init_app(app)
    
    from .main import main as main_blueprint;
    app.register_blueprint(main_blueprint);

    return app;