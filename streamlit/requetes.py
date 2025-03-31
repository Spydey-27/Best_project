import streamlit as st
from pymongo import MongoClient
from globals import client, db, collection, neo4j_driver
import json
import networkx as nx
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
        st.code('records, summary, keys = neo4j_driver.execute_query("\n\tMATCH (n:Actors)-[:A_jouer]->(f:films) \n\tRETURN n.actor, COUNT(f) AS nb_films \n\tORDER BY nb_films DESC LIMIT 1" , database_="neo4j")')

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
        st.code('records, summary, keys = neo4j_driver.execute_query("\n\tMATCH (n:Actors)-[:A_jouer]->(f:films)<-[:A_jouer]-(a:Actors) \n\tWHERE a.actor = "Anne Hathaway" \n\tRETURN n.actor" , database_="neo4j")')

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
        st.write("L'acteur ayant joué dans des films totalisant le plus de revenu est", records[0][0], "avec", records[0][1], "millions de revenus.")
    with onglet2:
        st.header("Voici notre requête")
        st.code('records, summary, keys = neo4j_driver.execute_query("\n\tMATCH (n:Actors)-[:A_jouer]->(f:films) \n\tRETURN n.actor,  SUM(toInteger(f.Revenue)) AS total_revenue \n\tORDER BY total_revenue DESC" , database_="neo4j")')

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
        st.write("La moyenne de votes des films est de", round(records[0][0]), "votes.")

    with onglet2:
        st.header("Voici notre requête")
        st.code('records, summary, keys = neo4j_driver.execute_query("\n\tMATCH (f:films) \n\tRETURN AVG(toInteger(f.Votes))" , database_="neo4j")')

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
        st.code('records, summary, keys = neo4j_driver.execute_query("\n\tMATCH (n:Genre)<-[g:A_pour_genre]-(f:films) \n\tRETURN n.genre AS Genre, COUNT(f) AS Nombre_de_films \n\tORDER BY Nombre_de_films DESC LIMIT 1" , database_="neo4j")')

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
        st.code('records, summary, keys = neo4j_driver.execute_query("\n\tMATCH (j:Actors {actor: "Julien Oliveira"})-[:A_jouer]->(f:films) \n\tMATCH (a:Actors)-[:A_jouer]->(f) \n\tMATCH (a)-[:A_jouer]->(movie:films) \n\tWHERE NOT a.actor IN ["Ambre Vasseur", "Julien Oliveira"] \n\tRETURN a.actor, movie.title \n\tORDER BY a.actor" , database_="neo4j")')

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
        st.code('records, summary, keys = neo4j_driver.execute_query("\n\tMatch(n:Realisateur) -[:A_Realise]-> (f:films) <- [:A_jouer] - (a:Actors) \n\treturn n.realisateur, Count(DISTINCT a.actor) as ACTEUR_DISTINCT \n\tOrder by ACTEUR_DISTINCT DESC LIMIT 1" , database_="neo4j")')


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
        st.code('records, summary, keys = neo4j_driver.execute_query("\n\tMATCH (m:films)<-[:A_jouer]-(a:Actors)-[:A_jouer]->(other:films) \n\tWHERE m <> other \n\tRETURN m.title, COUNT(DISTINCT other) AS connected_movies \n\tORDER BY connected_movies DESC LIMIT 3" , database_="neo4j")')

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
            st.write(f"- {record[0]} qui a travaillé avec {record[1]} réalisateurs différents.")
    with onglet2:
        st.header("Voici notre requête")
        st.code('records, summary, keys = neo4j_driver.execute_query("\n\tMATCH (n:Realisateur)-[:A_Realise]->(m:films)<-[:A_jouer]-(a:Actors) \n\tRETURN a.actor, COUNT(DISTINCT n.realisateur) AS different_realisator \n\tORDER BY different_realisator DESC LIMIT 5" , database_="neo4j")')

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
        st.code(f'records2, summary2, keys2 = neo4j_driver.execute_query("\n\tMATCH (a:Actors)-[:A_jouer]->(m:films)-[:A_pour_genre]->(g:Genre) \n\tWHERE a.actor = "{actor}" \n\tMATCH (m2:films)-[:A_pour_genre]->(g) \n\tWHERE NOT (a)-[:A_jouer]->(m2) \n\tRETURN m2.title AS Recommandation, COUNT(DISTINCT g) AS Score \n\tORDER BY Score DESC, rand() \n\tLIMIT 5;" , database_="neo4j")')

