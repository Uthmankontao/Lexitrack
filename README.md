# 📖 LexiTrack

**LexiTrack** est une plateforme qui permet de **résumer automatiquement vos lectures** et de les retrouver facilement.  
Elle se compose de trois parties :  

- 🧩 **Extension Chrome** : résumez une page en un clic  
- 🌐 **Interface web (React + TailwindCSS)** : consultez et organisez vos résumés  
- ⚡ **Backend (FastAPI)** : gérez la génération et le stockage  

---

## 🚀 Fonctionnalités

- ✨ **Résumé en un clic** : déclenchez un résumé depuis l’extension Chrome  
- 📜 **Historique des résumés** : retrouvez vos résumés sauvegardés dans l’interface web  
- 📂 **Organisation simple** : résumés enregistrés automatiquement par page/fichier  
- 🤖 **IA intégrée** : génération des résumés via notre AI.

---

## 🏗️ Architecture

### 🔙 Backend (FastAPI)
- Endpoints REST  
- Persistance avec **PostgreSQL**  
- ORM : **SQLAlchemy + Alembic**  
- Intégration IA  

### 💻 Frontend Web (React + TailwindCSS)
- Interface moderne pour naviguer dans vos résumés  
- Organisation et affichage des fichiers résumés  

### 🧩 Extension Chrome (Manifest V3)
- Bouton **Résumé en un clic**  
