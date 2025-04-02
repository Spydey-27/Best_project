import streamlit as st
from pymongo import MongoClient
from globals import client, db, collection, neo4j_driver
import json
import networkx as nx
films_collection = collection
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr, spearmanr


def question1(onglet1,onglet2,onglet3):
    """
    Question 1 : Quelle est l'année où le plus grand nombre de films ont été sortis ?
    """
    pipeline1 = [
    {"$group": {"_id": "$year", "nombre_films": {"$sum": 1}}},
    {"$sort": {"nombre_films": -1}},
    {"$limit": 1}
]
    resultat1 = list(films_collection.aggregate(pipeline1))
    with onglet1:
        st.header("Afficher l'année où le plus grand nombre de films ont été sortis.") #Comptage du nombre de film par anné
        st.write("C'est en", resultat1[0]["_id"], "qu'il y a eu le plus grand nombre de films sortis. Avec", resultat1[0]["nombre_films"], "films.") #Tri par ordre décroissant 
        st.write("C'est un bon début !") #Sélection du premier
        
    with onglet2:
        st.header("Voici notre requête")
        formatted_pipeline = json.dumps(pipeline1, indent=1)
        st.code('resultat1 = list(films_collection.aggregate(pipeline1))')
        st.write("Le pipeline1 est :")
        st.code(formatted_pipeline, language="json")

    with onglet3:
        st.write("Pas de visualisation ici :(")