def question24(onglet1,onglet2,onglet3):
    records, summary, keys = neo4j_driver.execute_query(
        """
        MATCH (r:Realisateur) - [:A_Realise] -> (:films) - [:A_pour_genre] -> (g:Genre)
        Match (r2:Realisateur) - [:A_Realise] -> (:films) - [:A_pour_genre] -> (g)
        Where r <> r2 AND r.realisateur  < r2.realisateur 

        WITH r, r2, COUNT(g) AS nbGenresCommuns
        WHERE nbGenresCommuns >= 2 

        Merge (r) -[:Influence_par]-(r2)
        Return DISTINCT r.realisateur, r2.realisateur
        """
        , database_="neo4j"
    )
    realisateurs = set()

    with onglet1:
        st.header("Voici les réalisateurs qui se sont influencés mutuellement :")
        st.write("On considère que deux films sont similaires dès qu'ils ont au moins 2 genres en commun.")

        for record in records:
            realisateurs.add((record[0], record[1]))

        st.write(f"Sachant que {len(realisateurs)} résultats ont été trouvés, voici les 20 premiers :")
        for i,record in enumerate(realisateurs):
            if i>= 20:
                break
            st.write(f"- {record[0]} et {record[1]} se sont influencés mutuellement.")
    with onglet2:
        st.header("Voici notre requête")
        st.code('records, summary, keys = neo4j_driver.execute_query("\n\tMATCH (r:Realisateur) - [:A_Realise] -> (:films) - [:A_pour_genre] -> (g:Genre) \n\tMatch (r2:Realisateur) - [:A_Realise] -> (:films) - [:A_pour_genre] -> (g) \n\tWhere r <> r2 AND r.realisateur  < r2.realisateur WITH r, r2, COUNT(g) AS nbGenresCommuns WHERE nbGenresCommuns >= 2 \n\tMerge (r) -[:Influence_par]-(r2) \n\tReturn DISTINCT r.realisateur, r2.realisateur" \n\t, database_="neo4j")')

def question25(onglet1,onglet2,onglet3):

    def requetes():
        if actor == actor2 or actor2 == None or actor == None:
            st.write("Les deux acteurs sélectionnés sont identiques.")
            return None
        else:
            records2, summary2, keys2 = neo4j_driver.execute_query(
                f"""
                MATCH (debut:Actors {{actor: "{actor}"}}), (fin:Actors {{actor: "{actor2}"}})
                MATCH path = shortestPath((debut)-[*]-(fin))
                RETURN nodes(path) AS chemin;
                """
                , database_="neo4j",
            )
        return records2

    records, summary, keys = neo4j_driver.execute_query(
        """
        MATCH (n:Actors)-[:A_jouer]->(f:films)
        RETURN n.actor
        """
        , database_="neo4j",
    )
    actor = st.selectbox(
            "Sélectionnez un acteur",
            [record[0] for record in records], index=None
        )
    actor2 = st.selectbox(
            "Sélectionnez un autre acteur",
            [record[0] for record in records], index=None
        )

    
    records2= requetes()
    
        
        
    with onglet1:
            st.header(f"Quel est le plus court chemin entre {actor} et {actor2} ?")
            st.write("Voici le plus court chemin entre les deux acteurs :")
            if records2 == None:
                st.write("Veuillez choisir deux acteurs différents !")
            else:
                  for record in records2:
                    chemin = record['chemin']
                    chemin_affiche = []
                    for i, node in enumerate(chemin):
                        if 'actor' in node._properties:
                            chemin_affiche.append(f"Acteur : {node._properties['actor']}")
                        if 'genre' in node._properties:
                            chemin_affiche.append(f"Genre : {node._properties['genre']}")
                        if 'title' in node._properties:
                            chemin_affiche.append(f"Film : {node._properties['title']}")
                    
                    st.write(" -> ".join(chemin_affiche))

    with onglet2:
        st.header("Voici notre requête")
        st.code('records2, summary2, keys2 = neo4j_driver.execute_query("\n\tMATCH (debut:Actors {actor: "{actor}"}}), (fin:Actors {actor: "{actor2}"}}) \n\tMATCH path = shortestPath((debut)-[*]-(fin)) \n\tRETURN nodes(path) AS chemin;" , \n\tdatabase_="neo4j")')
