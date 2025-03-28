import streamlit as st
import json
from requetes import *

from globals import collection, neo4j_driver, createdb

############## Connexion Mongo DB + Neo4J #####################


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


import os
def home():
    """
    Permet de charger la page d'accueil
    """
    st.title("Bienvenue sur notre projet NoSQL aka le 🌟 Best project 🌟")
    st.write("Ce projet a été réalisé par Julien Oliveira et Ambre Vasseur.")
    
    onglet1, onglet2 = st.tabs(["MongoDB", "Neo4j"]) 
    

    with onglet1:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Charger les données"):
                            load_data()
                            st.success("Données chargées !")
            if st.button("Ajouter un document à MongoDB"):
                collection.insert_one({"message": "Hello from MongoDB!"})
                st.success("Document ajouté !")
        with col2:
            if st.button("Supprimer les données"):
                collection.drop()
                st.success("Données supprimées !")

            if st.button("Afficher les documents MongoDB"):
                documents = list(collection.find({}, {"_id": 0}))
                st.json(documents)

    with onglet2:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Créer la base de données"):
                createdb()
                st.success("Base de données créée !")
            
            if st.button("Ajouter un nœud Neo4j"):
                st.success("Nœud ajouté !")
        with col2:
            if st.button("Supprimer la base de données"):
                with neo4j_driver.session(database="neo4j") as session:
                    session.run("MATCH (n) DETACH DELETE n")

                session.close()
                st.success("Base de données supprimée !")

            if st.button("Afficher les nœuds Neo4j"):
                with neo4j_driver.session(database="neo4j") as session:
                    result = session.run("MATCH (n) RETURN n")
                    messages = [record["n"] for record in result]
                session.close()
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
    questions = [f"Question {i}" for i in range(1, 31)]
    if "question_index" not in st.session_state:
        st.session_state.question_index = 0
    submenu = st.sidebar.selectbox("Questions", [f"Question {i}" for i in range(1,31)],index=st.session_state.question_index)

   

    titres_onglets = ['Réponse', 'Requête', 'Visualisation']

    st.title(f"Question {submenu.split()[-1]}")
    onglet1, onglet2, onglet3 = st.tabs(titres_onglets)

    switch = {
        "Question 1": lambda : question1(onglet1,onglet2,onglet3),
        "Question 2":  lambda : question2(onglet1,onglet2,onglet3),
        "Question 3":  lambda : question3(onglet1,onglet2,onglet3),
        "Question 4":  lambda : question4(onglet1,onglet2,onglet3),
        "Question 5":  lambda : question5(onglet1,onglet2,onglet3),
        "Question 6":  lambda : question6(onglet1,onglet2,onglet3),
        "Question 7":  lambda : question7(onglet1,onglet2,onglet3),
        "Question 8":  lambda : question8(onglet1,onglet2,onglet3),
        "Question 9":  lambda : question9(onglet1,onglet2,onglet3),
        "Question 10":  lambda : question10(onglet1,onglet2,onglet3),
        "Question 11":  lambda : question11(onglet1,onglet2,onglet3),
        "Question 12":  lambda : question12(onglet1,onglet2,onglet3),
        "Question 13":  lambda : question13(onglet1,onglet2,onglet3),
        "Question 14":  lambda : question14(onglet1,onglet2,onglet3),
        "Question 15":  lambda : question15(onglet1,onglet2,onglet3),
        "Question 16":  lambda : question16(onglet1,onglet2,onglet3),
        "Question 17":  lambda : question17(onglet1,onglet2,onglet3),
        "Question 18":  lambda : question18(onglet1,onglet2,onglet3),
        "Question 19":  lambda : question19(onglet1,onglet2,onglet3),
        "Question 20":  lambda : question20(onglet1,onglet2,onglet3),
        "Question 21":  lambda : question21(onglet1,onglet2,onglet3),
        "Question 22":  lambda : question22(onglet1,onglet2,onglet3),
        "Question 23":  lambda : question23(onglet1,onglet2,onglet3),
        "Question 24":  lambda : question24(onglet1,onglet2,onglet3),
        "Question 25":  lambda : question25(onglet1,onglet2,onglet3),
        "Question 26":  lambda : question26(onglet1,onglet2,onglet3),
        "Question 27":  lambda : question27(onglet1,onglet2,onglet3),
        "Question 28":  lambda : question28(onglet1,onglet2,onglet3),
        "Question 29":  lambda : question29(onglet1,onglet2,onglet3),
        "Question 30":  lambda : question3(onglet1,onglet2,onglet3)
    } 

    switch.get(submenu, lambda: st.write("Question non définie"))()

    col1, col2 = st.sidebar.columns([1, 1])

    with col1:
        if st.button("⬅️ Précédent"):
            st.session_state.question_index = (st.session_state.question_index - 1) % len(questions)
            st.rerun()

    with col2:
        if st.button("➡️ Suivant"):
            st.session_state.question_index = (st.session_state.question_index + 1) % len(questions)
            st.rerun()

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


