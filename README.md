# 🏃‍♂️ Générateur d'équipes sportives équilibrées

> **Contexte :** Projet développé en 2021 pour automatiser la constitution d'équipes mixtes dans le cadre d'activités sportives inter-classes (75 élèves, 3 classes).

## 🎯 Problème résolu

**Avant :** Constitution manuelle des équipes = 15-20min par séance, difficulté à garantir la parité et l'équilibre entre classes.

**Après :** Génération automatique en < 1min, équipes aléatoires et équilibrées, export multi-formats (global/par classe/par équipe).

**Impact :** Utilisé pendant 2 ans par 3 enseignants, ~100 tirages effectués.

## 🛠️ Stack technique

- **Python 3.x**
- **Pandas** (manipulation de données)
- **XlsxWriter** (export Excel formaté avec couleurs) - *branche `Pandas-version`*
- **CSV natif** - *branche `main`*

## 📊 Fonctionnalités clés

✅ Lecture fichier CSV (nom, prénom, genre, classe)  
✅ Algorithme de répartition aléatoire avec contrainte de parité  
✅ Export multi-formats (global, par classe, par équipe)  
✅ Personnalisation des noms d'équipes  
✅ Code couleur par équipe (version Pandas)  

## 💡 Apprentissage personnel

Premier projet Python développé en autonomie (sans LLM). M'a permis de découvrir :
- La manipulation de DataFrames avec Pandas
- L'importance de l'UX pour des utilisateurs non-techniques
- Le plaisir de résoudre des problèmes opérationnels par le code

**Ce projet est à l'origine de ma reconversion vers la Data.**

---

## 📖 Documentation utilisateur
