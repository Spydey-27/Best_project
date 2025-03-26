# from neo4j import GraphDatabase

# # URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"
# URI = "neo4j+s://2ea23cf6.databases.neo4j.io"
# AUTH = ("neo4j", "nMA6eFsv5KqeP7RiDVmI41wE67ad3UwPjo_uJPupSzE")

# with GraphDatabase.driver(URI, auth=AUTH) as driver:
#     driver.verify_connectivity()
#     print("connection reussie")
    
    
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
uri = "mongodb+srv://vasseur:aled@cluster0.bgn7j.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# # Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)


db = client["entertainement"]
films_collection = db["films"]

pipeline = [
    {"$group": {"_id": "$year", "nombre_films": {"$sum": 1}}},
    {"$sort": {"nombre_films": -1}},
    {"$limit": 1}
]

# Exécuter l'agrégation
resultat = list(films_collection.aggregate(pipeline))

