from pymongo import MongoClient
from neo4j import GraphDatabase
import os

# Connexion MongoDB 
client = MongoClient("mongodb://mongodb:27017/")
db = client["movies"]
collection = db["films"]

# Connexion Neo4j
uri = "bolt://neo4j:7687"
auth = ("neo4j", os.environ.get("NEO4J_AUTH"))
neo4j_driver = GraphDatabase.driver(uri, auth=auth)

with neo4j_driver.session(database="neo4j") as session:
    neo4j_driver.verify_connectivity()



# La différence entre un driver et une session ?
# Le driver permet de se connecter à une base de données Neo4j.
# Une session est un context pour executer du travail avec un driver. Il permet également de faire des opérations légères.


# Une session est un context pour executer du travail avec un driver.
#
#

##################### SET UP NEO4J #####################

def createdb():
    movie = collection.find({},{ "_id": 1, "title": 1, "year": 1, "Director": 1, "rating": 1, "Revenue (Millions)":1, "Votes":1, "genre":1})
    for i in movie:
        summary = neo4j_driver.execute_query(
            "CREATE (:films {id: $id, title: $title, year: $year, Director: $Director, rating: $rating, Revenue: $Revenue, Votes: $Votes})",
            id = i["_id"],
            title=i["title"],
            year=i["year"],
            Director=i["Director"],
            rating=i["rating"],
            Revenue=i["Revenue (Millions)"],
            Votes=i["Votes"],
            database_="neo4j",
        ).summary      
    
    actors = find_actors()

    for i in actors:
        summary = neo4j_driver.execute_query(
            "CREATE (:Actors {actor: $actor})",
            actor=i,
            database_="neo4j",
        ).summary
    
    find_movies_x_actor()

    membres = ["Julien Oliveira", "Ambre Vasseur"]
    for i in membres:
        summary = neo4j_driver.execute_query(
            "CREATE (:Actors {actor: $nom})",
            nom=i,
            database_="neo4j",
        ).summary
        summary2 = neo4j_driver.execute_query(
            "MATCH (a:Actors {actor: $actor}) MERGE (f:films {title: $title}) MERGE (a)-[:A_jouer]->(f)",
            actor=i,
            title="Passengers",
            database_="neo4j",
        ).summary


    realisator = find_realisator()
    for i in realisator:
        summary = neo4j_driver.execute_query(
            "CREATE (:Realisateur {realisateur: $director})",
            director=i,
            database_="neo4j",
        ).summary

    find_genre()
    director_x_films()


def find_actors():
    acteurs = set() #merci chatgpt! En gros c'est un type de collection qui peut contenir que des valeurs unique
    query = collection.find({},{ "_id": 0, "Actors": 1})
    for i in query:
        resultat = i["Actors"].split(",")
        for j in range(len(resultat)):
            resultat[j] = resultat[j].strip()
        acteurs.update(resultat)
    return list(acteurs)

def find_movies_x_actor():
    actor = find_actors()
    resultat = {}
    for i in range(len(actor)):
        pipeline=[
            {"$match": {"$expr": {"$regexMatch": {
                        "input": "$Actors",
                        "regex": actor[i]  # Vérifie si la chaîne commence par "valeurCherchée"
                    }}}},
            {"$group": {"_id": "$title"}},
        ]
        resultat = list(collection.aggregate(pipeline))
        for j in resultat:
            summary = neo4j_driver.execute_query(
                "MATCH (a:Actors {actor: $actor}) MERGE (f:films {title: $title}) MERGE (a)-[:A_jouer]->(f)",
                actor=actor[i],
                title=j["_id"],
                database_="neo4j",
            ).summary

def find_realisator():
    realisateurs = set()
    query = collection.find({},{ "_id": 0, "Director": 1})
    for i in query:
        realisateurs.add(i["Director"])
    return list(realisateurs)

def find_genre():
    genre_unique = set()
    query = collection.find({},{ "_id": 1, "genre": 1})
    for film in query:
        genres = film["genre"].split(",")
        for genre in genres:
            genre = genre.strip()

            if genre not in genre_unique:
                neo4j_driver.execute_query(
                    "MERGE (:Genre {genre: $genre})",
                    genre=genre,
                    database_="neo4j",
                )
                genre_unique.add(genre)

            neo4j_driver.execute_query(
                """
                MATCH (f:films {id: $id})
                MERGE (g:Genre {genre: $genre})
                MERGE (f)-[:A_pour_genre]->(g)
                """,  
                id=film["_id"],
                genre=genre,
                database_="neo4j",
            )

def director_x_films():
    query = collection.find({},{ "_id": 1, "Director": 1})
    for i in query:
        summary = neo4j_driver.execute_query(
            "MATCH (f:films {id: $id}) MERGE (r:Realisateur {realisateur: $director}) MERGE (r)-[:A_Realise]->(f)",
            id=i["_id"],
            director=i["Director"],
            database_="neo4j",
        ).summary