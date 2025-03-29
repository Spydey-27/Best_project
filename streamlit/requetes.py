import streamlit as st
from pymongo import MongoClient
from globals import client, db, collection, neo4j_driver
import json
films_collection = collection

#
## Exécuter l'agrégation
#
##question 4
#
##question 5
#
pipeline5 = [
    {"$set": {"genre": {"$split": ["$genre", ","]}}},  
    {"$unwind": "$genre"},  
    {"$group": {"_id": "$genre"}}  
]
# 
#
#resultat5 = list(films_collection.aggregate(pipeline5))
#
##question 6 
#
#pipeline6= [
#    { "$match": { "Revenue (Millions)": { "$ne": Null , "$ne": "", "$gt": 0 } } },  
#    { "$sort": { "Revenue (Millions)": -1 } },  
#    { "$limit": 1 }
#]
#
#resultat6 = list(films_collection.aggregate(pipeline6))
#
#


def question1(onglet1,onglet2,onglet3):
    pipeline1 = [
    {"$group": {"_id": "$year", "nombre_films": {"$sum": 1}}},
    {"$sort": {"nombre_films": -1}},
    {"$limit": 1}
]
    resultat1 = list(films_collection.aggregate(pipeline1))
    with onglet1:
        st.header("Afficher l'année où le plus grand nombre de films ont été sortis.")
        st.write("C'est en", resultat1[0]["_id"], "qu'il y a eu le plus grand nombre de films sortis. Avec", resultat1[0]["nombre_films"], "films.")
        st.write("C'est plutôt bien  !")
        
    with onglet2:
        st.header("Voici notre requête")
        formatted_pipeline = json.dumps(pipeline1, indent=1)
        st.code('resultat1 = list(films_collection.aggregate(pipeline1))')
        st.write("Le pipeline1 est :")
        st.code(formatted_pipeline, language="json")

    with onglet3:
        st.write("Pas de visualisation ici :(")

def question2(onglet1,onglet2,onglet3):
    pipeline = [
    { "$match": {  "year": { "$gt": 1999 } }},
    { "$count": "nombre_films" }
    ]
    resultat = list(films_collection.aggregate(pipeline))
    with onglet1:
        st.header("Quel est le nombre de films sortis après 1999 ?")
        st.write("Il y en a eu ", resultat[0]["nombre_films"], "sortis après 1999.")
        
    with onglet2:
        st.header("Voici notre requête")
        formatted_pipeline = json.dumps(pipeline, indent=1)
        st.code('resultat = list(films_collection.aggregate(pipeline2))')
        st.write("Le pipeline est :")
        st.code(formatted_pipeline, language="json")

    with onglet3:
        st.write("Pas de visualisation ici :(")

