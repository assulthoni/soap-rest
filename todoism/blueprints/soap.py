# -*- coding: utf-8 -*-
"""test"""
from suds.client import Client
from flask import render_template, Blueprint, current_app, make_response, jsonify
from flask_babel import _
from flask_login import current_user
from flask import request, redirect, url_for
from todoism.extensions import db

soap_bp = Blueprint('soap', __name__)

@soap_bp.route('/time')
def getCurrentTime():
    """Consume SOAP SERVER"""
    hello_client = Client('http://localhost:7789/?wsdl')
    time = hello_client.service.getTime()
    return jsonify({'current_time' : time})

@soap_bp.route('/soap', methods=['GET'])
def index():
    return render_template('soap.html')

@soap_bp.route('/form', methods=['GET'])
def form():
    name = request.args['userInput']
    times = request.args['times']
    hello_client = Client('http://localhost:7789/?wsdl')
    hello = hello_client.service.say_hello(name, times)
    data = Client.dict(hello)
    return render_template('result_soap.html', data=data, xml=hello_client.__str__())