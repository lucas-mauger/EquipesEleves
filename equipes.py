import random
import csv
from pathlib import Path
from glob import glob

nb_equipes_input = input("Combien d'équipes pour la répartition ? (répondre en chiffres) : ")
while not nb_equipes_input.isnumeric():
    nb_equipes_input = input("Veuillez répondre en chiffres. Combien d'équipes pour la répartition ? ")
nb_equipes = int(nb_equipes_input)
fichier_eleves = "liste_eleves.csv"

# liste globale de toutes les équipes
toutes_eq = []

liste_profs = []
liste_eleves = []

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
    liste_couleurs = ['jaune','rouge','bleu','vert','violet','orange','blanc','noir']
    liste_numeros = []
    y=1 # il n'y a pas d'équipe 0, on l'a évité dans le code
    for x in range(0,len(liste_couleurs)):
        liste_numeros.append(y)
        y=y+1
    if int(numero_equipe[6:]) in liste_numeros:
        numero_equipe = liste_couleurs[int(numero_equipe[6:])-1]
    else:
        numero_equipe = numero_equipe
    return numero_equipe

def attribuer_joueur(liste_joueurs):
    ''' Attribue chaque joueur d'une liste de joueurs à l'équipe comportant
    le moins de joueurs au moment de l'attribution.\n
    Nécessite la variable globale "toutes_eq[]" initialisée au préalable.'''
    for joueur in liste_joueurs:
        index_eq = index_plus_petite_equipe(toutes_eq) 
        numero_equipe = (f'équipe {index_eq+1}') # on évite une "équipe 0"
        joueur.append(numero_equipe)
        toutes_eq[index_eq].append(joueur)
    return None

def programme_principal(fichier_eleves_csv,profs_liste):
    with open(fichier_eleves_csv,newline='') as db_eleves:
        lecteur = csv.reader(db_eleves,delimiter=';')
        x=0 # on passe l'en-tête du fichier csv
        for ligne in lecteur:
            if x>=1:
                profs_liste.append(ligne[3])
                liste_eleves.append(ligne)
            x=x+1
        profs_liste = list(set(profs_liste)) # on supprime les doublons de la liste des profs

        # Pour chaque classe, on crée deux listes (filles et garçons)
        # sur lesquelles on effectue la fonction "attribuer_joueurs"
        for x in range(0,len(profs_liste)):
            liste_filles = []
            liste_garcons = []
            with open(fichier_eleves_csv, newline='') as eleves_classe:
                lecteur = csv.reader(eleves_classe, delimiter=';')
                y=0
                for eleve in lecteur:
                    if y >= 1 and eleve[3] == profs_liste[x]:
                        if eleve[2] == 'F':
                            liste_filles.append(eleve)
                        elif eleve[2] in ['G','M']:
                            liste_garcons.append(eleve)
                        else:
                            print("Erreur de renseignement du sexe de l'élève")
                    y=y+1

            random.shuffle(liste_filles)
            random.shuffle(liste_garcons)
            attribuer_joueur(liste_filles)
            attribuer_joueur(liste_garcons)


    path = Path('./tirage_equipes')
    path.mkdir(exist_ok=True)

    with open('./tirage_equipes/equipes_eleves.csv', 'w', newline='',encoding='utf-8') as equipes_attribuees:
        scripteur = csv.writer(equipes_attribuees, delimiter=';')
        scripteur.writerow(['nom','prenom','equipe','prof'])
        for equipe in toutes_eq:
            for eleve in equipe:
                scripteur.writerow([eleve[0],eleve[1],couleur_equipe(eleve[4]),eleve[3]])



pth ="./"
liste_fichiers_csv = glob(pth+"*.csv")
if len(liste_fichiers_csv)>1:
    print("Il y a plusieurs fichiers csv dans le répertoire :")
    for fichier in liste_fichiers_csv:
        if fichier[2:] != 'equipes_eleves.csv':
            print(f"-- {fichier[2:]} --")
    print("Veuillez ne conserver que le fichier qui contient la liste des élèves à répartir, puis relancez le programme.")
else:
    print(f"Le fichier \"{liste_fichiers_csv[0][2:]}\" a été trouvé dans le répertoire.")
    reponse_bool = input("Voulez-vous l'utiliser pour la répartition (o/n) ? ")
    while reponse_bool not in ['o','n']:
        reponse_bool = input(f"Je n'ai pas compris votre réponse.\nVoulez-vous utiliser le fichier \"{liste_fichiers_csv[0][2:]}\" pour la répartition ? (o/n)")
    if reponse_bool == 'n':
        print("Les équipes n'ont pas été réparties.\nFin du programme.")
    else:
        fichier_eleves = f'{liste_fichiers_csv[0][2:]}'
        programme_principal(fichier_eleves, liste_profs)
        print("Répartition des équipes effectuée.\nVous la trouverez dans le dossier \"tirage_equipes\"")
        input("Appuyez sur Entrée pour quitter le programme.")