def question3(onglet1,onglet2,onglet3):
    pipeline = [
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

    resultat = list(films_collection.aggregate(pipeline))
    with onglet1:
        st.header("Quelle est la moyenne des votes des films sortis en 2007 ?")
        st.write("La moyenne est de ", resultat[0]["averageVotes"])
        
    with onglet2:
        st.header("Voici notre requête")
        formatted_pipeline = json.dumps(pipeline, indent=1)
        st.code('resultat = list(films_collection.aggregate(pipeline3))')
        st.write("Le pipeline est :")
        st.code(formatted_pipeline, language="json")

    with onglet3:
        st.write("Pas de visualisation ici :(")

def question4(onglet1,onglet2,onglet3):
    realisateurs = set()
    query = collection.find({},{ "_id": 0, "Director": 1})
    for i in query:
        realisateurs.add(i["Director"])
    realisateurs = list(realisateurs)
    st.write(realisateurs)

def question5(onglet1,onglet2,onglet3):
    pipeline5 = [
        {"$set": {"genre": {"$split": ["$genre", ","]}}},  
        {"$unwind": "$genre"},  
        {"$group": {"_id": "$genre"}}  
    ]

    resultat5 = list(films_collection.aggregate(pipeline5))
    for i in range(len(resultat5)):
        resultat5[i] = resultat5[i]["_id"]


    with onglet1:
        st.header("Quels sont les genres de films disponibles dans la base ?")
        st.write("Les genres de films disponibles sont :")
        for genre in resultat5:
            st.write(f"- {genre}")

    with onglet2:
        st.header("Voici notre requête")
        formatted_pipeline = json.dumps(pipeline5, indent=1)
        st.code('resultat5 = list(films_collection.aggregate(pipeline5))')
        st.write("Le pipeline5 est :")
        st.code(formatted_pipeline, language="json")


def question6(onglet1,onglet2,onglet3):
    pass

def question7(onglet1,onglet2,onglet3):
    pass

def question8(onglet1,onglet2,onglet3):
    pass

def question9(onglet1,onglet2,onglet3):
    pass

def question10(onglet1,onglet2,onglet3):
    pass

def question11(onglet1,onglet2,onglet3):
    pass

def question12(onglet1,onglet2,onglet3):
    pass

def question13(onglet1,onglet2,onglet3):
    pass

def question14(onglet1,onglet2,onglet3):
    records, summary, keys = neo4j_driver.execute_query(
        "MATCH (n:Actors)-[:A_jouer]->(f:films) RETURN n.actor, COUNT(f) AS nb_films ORDER BY nb_films DESC LIMIT 1" ,
            database_="neo4j",
        )
    
    with onglet1:
        st.header("Quel acteur a joué dans le plus de films ?")
        st.write("L'acteur qui a joué dans le plus de films est", records[0][0], "avec", records[0][1], "films.")

    with onglet2:
        st.header("Voici notre requête")
        st.code('records, summary, keys = neo4j_driver.execute_query("MATCH (n:Actors)-[:A_jouer]->(f:films) RETURN n.actor, COUNT(f) AS nb_films ORDER BY nb_films DESC LIMIT 1" , database_="neo4j")')

def question15(onglet1,onglet2,onglet3):
    records, summary, keys = neo4j_driver.execute_query(
        """
        MATCH (n:Actors)-[:A_jouer]->(f:films)<-[:A_jouer]-(a:Actors)
        WHERE a.actor = "Anne Hathaway"
        RETURN n.actor
        """ ,
            database_="neo4j",
        )
    
    with onglet1:
        st.header("Quels sont les acteurs qui ont joué avec Anne Hathaway ?")
        for record in records:
            st.write(f"- {record[0]}")

    with onglet2:
        st.header("Voici notre requête")
        st.code('records, summary, keys = neo4j_driver.execute_query("MATCH (n:Actors)-[:A_jouer]->(f:films)<-[:A_jouer]-(a:Actors) WHERE a.actor = "Anne Hathaway" RETURN n.actor" , database_="neo4j")')

def question16(onglet1,onglet2,onglet3):

    records, summary, keys = neo4j_driver.execute_query(
        """
        MATCH (n:Actors)-[:A_jouer]->(f:films)
        RETURN n.actor,  SUM(toInteger(f.Revenue)) AS total_revenue
        ORDER BY total_revenue DESC
        """ ,
            database_="neo4j",
        )
    
    with onglet1:
        st.header("Quel est l'acteur ayant joué dans des films totalisant le plus de revenu ?")
        st.write("L'acteur ayant joué dans des films totalisant le plus de revenu est", records[0][0], "avec", records[0][1], "milions de revenus.")
    with onglet2:
        st.header("Voici notre requête")
        st.code('records, summary, keys = neo4j_driver.execute_query("MATCH (n:Actors)-[:A_jouer]->(f:films) RETURN n.actor,  SUM(toInteger(f.Revenue)) AS total_revenue ORDER BY total_revenue DESC" , database_="neo4j")')

def question17(onglet1,onglet2,onglet3):
    
    records, summary, keys = neo4j_driver.execute_query(
        """
        MATCH (f:films)
        RETURN AVG(toInteger(f.Votes))
        """ ,
            database_="neo4j",
        )
    with onglet1:
        st.header("Quelle est la moyenne de votes des films ?")
        st.write("La moyenne de votes des films est de", records[0][0])

    with onglet2:
        st.header("Voici notre requête")
        st.code('records, summary, keys = neo4j_driver.execute_query("MATCH (f:films) RETURN AVG(toInteger(f.Votes))" , database_="neo4j")')
        
def question18(onglet1,onglet2,onglet3):
    records, summary, keys = neo4j_driver.execute_query(
        """
        MATCH (n:Genre)<-[g:A_pour_genre]-(f:films)
        RETURN n.genre AS Genre, COUNT(f) AS Nombre_de_films
        ORDER BY Nombre_de_films DESC LIMIT 1
        """ ,
            database_="neo4j",
        )
    with onglet1:
        st.header("Quel est le genre de film le plus représenté ?")
        st.write("Le genre de film le plus représenté est", records[0][0], "avec", records[0][1], "films.")
    with onglet2:
        st.header("Voici notre requête")
        st.code('records, summary, keys = neo4j_driver.execute_query("MATCH (n:Genre)<-[g:A_pour_genre]-(f:films) RETURN n.genre AS Genre, COUNT(f) AS Nombre_de_films ORDER BY Nombre_de_films DESC LIMIT 1" , database_="neo4j")')

def question19(onglet1,onglet2,onglet3):
    records, summary, keys = neo4j_driver.execute_query(
        """
        MATCH (j:Actors {actor: "Julien Oliveira"})-[:A_jouer]->(f:films)
        MATCH (a:Actors)-[:A_jouer]->(f)
        MATCH (a)-[:A_jouer]->(movie:films)
        WHERE NOT a.actor IN ["Ambre Vasseur", "Julien Oliveira"]
        RETURN a.actor, movie.title
        ORDER BY a.actor
        """ ,
            database_="neo4j",
        )
    with onglet1:
        st.header("Les acteurs qui ont joué dans le film Passengers ont joué dans les films suivants :")
        for record in records:
            st.write(f"- {record[0]} a joué dans {record[1]}")
    with onglet2:
        st.header("Voici notre requête")
        st.write("La requête est un peu plus complexe, mais elle est la suivante :")
        st.code('records, summary, keys = neo4j_driver.execute_query("MATCH (j:Actors {actor: "Julien Oliveira"})-[:A_jouer]->(f:films) MATCH (a:Actors)-[:A_jouer]->(f) MATCH (a)-[:A_jouer]->(movie:films) WHERE NOT a.actor IN ["Ambre Vasseur", "Julien Oliveira"] RETURN a.actor, movie.title ORDER BY a.actor" , database_="neo4j")')

def question20(onglet1,onglet2,onglet3):
    records, summary, keys = neo4j_driver.execute_query(
        """
        Match(n:Realisateur) -[:A_Realise]-> (f:films) <- [:A_jouer] - (a:Actors)
        return n.realisateur, Count(DISTINCT a.actor) as ACTEUR_DISTINCT
        Order by ACTEUR_DISTINCT DESC LIMIT 1
        """
        , database_="neo4j",
    )
    with onglet1:
        st.header("Quel est le réalisateur ayant dirigé le plus d'acteurs différents ?")
        st.write("Le réalisateur ayant dirigé le plus d'acteurs différents est", records[0][0], "avec", records[0][1], "acteurs différents.")
    with onglet2:
        st.header("Voici notre requête")
        st.code('records, summary, keys = neo4j_driver.execute_query("Match(n:Realisateur) -[:A_Realise]-> (f:films) <- [:A_jouer] - (a:Actors) return n.realisateur, Count(DISTINCT a.actor) as ACTEUR_DISTINCT Order by ACTEUR_DISTINCT DESC LIMIT 1" , database_="neo4j")')


def question21(onglet1,onglet2,onglet3):
    records, summary, keys = neo4j_driver.execute_query(
        """
        MATCH (m:films)<-[:A_jouer]-(a:Actors)-[:A_jouer]->(other:films)
        WHERE m <> other
        RETURN m.title, COUNT(DISTINCT other) AS connected_movies
        ORDER BY connected_movies DESC LIMIT 3
        """
        , database_="neo4j",
    )
    with onglet1:
        st.header("Quels sont les films qui ont le plus d'acteurs en commun avec d'autres films ?")
        for record in records:
            st.write(f"- {record[0]} a {record[1]} acteurs en commun avec d'autres films.")
    with onglet2:
        st.header("Voici notre requête")
        st.code('records, summary, keys = neo4j_driver.execute_query("MATCH (m:films)<-[:A_jouer]-(a:Actors)-[:A_jouer]->(other:films) WHERE m <> other RETURN m.title, COUNT(DISTINCT other) AS connected_movies ORDER BY connected_movies DESC LIMIT 3" , database_="neo4j")')

def question22(onglet1,onglet2,onglet3):
    records, summary, keys = neo4j_driver.execute_query(
        """
        MATCH (n:Realisateur)-[:A_Realise]->(m:films)<-[:A_jouer]-(a:Actors)
        RETURN a.actor, COUNT(DISTINCT n.realisateur) AS different_realisator
        ORDER BY different_realisator DESC LIMIT 5
        """
        , database_="neo4j",
    )

    with onglet1:
        st.header("Quels sont les acteurs ayant travaillé avec le plus de réalisateurs différents ?")
        st.write("Les acteurs ayant travaillé avec le plus de réalisateurs différents sont :")
        for record in records:
            st.write(f"- {record[0]} a travaillé avec {record[1]} réalisateurs différents.")
    with onglet2:
        st.header("Voici notre requête")
        st.code('records, summary, keys = neo4j_driver.execute_query("MATCH (n:Realisateur)-[:A_Realise]->(m:films)<-[:A_jouer]-(a:Actors) RETURN a.actor, COUNT(DISTINCT n.realisateur) AS different_realisator ORDER BY different_realisator DESC LIMIT 5" , database_="neo4j")')

def question23(onglet1,onglet2,onglet3):
    records, summary, keys = neo4j_driver.execute_query(
        """
        MATCH (n:Actors)-[:A_jouer]->(f:films)
        RETURN n.actor
        """
        , database_="neo4j",
    )
    actor = st.selectbox(
            "Sélectionnez un acteur",
            [record[0] for record in records]
        )
    records2, summary2, keys2 = neo4j_driver.execute_query(
        f"""
        MATCH (a:Actors)-[:A_jouer]->(m:films)-[:A_pour_genre]->(g:Genre)
        WHERE a.actor = "{actor}"
        MATCH (m2:films)-[:A_pour_genre]->(g)
        WHERE NOT (a)-[:A_jouer]->(m2)
        RETURN m2.title AS Recommandation, COUNT(DISTINCT g) AS Score
        ORDER BY Score DESC, rand()
        LIMIT 5;
        """
        , database_="neo4j",
    )

    with onglet1:
        st.header(f"Quels sont les films recommandés pour {actor} ?")
        for record in records2:
            st.write(f"- {record[0]}")
    with onglet2:
        st.header("Voici notre requête")
        st.code(f'records2, summary2, keys2 = neo4j_driver.execute_query("MATCH (a:Actors)-[:A_jouer]->(m:films)-[:A_pour_genre]->(g:Genre) WHERE a = "{actor}" MATCH (m2:films)-[:A_pour_genre]->(g) WHERE NOT (a)-[:A_jouer]->(m2) RETURN m2.title AS Recommandation, COUNT(DISTINCT g) AS Score ORDER BY Score DESC, rand() LIMIT 5;" , database_="neo4j")')

def question24(onglet1,onglet2,onglet3):
    pass

def question25(onglet1,onglet2,onglet3):
    pass

def question26(onglet1,onglet2,onglet3):
    pass

def question27(onglet1,onglet2,onglet3):
    pass

def question28(onglet1,onglet2,onglet3):
    pass

def question29(onglet1,onglet2,onglet3):
    pass

def question30(onglet1,onglet2,onglet3):
    pass