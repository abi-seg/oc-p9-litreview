LitReview – Projet 9 OpenClassrooms

LitReview est une application web développée avec **Django** dans le cadre du parcours "Développeur d’application Python" sur OpenClassrooms.

Elle permet aux utilisateurs de :
- Publier des **tickets** (demandes de critiques d'œuvres littéraires ou articles)
- Écrire des **critiques** et attribuer une **note** (de 0 à 5)
- **Suivre** d’autres utilisateurs et voir leurs écrits dans un **flux **
- **Téléverser une image** lors de la création d’un ticket (ex. couverture du livre)

---

## Fonctionnalités

-  Authentification (inscription / connexion / déconnexion)
-  Création, modification et suppression des tickets et des critiques
-  Attribution de notes (0 à 5)
-  Ajout d’images pour les tickets
-  Système d'abonnements (utilisateurs suivis et abonnés)
-  Flux de publications personnalisé
-  Interface responsive avec Bootstrap

---

## Installation locale de l’application

### Étapes à suivre

1. **Cloner le dépôt Git :** git clone https://github.com/abi-seg/oc-p9-litreview
cd litreview
2.	Créer un environnement virtuel : python -m venv env
3.	Activer l’environnement virtuel :
•	Sous Windows : env\Scripts\activate
•	Sous macOS / Linux : source env/bin/activate
4.	Installer Django :
pip install django
pip install pillow
(Pillow est requis pour la gestion des images via ImageField)
5.	Appliquer les migrations de la base de données : python manage.py migrate
6.	Lancer le serveur local : python manage.py runserver
7.	Accéder à l’application : http://localhost:8000
________________________________________
Informations de connexion (compte de test)
•	Nom d’utilisateur : testuser
•	Mot de passe : mdp12345
Ou vous pouvez créer un nouveau compte via la page d’inscription.
________________________________________
Contenu du dépôt GitHub
•	README.md → instructions d’installation
•	db.sqlite3 → base de données incluse avec données de test
•	Répertoire media/ ignoré dans .gitignore
•	Code source Django :
•	accounts/ : gestion des utilisateurs
•	reviews/ : tickets, critiques, abonnements
•	templates/ : pages HTML de l'application
________________________________________
Projet créé par SEGARIN Abiramasundari
Parcours : Développeur d’application Python – OpenClassrooms
Contact :abirami1488@gmail.com 