def question2(onglet1,onglet2,onglet3):
    """
    Question 2 : Quel est le nombre de films sortis après 1999 ?
    """
    pipeline = [
        { "$match": {  "year": { "$gt": 1999 } }}, #Selectionne les années au dessus de 1999
        { "$count": "nombre_films" } #Compte le nombre de film
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
    """
    Question 3 : Quelle est la moyenne des votes des films sortis en 2007 ?
    """

    pipeline = [
    {
        "$group": {
        "_id": { "$eq": ["$year", 2007] },  #Selection des films seulement sorti en 2007
        "averageVotes": { "$avg": "$Votes" } #Moyenne des Votes
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
    """
    Question 4 : Quel est le nombre de films sortis par année ?
    """ 
    pipeline = [
    {"$match": {"year": {"$ne": None, "$exists": True}}},  # Exclure années vides
    {"$group": {"_id": "$year", "nombreFilms": {"$sum": 1}}},
    {"$sort": {"_id": 1}}  # Trier par année
]
    result = list(films_collection.aggregate(pipeline))

    df = pd.DataFrame(result)
    df.rename(columns={"_id": "Année", "nombreFilms": "Nombre de films"}, inplace=True)
    
    with onglet1:
        st.header("Affichez un histogramme qui permet de visualiser le nombres de films par année.")
        st.write("L'histogramme est le suivant : ")
        
        with st.container():
            st.write("Cet histogramme montre l'évolution du nombre de films produits chaque année.")
        
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.barplot(x=df["Année"], y=df["Nombre de films"], color="skyblue", ax=ax)
            
            # Personnalisation
            ax.set_xlabel("Année")
            ax.set_ylabel("Nombre de films")
            ax.set_title("Nombre de films produits par année")
            plt.xticks(rotation=45)
            plt.grid(axis="y", linestyle="--", alpha=0.7)
            
            st.pyplot(fig)
    
    with onglet2:
        st.header("Voici notre requête")
        formatted_pipeline = json.dumps(pipeline, indent=1)
        st.code('resultat = list(films_collection.aggregate(pipeline))')
        st.write("Le pipeline est :")
        st.code(formatted_pipeline, language="json")
        

def question5(onglet1,onglet2,onglet3):
    """
    Question 5 : Quels sont les genres de films disponibles dans la base ?
    """
    pipeline5 = [
        {"$set": {"genre": {"$split": ["$genre", ","]}}},    #Sépare les différents genre des films
        {"$unwind": "$genre"},  
        {"$group": {"_id": "$genre"}}  
    ]

    resultat5 = list(films_collection.aggregate(pipeline5))
    for i in range(len(resultat5)):
        resultat5[i] = resultat5[i]["_id"]#Liste tout les genres


    with onglet1:
        st.header("Quels sont les genres de films disponibles dans la base ?")
        st.write("Les genres de films disponibles sont :")
        for genre in resultat5:
            st.write(f"- {genre}")

    with onglet2:
        st.header("Voici notre requête")
        formatted_pipeline = json.dumps(pipeline5, indent=1)
        st.code('resultat5 = list(films_collection.aggregate(pipeline5))')
        st.write("Le pipeline est :")
        st.code(formatted_pipeline, language="json")


def question6(onglet1,onglet2,onglet3):
    """
    Question 6 : Quel est le film qui a généré le plus de revenu ?
    """
    pipeline6= [
    { "$match": { "Revenue (Millions)": { "$ne": None , "$ne": "", "$gt": 0 } } },   #Non Sélection des Revenus non nuls 
    { "$sort": { "Revenue (Millions)": -1 } },  #Tri par revenus décroissant 
    { "$limit": 1 }#Sélection du premier
    ]

    resultat6 = list(films_collection.aggregate(pipeline6))
    
    with onglet1:
        st.header("Quel est le film qui a généré le plus de revenu.")
        st.write("Le film qui a généré le plus de revenus est ", resultat6[0]["title"])
    
    with onglet2:
        st.header("Voici notre requête")
        formatted_pipeline = json.dumps(pipeline6, indent=1)
        st.code('resultat6 = list(films_collection.aggregate(pipeline6))')
        st.write("Le pipeline est :")
        st.code(formatted_pipeline, language="json")
        

def question7(onglet1,onglet2,onglet3):
    """
    Question 7 : Quels sont les réalisateurs ayant réalisé plus de 5 films dans la base de données ?
    """
    
    pipeline7= [

    { "$group": {"_id": "$Director","nombreFilms": { "$sum": 1 } }}, #Extraction des Réalisateur et somme du nombre de leur films
    { "$match": { "nombreFilms": { "$gt": 5 } }},#Sélection de ceux qui en ont 5
    { "$sort": { "nombreFilms": -1 } }#Ordre décroissant

    ]

    resultat7 = list(films_collection.aggregate(pipeline7))

    with onglet1:
        st.header("Quels sont les réalisateurs ayant réalisé plus de 5 films dans la base de données ?")
        
        if resultat7:
            for realisateur in resultat7:
                st.write(f"{realisateur['_id']} - {realisateur['nombreFilms']} films")
        else:
            st.write("Aucun réalisateur n'a réalisé plus de 5 films dans la base. Nolan est à selement 4 ;)")

    with onglet2:
        st.header("Voici notre requête")
        formatted_pipeline = json.dumps(pipeline7, indent=1)
        st.code('resultat7 = list(films_collection.aggregate(pipeline7))')
        st.write("Le pipeline est :")
        st.code(formatted_pipeline, language="json")
        


def question8(onglet1,onglet2,onglet3):
    """
    Question 8 : Quel est le genre de film qui rapporte en moyenne le plus de revenus ?
    """
    pipeline = [
        { 
            "$match": { 
                "Revenue (Millions)": { "$ne": None, "$ne": "", "$exists": True }  # Exclure revenus vides
            }
        },
        { 
            "$addFields": { 
                "revenueNum": { "$toDouble": "$Revenue (Millions)" },  # Convertir en nombre
                "genreList": { "$split": ["$genre", ","] }  # Transformer en liste
            }
        },
        { 
            "$unwind": "$genreList"  
        },
        { 
            "$group": {"_id": "$genreList",  "revenuMoyen": { "$avg": "$revenueNum" }  }
        },
        { 
            "$sort": { "revenuMoyen": -1 }  
        },
        {"$limit": 1}
    ]

    result = films_collection.aggregate(pipeline)
    
    with onglet1:
        st.header("Quel est le genre de film qui rapporte en moyenne le plus de revenus ?")
        
        for genre_data in result:
            genre = genre_data["_id"]
            revenu_moyen = round(genre_data["revenuMoyen"], 2)  
    
            st.write(f" Le genre qui génère le plus de revenus en moyenne est **{genre}** avec **{revenu_moyen}Millions**")
                
    with onglet2:
        st.header("Voici notre requête")
        formatted_pipeline = json.dumps(pipeline, indent=1)
        st.code('result = list(films_collection.aggregate(pipeline))')
        st.write("Le pipeline est :")
        st.code(formatted_pipeline, language="json")



def question9(onglet1,onglet2,onglet3):
    """
    Question 9 : Quels sont les 3 films les mieux notés (rating) pour chaque décennie (1990-1999, 2000-2009,etc.) ?
    """
    pipeline = [
    { 
        "$match": { 
            "year": { "$ne": None, "$exists": True },
            "Votes": { "$ne": None, "$ne": "", "$exists": True }#Exclusion des données nulles ou inexistantes
        }
    },
    { 
        "$addFields": { 
            "votesNum": { 
                "$convert": { 
                    "input": "$Votes", 
                    "to": "int", 
                    "onError": None
                }
            },
            "decade": { 
                "$subtract": [ { "$toInt": "$year" }, { "$mod": [{ "$toInt": "$year" }, 10] } ] #Trier par decades
            }
        }
    }, 
    { "$match": { "votesNum": { "$ne": None } } }, #exclus Votes nuls ou inexistants 
    { "$sort": { "decade": 1, "votesNum": -1 } },#Tri par vote
    { 
        "$group": {
            "_id": "$decade",
            "topFilms": { "$push": { "title": "$title", "votes": "$votesNum", "year": "$year", "rating":"$rating" } }#Groupe par décades
        }
    },
    { 
        "$project": {
            "_id": 1,
            "topFilms": { "$slice": ["$topFilms", 3] }
        }#prends les trois fikm plus voté
    },
    { "$sort": { "_id": 1 } }
]

    result = films_collection.aggregate(pipeline)
    
    
    with onglet1:
        st.header("Quels sont les 3 films les mieux notés (rating) pour chaque décennie (1990-1999, 2000-2009,etc.) ?")
        st.write("Les films les plus mieux notés par décennies sont : ( les ratings étant juste G ou unrated on a décidé de choisir au nombre de Votes aussi)")
        for decade_data in result:
            decade = decade_data["_id"]
            st.subheader(f"Décennie {decade}s")  

            for film in decade_data["topFilms"]:
                title = film["title"]
                votes = film["votes"]
                year = film["year"]
                rating = film["rating"]

                st.write(f"**{title}** ({year}) - {votes} votes - Rating: {rating}")
            
    with onglet2:
        st.header("Voici notre requête")
        formatted_pipeline = json.dumps(pipeline, indent=1)
        st.code('result = list(films_collection.aggregate(pipeline))')
        st.write("Le pipeline est :")
        st.code(formatted_pipeline, language="json")
    

def question10(onglet1,onglet2,onglet3):
    """
    Question 10 : Quel est le film le plus long (Runtime) par genre ?
    """
    pipeline = [
        { 
            "$match": { #Exclusion des donnes nulles ou inexistante
                "Runtime (Minutes)": { "$ne": None, "$ne": "", "$exists": True },
                "genre": { "$ne": None, "$ne": "", "$exists": True }
            }
        },
        { 
            "$addFields": { 
                "runtimeNum": { "$toInt": "$Runtime (Minutes)" },  
                "genreList": { "$split": ["$genre", ","] }   #Tri des genre par films
            }
        },
        { "$unwind": "$genreList" },  
        { "$sort": { "genreList": 1, "runtimeNum": -1 } },  
        { 
            "$group": {
                "_id": "$genreList",
                "longestFilm": { "$first": { "title": "$title", "runtime": "$runtimeNum", "year": "$year" } }#Associe le film le plus long à son genre
            }
        },
        { "$sort": { "_id": 1 } }  
    ]

    result = films_collection.aggregate(pipeline)
    
    
    with onglet1:
        st.header("Quel est le film le plus long (Runtime) par genre ?")
        st.write("Les films les plus longs par genre sont : ")
        for film in result:
            genre = film["_id"]
            title = film["longestFilm"]["title"]
            runtime = film["longestFilm"]["runtime"]
            year = film["longestFilm"]["year"]
        
            st.write(f"**{genre}** : *{title}* ({year}) -  {runtime} min")
    
    with onglet2:
        st.header("Voici notre requête")
        formatted_pipeline = json.dumps(pipeline, indent=1)
        st.code('result = list(films_collection.aggregate(pipeline))')
        st.write("Le pipeline est :")
        st.code(formatted_pipeline, language="json")


def question11(onglet1,onglet2,onglet3):
    """
    Question 11 : Créer une vue MongoDB affichant uniquement les films ayant une note supérieure à 80 (Metascore) et généré plus de 50 millions de dollars.
    """
    pipeline = [
    { 
        "$match": { 
            "Metascore": { "$ne": None, "$exists": True },
            "Revenue (Millions)": { "$ne": None, "$exists": True } #Exclusion des données inexistante ou nulles
        }
    },
    { 
        "$addFields": { 
            "MetascoreNum": { 
                "$convert": { 
                    "input": "$Metascore", 
                    "to": "int", 
                    "onError": None  
                }
            },
            "RevenueNum": { 
                "$convert": { 
                    "input": "$Revenue (Millions)", 
                    "to": "double", 
                    "onError": None  
                }
            }
        }
    },
    { 
        "$match": { 
            "MetascoreNum": { "$gt": 80 },
            "RevenueNum": { "$gt": 50 }
        }
    },
    { 
        "$project": { 
            "_id": 0, 
            "title": 1, 
            "year": 1, 
            "Metascore": "$MetascoreNum", 
            "Revenue (Millions)": "$RevenueNum" 
        }
    }
    ]

    # Création de la vue
    db.command("create", "high_rated_profitable_movies", viewOn="films", pipeline=pipeline)
    
    result = db["high_rated_profitable_movies"].find()
    
    with onglet1:
        st.header("Créer une vue MongoDB affichant uniquement les films ayant une note supérieure à 80 (Metascore) et généré plus de 50 millions de dollars.")
        st.write("La vue est belle d'ici")
        
    with onglet2:
        st.header("Voici notre requête")
        formatted_pipeline = json.dumps(pipeline, indent=1)
        st.code('result = db["high_rated_profitable_movies"].find()')
        st.code('db.command("create", "high_rated_profitable_movies", viewOn="films", pipeline=pipeline)')
        st.write("Le pipeline est :")
        st.code(formatted_pipeline, language="json")
    
    

def question12(onglet1,onglet2,onglet3):  
    """
    Question 12 : Quelle est la corrélation entre la durée des films et leurs revenus ?
    """
    
    pipeline = [
    { 
        "$match": { 
            "Runtime (Minutes)": { "$ne": None, "$exists": True },
            "Revenue (Millions)": { "$ne": None, "$exists": True }#Exclusion donnée nulle ou inexistante
        }
    },
    { 
        "$addFields": { #Conversion
            "RuntimeNum": { 
                "$convert": { "input": "$Runtime (Minutes)", "to": "int", "onError": None }
            },
            "RevenueNum": { 
                "$convert": { "input": "$Revenue (Millions)", "to": "double", "onError": None }
            }
        }
    },
    { "$match": { "RuntimeNum": { "$ne": None }, "RevenueNum": { "$ne": None } } },#Exclusion données nulles ou inexistante
    { "$project": { "_id": 0, "Runtime": "$RuntimeNum", "Revenue": "$RevenueNum" } }#Recuperation données utiles
]


    data = list(films_collection.aggregate(pipeline))
    df = pd.DataFrame(data)  # Conversion en DataFrame

    # Calcul des différents coefficients
    pearson_corr, pearson_p = pearsonr(df["Runtime"], df["Revenue"])
    spearman_corr, spearman_p = spearmanr(df["Runtime"], df["Revenue"])

    # Heatmap de la corrélation
    corr_matrix = df.corr()

    # Affichage Streamlit
    with st.container():
        st.header("Corrélation entre la durée des films et leurs revenus")
        st.write("Il n'y a pas vraiment de corrélation entre les deux")
        
        st.write(f"**Corrélation de Pearson** : {pearson_corr:.3f} (p-value: {pearson_p:.5f})")
        st.write(f" **Corrélation de Spearman** : {spearman_corr:.3f} (p-value: {spearman_p:.5f})")
        st.write("Ces coefficient indique qu'il y a une faible corrélation entre Runtime et Revenus les coeficients aurait dû être plus élevé")

        # Affichage de la heatmap
        st.subheader("Matrice de corrélation")
        st.write("Le tout confimé par cette matrice")
        fig, ax = plt.subplots(figsize=(6, 5))
        sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
        st.pyplot(fig)

        # Affichage du scatter plot avec régression
        st.subheader("Graphique de régression")
        st.write("Le tout re-reconfimé par ce graphique, la droite aurait du être linéaire.")
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.regplot(x=df["Runtime"], y=df["Revenue"], scatter_kws={"alpha": 0.5}, line_kws={"color": "red"}, ax=ax)
        ax.set_xlabel("Durée du film (minutes)")
        ax.set_ylabel("Revenu (Millions)")
        ax.set_title("Corrélation entre la durée et le revenu des films")
        st.pyplot(fig)
    

def question13(onglet1,onglet2,onglet3):
    """
    Question 13 : Quelle est l'évolution de la durée moyenne des films par décennie ?
    """
    pipeline = [
    {
        "$match": {#Exclusion des donéée non existante ou nulles
            "Runtime (Minutes)": {"$ne": None, "$exists": True},
            "year": {"$ne": None, "$exists": True}
        }
    },
    {
        "$addFields": {#Convertion en entier
            "RuntimeNum": {"$convert": {"input": "$Runtime (Minutes)", "to": "int", "onError": None}},
            "Decade": {"$subtract": ["$year", {"$mod": ["$year", 10]}]}#Séparation des année par décades
        }
    },
    {
        "$group": {
            "_id": "$Decade",
            "AverageRuntime": {"$avg": "$RuntimeNum"},#Durée moyenne des films par décades
            "FilmCount": {"$sum": 1}
        }
    },
    {"$sort": {"_id": 1}}
]

# Exécuter la requête
    data = list(films_collection.aggregate(pipeline))
    df = pd.DataFrame(data)
    df.rename(columns={"_id": "Décennie"}, inplace=True)

# Affichage dans Streamlit
    with st.container():
        st.header("Évolution de la durée moyenne des films par décennie")
        

        # Création du graphique Matplotlib
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(df["Décennie"], df["AverageRuntime"], marker="o", linestyle="-", color="b", label="Durée moyenne")
        
        # Personnalisation
        ax.set_xlabel("Décennie")
        ax.set_ylabel("Durée moyenne (minutes)")
        ax.set_title("Évolution de la durée moyenne des films par décennie")
        ax.grid(True)
        ax.legend()

        # Affichage dans Streamlit
        st.pyplot(fig)


def question14(onglet1,onglet2,onglet3):
    """
    Question 14 : Quel acteur a joué dans le plus de films ? 

    Paramètres :
    onglet1 : Onglet Streamlit pour afficher les résultats
    onglet2 : Onglet Streamlit pour afficher la requête
    onglet3 : Onglet Streamlit pour afficher les résultats supplémentaires
    """

    # C'est la requête Neo4j, ce qu'on utilise le plus est records.
    # Records contient les résultats de la requête, c'est ce qui nous itéresse.
    records, summary, keys = neo4j_driver.execute_query(
        "MATCH (n:Actors)-[:A_jouer]->(f:films) RETURN n.actor, COUNT(f) AS nb_films ORDER BY nb_films DESC LIMIT 1" ,
            database_="neo4j",
        )
    
    # On affiche les résultats dans le premier onglet
    with onglet1:
        st.header("Quel acteur a joué dans le plus de films ?")
        st.write("L'acteur qui a joué dans le plus de films est", records[0][0], "avec", records[0][1], "films.")

    # On affiche la requête dans le deuxième onglet
    with onglet2:
        st.header("Voici notre requête")
        st.code('records, summary, keys = neo4j_driver.execute_query("\n\tMATCH (n:Actors)-[:A_jouer]->(f:films) \n\tRETURN n.actor, COUNT(f) AS nb_films \n\tORDER BY nb_films DESC LIMIT 1" , database_="neo4j")')

def question15(onglet1,onglet2,onglet3):
    """
    Question 15 : Quels sont les acteurs qui ont joué avec Anne Hathaway ?
    Paramètres :
    onglet1 : Onglet Streamlit pour afficher les résultats
    onglet2 : Onglet Streamlit pour afficher la requête
    onglet3 : Onglet Streamlit pour afficher les résultats supplémentaires
    """

    # La requête Neo4j
    records, summary, keys = neo4j_driver.execute_query(
        """
        MATCH (n:Actors)-[:A_jouer]->(f:films)<-[:A_jouer]-(a:Actors)
        WHERE a.actor = "Anne Hathaway"
        RETURN n.actor
        """ ,
            database_="neo4j",
        )
    
    # Affichage resultats
    with onglet1:
        st.header("Quels sont les acteurs qui ont joué avec Anne Hathaway ?")
        for record in records:
            st.write(f"- {record[0]}")

    # Affichage de la requête
    with onglet2:
        st.header("Voici notre requête")
        st.code('records, summary, keys = neo4j_driver.execute_query("\n\tMATCH (n:Actors)-[:A_jouer]->(f:films)<-[:A_jouer]-(a:Actors) \n\tWHERE a.actor = "Anne Hathaway" \n\tRETURN n.actor" , database_="neo4j")')

def question16(onglet1,onglet2,onglet3):
    """
    Question 16 : Quel est l'acteur ayant joué dans des films totalisant le plus de revenu ?
    Paramètres :
    onglet1 : Onglet Streamlit pour afficher les résultats
    onglet2 : Onglet Streamlit pour afficher la requête
    onglet3 : Onglet Streamlit pour afficher les résultats supplémentaires
    """
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
    """
    Question 17 : Quelle est la moyenne de votes des films ?

    Paramètres :
    onglet1 : Onglet Streamlit pour afficher les résultats
    onglet2 : Onglet Streamlit pour afficher la requête
    onglet3 : Onglet Streamlit pour afficher les résultats supplémentaires
    """

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
    """
    Question 18 : Quel est le genre de film le plus représenté ?
    Paramètres :
    onglet1 : Onglet Streamlit pour afficher les résultats
    onglet2 : Onglet Streamlit pour afficher la requête
    onglet3 : Onglet Streamlit pour afficher les résultats supplémentaires
    """

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
    """
    Question 19 : Quels sont les films dans lesquels ont joué les acteurs ayant joué avec Julien Oliveira ?
    Paramètres :
    onglet1 : Onglet Streamlit pour afficher les résultats
    onglet2 : Onglet Streamlit pour afficher la requête
    onglet3 : Onglet Streamlit pour afficher les résultats supplémentaires
    """
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
    """
    Question 20 : Quel est le réalisateur ayant dirigé le plus d'acteurs différents ?
    Paramètres :
    onglet1 : Onglet Streamlit pour afficher les résultats
    onglet2 : Onglet Streamlit pour afficher la requête
    onglet3 : Onglet Streamlit pour afficher les résultats supplémentaires
    """
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
    """
    Question 21 : Quels sont les films qui ont le plus d'acteurs en commun avec d'autres films ?
    Paramètres :
    onglet1 : Onglet Streamlit pour afficher les résultats
    onglet2 : Onglet Streamlit pour afficher la requête
    onglet3 : Onglet Streamlit pour afficher les résultats supplémentaires
    """
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
    """
    Question 22 : Quels sont les acteurs ayant travaillé avec le plus de réalisateurs différents ?
    Paramètres :
    onglet1 : Onglet Streamlit pour afficher les résultats
    onglet2 : Onglet Streamlit pour afficher la requête
    onglet3 : Onglet Streamlit pour afficher les résultats supplémentaires
    """
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
    """
    question 23 : Quels sont les films recommandés pour un acteur donné ?
    Paramètres :
    onglet1 : Onglet Streamlit pour afficher les résultats
    onglet2 : Onglet Streamlit pour afficher la requête
    onglet3 : Onglet Streamlit pour afficher les résultats supplémentaires
    """

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
    """
    Question 24 : Quels sont les réalisateurs qui se sont influencés mutuellement ?
    Paramètres :
    onglet1 : Onglet Streamlit pour afficher les résultats
    onglet2 : Onglet Streamlit pour afficher la requête
    onglet3 : Onglet Streamlit pour afficher les résultats supplémentaires
    """
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
    """
    Question 25 : Quel est le plus court chemin entre deux acteurs ?
    Paramètres :
    onglet1 : Onglet Streamlit pour afficher les résultats
    onglet2 : Onglet Streamlit pour afficher la requête
    onglet3 : Onglet Streamlit pour afficher les résultats supplémentaires
    """
    def requetes():
        """
        Permet de faire la requête pour trouver le plus court chemin entre deux acteurs.
        """
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
    # Permet de choisir deux acteurs différents
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
                # Selon la requête, records2 contient le chemin entre les deux acteurs
                # Et on affiche le chemin en allant récupérer les propriétés des noeuds
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
    """
    Question 26 : Trouver les communautés d'acteurs dans le graphe
    Paramètres :
    onglet1 : Onglet Streamlit pour afficher les résultats
    onglet2 : Onglet Streamlit pour afficher la requête
    onglet3 : Onglet Streamlit pour afficher les résultats supplémentaires
    """

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
    """
    Question 27 : Quels sont les films qui ont le même genre mais des réalisateurs différents ?
    Paramètres :
    onglet1 : Onglet Streamlit pour afficher les résultats
    onglet2 : Onglet Streamlit pour afficher la requête
    onglet3 : Onglet Streamlit pour afficher les résultats supplémentaires
    """
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
    """
    Question 28 : Quels sont les films recommandés pour un acteur donné ?
    Paramètres :
    onglet1 : Onglet Streamlit pour afficher les résultats
    onglet2 : Onglet Streamlit pour afficher la requête
    onglet3 : Onglet Streamlit pour afficher les résultats supplémentaires
    """
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
    """
    Question 29 : Quels sont les réalisateurs qui ont réalisé des films similaires la même année ?
    Paramètres :
    onglet1 : Onglet Streamlit pour afficher les résultats
    onglet2 : Onglet Streamlit pour afficher la requête
    onglet3 : Onglet Streamlit pour afficher les résultats supplémentaires
    """
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
    """
    Questions 30 : Quels sont les collaborations les plus fréquentes entre acteurs et réalisateurs ? Est ce que ces collaborations sont associés à un succès commercial ou critique ?
    """
    records, summary, keys = neo4j_driver.execute_query(
        """
    MATCH (a:Actors)-[:A_jouer]->(f:films)<-[:A_Realise]-(r:Realisateur)
    WITH a, r, COUNT(f) AS films_commun, Collect(f.title) AS films_titres
    Where films_commun >= 2
    RETURN a.actor, r.realisateur, films_commun, films_titres
    Order by films_commun DESC
    LIMIT 5
    """
        , database_="neo4j",
    )

    films = set()
    films_mongo = []
    with onglet1:
        st.header("Dans cette section, nous allons voir les collaborations les plus fréquentes entre acteurs et réalisateurs.")
        st.write("On considère que un acteur et un réalisateur ont collaboré 'souvent' s'ils ont réalisé au moins 2 films ensemble.")
        st.write("Avec notre requête, nous avons trouvé", len(records), "collaborations.")
        
        for record in records:
            st.write(f"- {record[0]} et {record[1]} ont collaboré {record[2]} fois.")
            for film in record[3]:
                films.add(film)

        st.write("Est ce que ces collaborations sont associés à un succès commercial ou critique ?")
        # On va étudier la moyenne des notes meta critic et des revenus via mongodb
        

        for film in films:
             films_mongo.extend(list(collection.find({"title": film})))

        st.write("La moyenne des notes meta critic est de", round(sum([film['Metascore'] for film in films_mongo])/len(films_mongo), 2))
        st.write("La moyenne des revenus est de", round(sum([film['Revenue (Millions)'] for film in films_mongo])/len(films_mongo), 2))

    with onglet2:
        st.header("Voici nos requêtes")
        st.code('records, summary, keys = neo4j_driver.execute_query("\n\tMATCH (a:Actors)-[:A_jouer]->(f:films)<-[:A_Realise]-(r:Realisateur) \n\tWITH a, r, COUNT(f) AS films_commun \n\tWhere films_commun >= 2 \n\tRETURN a.actor, r.realisateur, films_commun, f.title \n\tOrder by films_commun DESC \n\tLIMIT 5" , database_="neo4j")')
        st.write("Cette requête permet de trouver les collaborations les plus fréquentes entre acteurs et réalisateurs.")
        st.code('films_mongo = collection.find({"title": film})')
        st.write("Cette requête permet de trouver les films dans la base de données MongoDB.")
    with onglet3:
        st.header("Voici nos résultats supplémentaires")
        data_list = []
        for film in films_mongo:
            data = {
                'title': film['title'],
                'meta_score': film['Metascore'],
                'revenue': film['Revenue (Millions)'],
                'Réalisateur': film['Director'],
                'Acteur': film['Actors'],
            }
            data_list.append(data)
            df = pd.DataFrame(data_list)

        st.dataframe(df)