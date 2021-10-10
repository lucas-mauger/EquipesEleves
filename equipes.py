from os import X_OK
import sqlite3
import random
import csv

nb_equipes_input = input("combien d'équipes ? (répondre en chiffres) : ")
nb_equipes = int(nb_equipes_input)

# liste globale de toutes les équipes
toutes_eq = []

# on initialise la liste pour que la fonction index_plus_petite_equipe fonctionne
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
    Nécessite la variable globale "toutes_eq[]" initialisée au préalable.'''
    for joueur in liste_joueurs:
        index_eq = index_plus_petite_equipe(toutes_eq) 
        # les joueurs récupérés dans la liste sont des tuples, 
        # on ne peut pas concaténer des str avec eux
        # donc un crée une liste qui contient les deux informations (infos joueurs + équipe attribuée)
        numero_equipe = (f'équipe {index_eq+1}') # on évite une "équipe 0"
        joueur.append(numero_equipe)
        # joueur_de_liste = []
        # joueur_de_liste.append(joueur+numero_equipe)
        toutes_eq[index_eq].append(joueur)
    return None



liste_eleves = []
liste_profs = []

with open("liste_eleves_db.csv",newline='') as db_eleves:
    lecteur = csv.reader(db_eleves)
    x=0 # on passe l'en-tête du fichier csv
    for ligne in lecteur:
        if x>=1:
            liste_profs.append(ligne[3])
            liste_eleves.append(ligne)
        x=x+1
    liste_profs = list(set(liste_profs)) # on supprime les doublons de la liste des profs

    print(liste_profs)
# connection = sqlite3.connect('eleves_eps.db')
# curseur = connection.cursor()

# #On récupère tous les professeurs de la db, sans répétition
# curseur.execute('SELECT prof from eleves')
# liste_profs = curseur.fetchall()
# liste_profs_uniques = list(dict.fromkeys(liste_profs))

# Pour chaque classe, on crée deux listes (filles et garçons)
# sur lesquelles on effectue la fonction "attribuer_joueurs"
for x in range(0,len(liste_profs)):
    liste_filles = []
    liste_garcons = []
    with open('liste_eleves_db.csv', newline='') as eleves_classe:
        lecteur = csv.reader(eleves_classe)
        y=0
        for eleve in lecteur:
            if y >= 1:
                if eleve[2] == 'F' and eleve[3] == liste_profs[x]:
                    liste_filles.append(eleve)
                elif eleve[2] == 'G' and eleve[3] == liste_profs[x]:
                    liste_garcons.append(eleve)
            else:
                "erreur de test prof"
            y=y+1



    random.shuffle(liste_filles)
    random.shuffle(liste_garcons)
    attribuer_joueur(liste_filles)
    attribuer_joueur(liste_garcons)

for equipe in toutes_eq:
    for eleve in equipe:
        print(eleve)

with open('liste_equipes.csv', 'w', newline='',encoding='utf-8') as equipes_attribuees:
    scripteur = csv.writer(equipes_attribuees)
    scripteur.writerow(['nom','prenom','equipe','prof'])
    for equipe in toutes_eq:
        for eleve in equipe:
            scripteur.writerow([eleve[0],eleve[1],couleur_equipe(eleve[4]),eleve[3]])
# #on supprime les données précédentes de la table
# curseur.execute("DELETE FROM joueurs_par_equipes")

# # #on met à jour la bonne table avec les équipes
# for equipe in toutes_eq:
#     for joueur in equipe:
#         for detail in joueur:
#             curseur.execute("INSERT INTO joueurs_par_equipes VALUES ('"+ detail[0]+ "', '"+ detail[1]+ "', '"+ couleur_equipe(detail[4]) +  "', '"+ detail[3]+"')")


# connection.commit()
# connection.close()