def question26(onglet1,onglet2,onglet3):

    records, summary, keys = neo4j_driver.execute_query(
        """
        CALL gds.graph.exists('myGraph') YIELD exists
        RETURN exists;
        """
        , database_="neo4j",
    )
    if records[0][0] == False:
      neo4j_driver.execute_query(
            """
            CALL gds.graph.project(
            'myGraph',
            ['Actors','films'],
            'A_jouer'       
            )
            YIELD graphName, nodeCount, relationshipCount;
            """
            , database_="neo4j",
        )
    

    records, summary, keys = neo4j_driver.execute_query(
        """
        CALL gds.louvain.stream('myGraph')
        YIELD nodeId, communityId, intermediateCommunityIds
        WITH gds.util.asNode(nodeId) AS node, communityId
        WHERE node.actor IS NOT NULL
        RETURN node.actor AS name, communityId
        ORDER BY communityId ASC
        """
        , database_="neo4j",
    )

    with onglet1:
        st.header("Voici les communautés d'acteurs :")
        st.write("Il y a", len(set([record[1] for record in records])), "communautés d'acteurs.")
        st.write("On remarquera que certaines communautés sont plus grandes que d'autres. Nous supposons que cela est dû au peu de films présents dans la base de données. Seulement 100 ce qui n'est pas assez représentatif.")
        communaute_dict = {}
        temp = records[0][1]
        temp2 = 1
        communaute_dict[temp2] = []
        for i, record in enumerate(records):
            if record[1] != temp:
                temp = record[1]
                temp2 += 1
                communaute_dict[temp2] = []
            communaute_dict[temp2].append(record[0])
        
        commu = st.selectbox(
            "Sélectionnez une communauté",
            [key for key in communaute_dict.keys()], index=None
        )
        st.write(f"Voici les acteurs de la communauté {commu} :")
        for key, value in communaute_dict.items():
            if key == commu:
                for actor in value:
                    st.write(f"- {actor}")
                break


    with onglet2:
        st.header("Voici notre requête")
        st.code('records, summary, keys = neo4j_driver.execute_query("\n\tCALL gds.graph.exists(\'myGraph\') YIELD exists \n\tRETURN exists;" , database_="neo4j")')
        st.write("Cette requête permet de trouver les communautés d'acteurs dans le graphe.")

def question27(onglet1,onglet2,onglet3):
    records, summary, keys = neo4j_driver.execute_query(
        """
        MATCH (m:films)-[:A_pour_genre]->(g:Genre)<-[:A_pour_genre]-(m2:films)
        WHERE m.Director < m2.Director AND m.Director <> m2.Director 

        WITH m, m2, COUNT(g) AS nbGenresCommuns
        WHERE nbGenresCommuns >= 2
        
        RETURN m.title AS Film1, m2.title AS Film2, rand() AS alea
        ORDER BY alea
        """ 
        , database_="neo4j",
    )
    with onglet1:
        st.header("Quels sont les films qui ont le même genre mais des réalisateurs différents ?")
        films = set()
        for i, record in enumerate(records):
            films.add((record[0], record[1]))
        
        st.write(f"Sachant que {len(films)} résultats ont été trouvés, voici les 20 premiers  :")
        for i,film in enumerate(films):
            if i>= 20:
                break
            st.write(f"- {film[0]} et {film[1]} ont le même genre mais des réalisateurs différents.")
    with onglet2:
        st.header("Voici notre requête")
        st.code('records, summary, keys = neo4j_driver.execute_query("\n\tMATCH (m:films)-[:A_pour_genre]->(g:Genre)<-[:A_pour_genre]-(m2:films) \n\tWHERE m.Director < m2.Director AND m.Director <> m2.Director \n\tWITH m, m2, COUNT(g) AS nbGenresCommuns WHERE nbGenresCommuns >= 2 \n\tRETURN m.title AS Film1, m2.title AS Film2, rand() AS alea \n\tORDER BY alea" , database_="neo4j")')

