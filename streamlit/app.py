import streamlit as st
from pymongo import MongoClient
from neo4j import GraphDatabase
import json

from requetes import *

############## Connexion Mongo DB + Neo4J #####################

# Connexion MongoDB 
client = MongoClient("mongodb://mongodb:27017/")
db = client["movies"]
collection = db["films"]

# Connexion Neo4j
uri = "bolt://neo4j:7687"
auth = ("neo4j", "Ceciestuntest")
neo4j_driver = GraphDatabase.driver(uri, auth=auth)

######################## Config Streamlit #########################
st.set_page_config(
    layout="wide",  # "centered" ou "wide"
    initial_sidebar_state="expanded", 
)

############## Fonctions de Bases #####################""


def insert_if_not_exists(document):
    """Vérifie et ajoute le fichier JSON si il n'existe pas dans la db"""
    existing_doc = collection.find_one({"_id": document["_id"]})  # Remplace "name" par ton champ unique
    
    if existing_doc is None:
        collection.insert_one(document)
        
def load_data():
    """Charge les données dans la base de données."""
    with open("movies.json", "r") as file:
        data = json.load(file)

    if isinstance(data, list):
        for doc in data:
            insert_if_not_exists(doc)
    else:
        insert_if_not_exists(data)
    
    file.close()



def home():
    """
    Permet de charger la page d'accueil
    """
    st.title("Bienvenue sur notre projet NoSQL aka le 🌟 Best project 🌟")
    st.write("Ce projet a été réalisé par Julien Oliveira et Ambre Vasseur.")
    
    col1, col2 = st.columns(2)
   
    st.header('Réponse aux questions de la partie MongDB')
    st.write("C'est ici que vous pouvez prétraiter vos données.")

    with col1:
        if st.button("Charger les données"):
            load_data()
            st.success("Données chargées !")

    with col2:
        if st.button("supprimer les données"):
            collection.drop()
            st.success("Données supprimées !")

    if st.button("Ajouter un document à MongoDB"):
        collection.insert_one({"message": "Hello from MongoDB!"})
        st.success("Document ajouté !")

    if st.button("Afficher les documents MongoDB"):
        documents = list(collection.find({}, {"_id": 0}))
        st.json(documents)

    if st.button("Ajouter un nœud Neo4j"):
        with neo4j_driver.session() as session:
            session.run("CREATE (n:Test {message: 'Hello from Neo4j'})")
        st.success("Nœud ajouté !")

    if st.button("Afficher les nœuds Neo4j"):
        with neo4j_driver.session() as session:
            result = session.run("MATCH (n:Test) RETURN n.message AS message")
            messages = [record["message"] for record in result]
        st.json(messages)

def sources():
    """ Charge la page qui permet de montrer nos sources
    """
    st.title("Voici nos sources :")
    st.write("Ce projet a été réalisé par Julien Oliveira et Ambre Vasseur.")

    st.write(f'''
    <a target="_self" href="https://github.com/Spydey-27/Best_project">
        <button>
            Notre Repository github
        </button>
    </a>
    ''',
    unsafe_allow_html=True
)

def Questions():
    """ Page la plus importante du projet ! 
    Elle permet d'accéder à toutes les questions
    """
    submenu = st.sidebar.selectbox("Questions", [f"Question {i}" for i in range(1,31)])

    switch = {
        "Question 1": question1,
        "Question 2": question2,
        "Question 3": question3,
        "Question 4": question4,
        "Question 5": question5,
        "Question 6": question6,
        "Question 7": question7,
        "Question 8": question8,
        "Question 9": question9,
        "Question 10": question10,
        "Question 11": question11,
        "Question 12": question12,
        "Question 13": question13,
        "Question 14": question14,
        "Question 15": question15,
        "Question 16": question16,
        "Question 17": question17,
        "Question 18": question18,
        "Question 19": question19,
        "Question 20": question20,
        "Question 21": question21,
        "Question 22": question22,
        "Question 23": question23,
        "Question 24": question24,
        "Question 25": question25,
        "Question 26": question26,
        "Question 27": question27,
        "Question 28": question28,
        "Question 29": question29,
        "Question 30": question30
    }

    switch.get(submenu, lambda: st.write("Question non définie"))()

################### Streamlit Navigation Bar ################################""

pages = {
    "Menu": [
        st.Page(home, title="🌟 Best project 🌟"),
        st.Page(Questions, title="Questions", icon="❓"),
    ],
    "Sources" : [
        st.Page(sources , title="Source", icon="⚙️"),
    ],
}


pg = st.navigation(pages)
pg.run()


