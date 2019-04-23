'''
Created on Nov 26, 2018

@author: iaskarov
'''

from flask import Blueprint;

main = Blueprint('main', __name__);

from homeauto.main import view;