def question28(onglet1,onglet2,onglet3):
    records, summary, keys = neo4j_driver.execute_query(
        """
        MATCH (n:Actors)-[:A_jouer]->(f:films)
        RETURN n.actor
        """
        , database_="neo4j",
    )
    actor = st.selectbox(
            "Sélectionnez votre acteur préféré",
            [record[0] for record in records]
        )
    records2, summary2, keys2 = neo4j_driver.execute_query(
        f"""
        MATCH (a:Actors)-[:A_jouer]->(m:films)
        WHERE a.actor = "{actor}"
        RETURN m.title AS Recommandation
        LIMIT 5;
        """
        , database_="neo4j",
    )

    with onglet1:
        st.header(f"Tu aimes cet acteur : {actor} ? Voici quelques films que tu pourrais adorer :")
        for record in records2:
            st.write(f"- {record[0]}")
    with onglet2:
        st.header("Voici notre requête")
        st.code(f'records2, summary2, keys2 = neo4j_driver.execute_query("\n\tMATCH (a:Actors)-[:A_jouer]->(m:films) \n\tWHERE a.actor = "{actor}" \n\tRETURN m.title AS Recommandation \n\tLIMIT 5;" , \n\tdatabase_="neo4j")')
def question29(onglet1,onglet2,onglet3):
    records, summary, keys = neo4j_driver.execute_query(
        """
        
        MATCH (m:films)-[:A_pour_genre]->(g:Genre)<-[:A_pour_genre]-(m2:films)
        WHERE m.Director < m2.Director AND m.Director <> m2.Director AND m.year = m2.year and m.rating = m2.rating

        WITH m, m2, COUNT(g) AS nbGenresCommuns
        WHERE nbGenresCommuns >= 2 

        Match (r:Realisateur {realisateur: m.Director})
        Match (r2:Realisateur {realisateur: m2.Director})
        Merge (r) -[:Concurence]-(r2)
        RETURN r.realisateur, r2.realisateur
        """
        , database_="neo4j",
    )


    with onglet1:
        st.header("Voici les réalisateurs qui ont réalisé des films similaires la même année :")
        st.write("On considère que deux films sont similaires dès qu'ils ont au moins 2 genres en commun et la même classification. Actuellement il y a", len(records), ".")
        for record in records:
            st.write(f"- {record[0]} et {record[1]} sont entrés en concurrence.")

    with onglet2:
        st.header("Voici notre requête")
        st.code('records, summary, keys = neo4j_driver.execute_query("\n\tMATCH (m:films)-[:A_pour_genre]->(g:Genre)<-[:A_pour_genre]-(m2:films) \n\tWHERE m.Director < m2.Director AND m.Director <> m2.Director AND m.year = m2.year and m.rating = m2.rating \n\tWITH m, m2, COUNT(g) AS nbGenresCommuns WHERE nbGenresCommuns >= 2 \n\tMatch (r:Realisateur {realisateur: m.Director}) \n\tMatch (r2:Realisateur {realisateur: m2.Director}) \n\tMerge (r) -[:Concurence]-(r2) \n\tRETURN r.realisateur, r2.realisateur" , database_="neo4j")')
def question30(onglet1,onglet2,onglet3):
    pass