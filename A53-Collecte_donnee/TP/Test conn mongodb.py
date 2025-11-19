from pymongo import MongoClient

connection_string = "mongodb+srv://MB:mb@cluster0.luxsp4o.mongodb.net/"

client = MongoClient(connection_string)
print(client.list_database_names())