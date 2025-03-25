# from neo4j import GraphDatabase

# # URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"
# URI = "neo4j+s://2ea23cf6.databases.neo4j.io"
# AUTH = ("neo4j", "nMA6eFsv5KqeP7RiDVmI41wE67ad3UwPjo_uJPupSzE")

# with GraphDatabase.driver(URI, auth=AUTH) as driver:
#     driver.verify_connectivity()
#     print("connection reussie")
    
    
# from pymongo.mongo_client import MongoClient
# from pymongo.server_api import ServerApi
# uri = "mongodb+srv://vasseur:aled@cluster0.bgn7j.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# # Create a new client and connect to the server
# client = MongoClient(uri, server_api=ServerApi('1'))
# # Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)


import streamlit as st

st.title("Notre magnifique projet NOSQL")

# Créer les onglets
titres_onglets = ['MongoDB', 'Neo4j']
onglets = st.tabs(titres_onglets)


with onglets[0]:
    st.header('Réponse aux questions de la partie MongDB')
    st.write("C'est ici que vous pouvez prétraiter vos données.")

# Ajouter du contenu à l'onglet Formation des modèles
with onglets[1]:
    st.header('Réponse aux questions de la partie Neo4J')
    st.write("C'est ici que vous pouvez former votre modèle.")

