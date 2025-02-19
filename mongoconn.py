from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://ello:N8JKwUQmmhV9w4yH@ellosamsung.jg5zw.mongodb.net/?retryWrites=true&w=majority&appName=ellosamsung"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

#buat database cuy
db = client['DbSamsung']
my_collection = db['SensorData']


#input data
Sensor_1 = {'temperature' : 32, 'Humidity' : 41}
Sensor_2 = {'temperature' : 34, 'Humidity' : 50}
Sensor_3 = {'temperature' : 32, 'Humidity' : 40}

results = my_collection.insert_many([Sensor_1,Sensor_2,Sensor_3]) # untuk memasukkan data
print(results.inserted_ids)

get_result = my_collection.find() # untuk mengambil datanya 
for x in get_result:
    print(x)
