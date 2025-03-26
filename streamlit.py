import streamlit as st
from mongodb import *

st.title("Notre magnifique projet NOSQL")

# Créer les onglets
titres_onglets = ['MongoDB', 'Neo4j']
onglets = st.tabs(titres_onglets)


with onglets[0]:
    st.header('Réponse aux questions de la partie MongDB')
    
    st.write('Question 1 : Afficher l’année ou le plus grand nombre de films ont été sortis.')
    st.caption("Requête")
    st.write(pipeline1)
    st.caption("Résultat")
    st.write(resultat1)
    
    st.write('Question 2 : Quel est le nombre de films sortis après l’année 1999.')
    st.caption("Requête")
    st.write(pipeline2)
    st.caption("Résultat")
    st.write(resultat2)
    
    st.write('Question 3 : Quelle est la moyenne des votes des films sortis en 2007.')
    st.caption("Requête")
    st.write(pipeline3)
    st.caption("Résultat")
    st.write(resultat3)
    
    st.write('Question 4 : Affichez un histogramme qui permet de visualiser le nombres de films par année.')
    st.caption("Requête")
    st.write("On obtient cet histograme en allant dans l'onglet Schéma, puis en cliquant sur Analyze")
    st.caption("Résultat")
    st.image("histogramme.png")

    st.write('Question 5 : Quelles sont les genres de films disponibles dans la bases.')
    st.caption("Requête")
    st.write(pipeline5)
    st.caption("Résultat")
    st.write(resultat5)
    
    
    st.write('Question 6 : Quel est le film qui a généré le plus de revenu.')
    st.caption("Requête")
    st.write(pipeline6)
    st.caption("Résultat")
    st.write(resultat6)



# Ajouter du contenu à l'onglet Formation des modèles
with onglets[1]:
    st.header('Réponse aux questions de la partie Neo4J')
    st.write("C'est ici que vous pouvez former votre modèle.")
