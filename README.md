LexiTrack est une plateforme qui permet de résumer automatiquement vos lectures et de les retrouver facilement.
Elle se compose de trois parties :

Une extension Chrome pour résumer une page en un clic

Une interface web (React + TailwindCSS) pour consulter et organiser vos résumés

Un backend (FastAPI) pour gérer la génération et le stockage

🚀 Fonctionnalités

Résumé en un clic : déclenchez un résumé depuis l’extension Chrome.

Historique des résumés : retrouvez vos résumés sauvegardés dans l’interface web.

Organisation simple : vos résumés sont enregistrés automatiquement par page/fichier.

IA intégrée : génération des résumés via GPT-4o.

🏗️ Architecture

Backend (FastAPI)

Endpoints REST

Persistance avec PostgreSQL

ORM : SQLAlchemy + Alembic

Intégration IA

Frontend Web (React + TailwindCSS)

Interface moderne pour naviguer dans vos résumés

Organisation et affichage des fichiers résumés

Extension Chrome (Manifest V3) --> Bouton résumé en un clic
