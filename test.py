#!/usr/bin/python
# coding: utf-8
from flask import Flask, request, jsonify

app = Flask(__name__)


list_temp=[]
@app.route('/sensor1', methods=['POST','GET'])
def mantap():
    if request.method == 'POST':
        body = request.get_json()
        Temp = body['Temperature']
        Hum = body['Humidity']
        timestamp = body['timestamp']

        #simpan data ke list sementara
        list_temp.append({
                "Temperature":Temp,
                "Humidity" : Hum,
                "Timestamp" : timestamp

        })
        return jsonify({"message" : "Processing Your request", "data" : body}),201
    elif request.method == 'GET':
        return jsonify(list_temp),201


# @app.route('/sensor1', methods=['GET'])
# def data():


@app.route('/sensor1/temperature/avg', methods=['GET'])
def avg():
    if request.method == 'GET':
        if not list_temp :
            return jsonify({"average temperature" : None})
        
        AVG_temp = sum(entry["Temperature"] for entry in list_temp) / len(list_temp)
        return jsonify({"Average Temp" : AVG_temp}) 
    
if __name__ == '__main__':
    app.run(debug=True, port=1280)