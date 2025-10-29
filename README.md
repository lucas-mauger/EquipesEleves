# 🏃‍♂️ EquipesEleves - Générateur d'équipes sportives équilibrées

> Script Python pour la génération automatique d'équipes aléatoires et paritaires, conçu pour des activités inter-classes.

## 📋 Contexte

Projet développé en 2021 pour automatiser la constitution d'équipes mixtes dans le cadre d'activités sportives impliquant plusieurs classes (environ 75 élèves).

**Problème résolu :** Constitution manuelle chronophage (15-20min/séance), difficulté à garantir la parité filles/garçons et l'équilibre entre classes.

**Impact :** Utilisé pendant 2 ans par 3 enseignants, gain de temps significatif et équipes renouvelées à chaque séance.

## 🛠️ Technologies

- **Python 3.x**
- **CSV natif** (branche `main`)
- **Pandas + XlsxWriter** (branche `Pandas-version` - export Excel avec mise en forme couleur)

## ✨ Fonctionnalités

- ✅ Génération aléatoire d'équipes avec contrainte de parité
- ✅ Équilibrage automatique entre classes
- ✅ Gestion des absences/dispenses
- ✅ Export multi-formats (global, par classe, par équipe)
- ✅ Personnalisation des noms d'équipes
- ✅ Interface en ligne de commande intuitive

## 🚀 Utilisation

### 1. Préparer le fichier CSV

Créez un fichier `liste_eleves.csv` dans le même répertoire que le script :
```csv
nom;prenom;sexe;prof
Dupont;Marie;F;CM1
Martin;Lucas;G;CM2
...
```

**Format :**
- Séparateur : `;` (point-virgule)
- Encodage : UTF-8 (Mac/Linux) ou ANSI (Windows)
- Colonne "prof" : nom du professeur ou classe (ex: "CM1", "6èmeB")

Un fichier exemple avec des noms fictifs est disponible dans le dépôt.

### 2. Lancer le script
```bash
python main.py  # ou le nom de votre fichier principal
```

Le script vous guidera étape par étape pour :
- Choisir le nombre d'équipes
- Gérer les éventuelles dispenses
- Générer le tirage

### 3. Récupérer les résultats

Les résultats sont exportés dans le dossier `tirage_equipes/` :

- **Tirage global** : tous les élèves avec leur équipe (filtrable dans Excel)
- **Par classe/prof** : listes séparées par enseignant
- **Par équipe** : listes prêtes à imprimer

⚠️ **Attention :** Chaque nouveau tirage écrase le précédent.

## 🎨 Personnalisation (optionnel)

### Noms d'équipes personnalisés

Par défaut, les équipes portent des noms de couleurs (pratique pour les chasubles).

Pour personnaliser :

1. Effectuez un premier tirage
2. Un dossier `noms_equipes/` apparaît avec `noms_equipes.csv`
3. Modifiez ce fichier selon vos besoins (ex: "Lions", "Aigles", etc.)
4. Les tirages suivants utiliseront vos noms personnalisés

**Astuce :** Si vous générez 4 équipes, seules les 4 premières lignes du fichier seront utilisées.

## 💡 Apprentissage personnel

Premier projet Python développé en autonomie (sans LLM) en 2021. M'a permis de :
- Découvrir la manipulation de fichiers CSV
- Comprendre l'importance de l'UX pour des utilisateurs non-techniques
- Résoudre un problème opérationnel concret par le code

**Ce projet est à l'origine de ma reconversion vers la Data.**

## 📂 Structure du projet

- `main` : Version CSV basique
- `Pandas-version` : Version avec export Excel formaté et code couleur ⭐

---

📧 Contact : [lucas-mauger](https://github.com/lucas-mauger)
