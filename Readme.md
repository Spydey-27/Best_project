# ✨ The Best Project ✨

[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Docker](https://badgen.net/badge/icon/docker?icon=docker&label)](https://https://docker.com/)

Ce projet consiste à créer un site web à partir du framework [Streamlit](https://streamlit.io/) couplé à 2 bases de données. Une avec [MongoDB](https://www.mongodb.com/) et une autre avec [Neo4j](https://neo4j.com/).
L'objectif était de réaliser quelques requêtes sur un dataset de 100 films.

## Pour commencer

Pour commencer à explorer notre projet, rien de bien compliqué, il suffit de suivre la partie [Installation](#installation-et-démarrage).

### Pré-requis

Afin de pouvoir utiliser notre projet en Local, veuillez vérifier que vous remplissez les pré-requis

- Docker
Si vous ne l'avez pas, nous vous recommandons de suivre le tutoriel officiel : [Linux](https://docs.docker.com/engine/install/debian/), [MacOS](https://docs.docker.com/desktop/setup/install/mac-install/), [Windows](https://docs.docker.com/desktop/setup/install/windows-install/)

- Docker compose : https://docs.docker.com/compose/install/


## Installation et Démarrage

Pour lancer notre projet vous avez deux possibilités.
Tout d'abord, veuillez cloner ce repository avec : 
```bash
git clone https://github.com/Spydey-27/Best_project.git
```

1. Utiliser Docker compose
A la racine de notre projet, vous trouverez un [docker-compose.yml](docker-compose.yml)
Il suffit de l'exécuter avec (sur votre terminal) : 
```bash
docker compose up --build
```
pour lancer votre propre architecture docker 🎉

2. Utiliser les images fournies dans le dossier ~/[image_conteneurs](image_conteneurs/) du répertoire git
Pour les utiliser rien de plus simple (sur votre terminal) : 
```bash
docker load < image_service_mongo.tar
docker load < image_service_neo4j.tar
docker load < image_service_streamlit.tar
```
Ensuite lancez :
```bash
docker compose up --build
```

Enfin, vous aurez juste à vous connecter à l'adresse suivante : http://localhost:8501/

Pour bien commencer, nous vous recommandons de charger les données pour MongoDB et Neo4j. Vous pourrez faire ceci dans la première page de notre site (onglet : 🌟 Best project Home 🌟 )

*Pour aller plus loin* :
Si vous souhaitez accéder à Neo4j sur le web : http://localhost:7474/

## Fabriqué avec

* [![](https://img.shields.io/badge/-Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)
* ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
* ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
* ![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white)
* ![Neo4J](https://img.shields.io/badge/Neo4j-008CC1?style=for-the-badge&logo=neo4j&logoColor=white)


## Problèmes rencontrés & Solutions adoptées
L'une des premières difficultés a été de connecter les différentes bases de données entre elles. La base MongoDB via Atlas et Neo4J via Aura, nous avons trouvé la solution en recherchant dans la documentation. Cependant, pour des questions de facilités de déploiement, nous avons opté pour une version avec Docker beaucoup plus facile à manipuler.
Par ailleurs, certaines questions du sujet étaient un peu floues, nous incitant à faire des choix sur certaines réponses.
De plus, l'implémentation des graphiques pour les dernières questions de la partie MongoDB était complexe mais encore (et toujours) grâce à la documentation de streamlit, nous avons pu afficher joliment nos schémas.
Enfin, la dernière difficulté était de trouver les bonnes requêtes pour répondre aux questions, que ce soit en MongoDB ou en Neo4j.

## Versions
**Dernière version stable :** 1.0
**Dernière version :** 1.0

## Auteurs
* **Julien Oliveira** _alias_ [@Spydey-27](https://github.com/Spydey-27)
* **Ambre Vasseur** _alias_ [@Lisytheia](https://github.com/Lisytheia)



