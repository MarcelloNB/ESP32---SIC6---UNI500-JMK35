#!/usr/bin/python
# coding: utf-8
from flask import Flask, request, jsonify
app = Flask(__name__)

#PYMONGO SECTION
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://ello:N8JKwUQmmhV9w4yH@ellosamsung.jg5zw.mongodb.net/?retryWrites=true&w=majority&appName=ellosamsung"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

#buat database cuy
db = client['DbSamsung']
my_collection = db['SensorData']

def store_data(data):
    results = my_collection.insert_one(data) # untuk memasukkan data
    print(results.inserted_id)
    return results.inserted_id

def get_data():
    get_result = my_collection.find() # untuk mengambil datanya 
    return get_result

@app.route('/sensor1', methods=['POST','GET'])
def mantap():
    if request.method == 'POST':
        body = request.get_json()
        Temp = body['Temperature']
        Hum = body['Humidity']
        timestamp = body['timestamp']
        data_final = {
            #simpan data ke list sementara
                "Temperature":Temp,
                "Humidity" : Hum,
                "Timestamp" : timestamp

        }

        id = store_data(data_final)
        return {
            "message" : f"Processing Your request with id {id}"
            },201
    
    elif request.method == 'GET':
        return jsonify(message = "You get the data."),201


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