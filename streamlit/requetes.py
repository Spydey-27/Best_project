import streamlit as st
from pymongo import MongoClient
from globals import client, db, collection, neo4j_driver
import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from scipy.stats import pearsonr, spearmanr
films_collection = collection




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
        st.write("Le pipeline est :")
        st.code(formatted_pipeline, language="json")


def question6(onglet1,onglet2,onglet3):
    pipeline6= [
    { "$match": { "Revenue (Millions)": { "$ne": None , "$ne": "", "$gt": 0 } } },  
    { "$sort": { "Revenue (Millions)": -1 } },  
    { "$limit": 1 }
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
    
    
    pipeline7= [

    { "$group": {"_id": "$Director","nombreFilms": { "$sum": 1 } }},
    { "$match": { "nombreFilms": { "$gt": 5 } }},
    { "$sort": { "nombreFilms": -1 } }

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
    pipeline = [
    { 
        "$match": { 
            "year": { "$ne": None, "$exists": True },
            "Votes": { "$ne": None, "$ne": "", "$exists": True }
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
                "$subtract": [ { "$toInt": "$year" }, { "$mod": [{ "$toInt": "$year" }, 10] } ] 
            }
        }
    },
    { "$match": { "votesNum": { "$ne": None } } },  
    { "$sort": { "decade": 1, "votesNum": -1 } },
    { 
        "$group": {
            "_id": "$decade",
            "topFilms": { "$push": { "title": "$title", "votes": "$votesNum", "year": "$year", "rating":"$rating" } }
        }
    },
    { 
        "$project": {
            "_id": 1,
            "topFilms": { "$slice": ["$topFilms", 3] }
        }
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
    
    pipeline = [
        { 
            "$match": { 
                "Runtime (Minutes)": { "$ne": None, "$ne": "", "$exists": True },
                "genre": { "$ne": None, "$ne": "", "$exists": True }
            }
        },
        { 
            "$addFields": { 
                "runtimeNum": { "$toInt": "$Runtime (Minutes)" },  
                "genreList": { "$split": ["$genre", ","] }  
            }
        },
        { "$unwind": "$genreList" },  
        { "$sort": { "genreList": 1, "runtimeNum": -1 } },  
        { 
            "$group": {
                "_id": "$genreList",
                "longestFilm": { "$first": { "title": "$title", "runtime": "$runtimeNum", "year": "$year" } }
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
    pipeline = [
    { 
        "$match": { 
            "Metascore": { "$ne": None, "$exists": True },
            "Revenue (Millions)": { "$ne": None, "$exists": True }
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
    
    pipeline = [
    { 
        "$match": { 
            "Runtime (Minutes)": { "$ne": None, "$exists": True },
            "Revenue (Millions)": { "$ne": None, "$exists": True }
        }
    },
    { 
        "$addFields": { 
            "RuntimeNum": { 
                "$convert": { "input": "$Runtime (Minutes)", "to": "int", "onError": None }
            },
            "RevenueNum": { 
                "$convert": { "input": "$Revenue (Millions)", "to": "double", "onError": None }
            }
        }
    },
    { "$match": { "RuntimeNum": { "$ne": None }, "RevenueNum": { "$ne": None } } },
    { "$project": { "_id": 0, "Runtime": "$RuntimeNum", "Revenue": "$RevenueNum" } }
]


    data = list(films_collection.aggregate(pipeline))
    df = pd.DataFrame(data)  # Conversion en DataFrame

  
    pearson_corr, pearson_p = pearsonr(df["Runtime"], df["Revenue"])
    spearman_corr, spearman_p = spearmanr(df["Runtime"], df["Revenue"])

    # Heatmap de la corrélation
    corr_matrix = df.corr()

    # Affichage Streamlit
    with st.container():
        st.header("Corrélation entre la durée des films et leurs revenus")

        
        st.write(f"**Corrélation de Pearson** : {pearson_corr:.3f} (p-value: {pearson_p:.5f})")
        st.write(f" **Corrélation de Spearman** : {spearman_corr:.3f} (p-value: {spearman_p:.5f})")

        # Affichage de la heatmap
        st.subheader("Matrice de corrélation")
        fig, ax = plt.subplots(figsize=(6, 5))
        sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
        st.pyplot(fig)

        # Affichage du scatter plot avec régression
        st.subheader("Graphique de régression")
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.regplot(x=df["Runtime"], y=df["Revenue"], scatter_kws={"alpha": 0.5}, line_kws={"color": "red"}, ax=ax)
        ax.set_xlabel("Durée du film (minutes)")
        ax.set_ylabel("Revenu (Millions)")
        ax.set_title("Corrélation entre la durée et le revenu des films")
        st.pyplot(fig)
    
    
    
    
    

def question13(onglet1,onglet2,onglet3):
    pipeline = [
    {
        "$match": {
            "Runtime (Minutes)": {"$ne": None, "$exists": True},
            "year": {"$ne": None, "$exists": True}
        }
    },
    {
        "$addFields": {
            "RuntimeNum": {"$convert": {"input": "$Runtime (Minutes)", "to": "int", "onError": None}},
            "Decade": {"$subtract": ["$year", {"$mod": ["$year", 10]}]}
        }
    },
    {
        "$group": {
            "_id": "$Decade",
            "AverageRuntime": {"$avg": "$RuntimeNum"},
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
    title = st.selectbox(
        "Sélectionnez un film",
        ["Passengers", "The Dark Knight", "Inception", "The Avengers", "Avatar"]
    ) 
    st.write(title)

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








