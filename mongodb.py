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


#question 1 
pipeline1 = [
    {"$group": {"_id": "$year", "nombre_films": {"$sum": 1}}},
    {"$sort": {"nombre_films": -1}},
    {"$limit": 1}
]

# Exécuter l'agrégation
resultat1 = list(films_collection.aggregate(pipeline1))

#question 2 
pipeline2 = [
    { "$match": {  "year": { "$gt": 1999 } }},
    { "$count": "nombre_films" }
]

# Exécuter l'agrégation
resultat2 = list(films_collection.aggregate(pipeline2))


#question 3
pipeline3 = [

  {
    "$group": {
      "_id": { "$eq": ["$year", 2007] },  
      "averageVotes": { "$avg": "$Votes" } 
    }
  },
  {
    "$match": {
      "_id": True      }
  }

]

# Exécuter l'agrégation
resultat3 = list(films_collection.aggregate(pipeline3))

#question 4

#question 5

pipeline5 = [
    {"$set": {"genre": {"$split": ["$genre", ","]}}},  
    {"$unwind": "$genre"},  
    {"$group": {"_id": "$genre"}}  
]
 

resultat5 = list(films_collection.aggregate(pipeline5))

#question 6 

pipeline6= [
    { "$match": { "Revenue (Millions)": { "$ne": Null , "$ne": "", "$gt": 0 } } },  
    { "$sort": { "Revenue (Millions)": -1 } },  
    { "$limit": 1 }
]

resultat6 = list(films_collection.aggregate(pipeline6))