import sqlite3
import random

nb_equipes_input = input("combien d'équipes ? (répondre en chiffres) : ")
nb_equipes = int(nb_equipes_input)

# liste globale de toutes les équipes
toutes_eq = []

# on initialise la liste pour que la fonction index_tailles_equipes fonctionne
for i in range(0,nb_equipes):
    equipe = []
    toutes_eq.append(equipe)

def index_plus_petite_equipe(liste_equipes) :
    ''' Retourne l'index de l'équipe comptant le moins de joueurs '''
    tailles_equipes = []
    for i in range(0,(len(liste_equipes))):
        tailles_equipes.append(len(liste_equipes[i]))

    min_taille_equipes = min(tailles_equipes)
    index_min_taille_equipes = tailles_equipes.index(min_taille_equipes)
    return index_min_taille_equipes

def couleur_equipe(numero_equipe):
    if numero_equipe == 'équipe 1':
        numero_equipe = 'jaune'
    elif numero_equipe == 'équipe 2':
        numero_equipe = 'rouge'
    elif numero_equipe == 'équipe 3':
        numero_equipe = 'bleu'
    elif numero_equipe == 'équipe 4':
        numero_equipe = 'vert'
    elif numero_equipe == 'équipe 5':
        numero_equipe = 'violet'
    elif numero_equipe == 'équipe 6':
        numero_equipe = 'orange'
    elif numero_equipe == 'équipe 7':
        numero_equipe = 'blanc'
    elif numero_equipe == 'équipe 8':
        numero_equipe = 'noir'
    else:
        numero_equipe = numero_equipe
    return numero_equipe
            

def attribuer_joueur(liste_joueurs):
    ''' Attribue chaque joueur d'une liste de joueurs à l'équipe comportant
    le moins de joueurs au moment de l'attribution.\n
    Nécessite la variable globale "toutes_eq[]" initialisée au préalable. '''
    for joueur in liste_joueurs:
        index_eq = index_plus_petite_equipe(toutes_eq) 
        # les joueurs récupérés dans la liste sont des tuples, 
        # on ne peut pas concaténer des str avec eux
        # donc un crée une liste qui contient les deux informations (infos joueurs + équipe attribuée)
        numero_equipe = (f'équipe {index_eq+1}',) # on évite une "équipe 0"
        joueur_de_liste = []
        joueur_de_liste.append(joueur+numero_equipe)
        toutes_eq[index_eq].append(joueur_de_liste)
    return None


connection = sqlite3.connect('eleves_eps.db')
curseur = connection.cursor()

#On récupère tous les professeurs de la db, sans répétition
curseur.execute('SELECT prof from eleves')
liste_profs = curseur.fetchall()
liste_profs_uniques = list(dict.fromkeys(liste_profs))

# Pour chaque classe, on crée deux listes (filles et garçons)
# sur lesquelles on effectue la fonction "attribuer_joueurs"
for x in range(0,len(liste_profs_uniques)):
    curseur.execute('SELECT * FROM eleves WHERE prof = ?', liste_profs_uniques[x])
    liste_prof = curseur.fetchall()
    liste_filles = []
    liste_garcons = []
    for joueur in liste_prof:
        if joueur[2] == "G":
            liste_garcons.append(joueur)
        elif joueur[2] == "F":
            liste_filles.append(joueur)
        else:
            print("erreur, mauvais sexe récupéré pour ce joueur")
    random.shuffle(liste_filles)
    random.shuffle(liste_garcons)
    attribuer_joueur(liste_filles)
    attribuer_joueur(liste_garcons)

#on supprime les données précédentes de la table
curseur.execute("DELETE FROM joueurs_par_equipes")

# #on met à jour la bonne table avec les équipes
for equipe in toutes_eq:
    for joueur in equipe:
        for detail in joueur:
            curseur.execute("INSERT INTO joueurs_par_equipes VALUES ('"+ detail[0]+ "', '"+ detail[1]+ "', '"+ couleur_equipe(detail[4]) +  "', '"+ detail[3]+"')")


connection.commit()
connection.close()