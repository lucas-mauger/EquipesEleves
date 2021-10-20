import random
import csv
from pathlib import Path
from glob import glob

# liste globale de toutes les équipes
toutes_eq = []

# liste éventuelle des élèves à enlever du tirage
liste_eleves_dispenses = []

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
    # il n'y a pas d'équipe 0, on l'a évité dans le code
    liste_numeros = [i for i in range(1,(len(liste_couleurs)+1))]
    if int(numero_equipe[6:]) in liste_numeros:
        numero_equipe = liste_couleurs[int(numero_equipe[6:])-1]
    return numero_equipe

def gerer_eleves_dispenses(fichier_eleves):
    
    reponse_dispense = '1'
    while reponse_dispense in ['1','2','3','4']:

        # 1 - ajouter un élève à dispenser
        if reponse_dispense == '1':

            # si la liste n'est pas vide, on l'affiche
            if len(liste_eleves_dispenses) != 0:
                print("Élèves dispensés du tirage :")
                for eleve in liste_eleves_dispenses:
                    print(f"  -- {eleve[1]} {eleve[0]}")
            
            # on consulte la liste de tous les élèves
            with open(fichier_eleves,newline='') as db_eleves:
                lecteur = csv.reader(db_eleves,delimiter=';')
                dispense_locale = []
                prenom_eleve = input("Veuillez entrer le prénom (ou les premières lettres du prénom) d'un élève à dispenser du tirage : ")
                while not prenom_eleve.isalpha():
                    prenom_eleve = input("Veuillez ne pas entrer de chiffres. Prénom (ou début de prénom) d'un élève à dispenser ? ")

                for eleve in lecteur:
                    if prenom_eleve in eleve[1]:
                        if eleve not in liste_eleves_dispenses:
                            dispense_locale.append(eleve)
                        else:
                            print("  --  Cet élève est déjà dispensé.")
                
                if len(dispense_locale) != 0:
                    if len(dispense_locale) == 1:
                        liste_eleves_dispenses.append(dispense_locale[0])
                        print("L'élève suivant(e) a été ajouté(e) à la liste des élèves dispensés :")
                        print(f"  --  {dispense_locale[0][1]} {dispense_locale[0][0]}")
                    elif len(dispense_locale) > 1:
                        print("Les élèves suivants ont été trouvés pour cette saisie :")
                        x=1
                        numeros_ajout = [i for i in range(1,(len(dispense_locale)+1))]
                        for eleve in dispense_locale:
                            print(f"  {x} - {eleve[1]} {eleve[0]}")
                            x+=1
                        consigne = input(f"Quel élève ajouter aux élèves dispensés ? {numeros_ajout}")
                        while int(consigne) not in numeros_ajout:
                            consigne = input(f"Veuillez répondre parmi {numeros_ajout} : ")
                        liste_eleves_dispenses.append(dispense_locale[int(consigne)-1])
        

        # 2 - retirer un élève de la liste des dispensés
        if reponse_dispense == '2':
            # si la liste n'est pas vide, on l'affiche
            if len(liste_eleves_dispenses) != 0:
                print("Élèves dispensés du tirage :")
                x=1
                numeros_retrait = [i for i in range(1,(len(liste_eleves_dispenses)+1))]
                for eleve in liste_eleves_dispenses:
                    print(f"  {x} -- {eleve[1]} {eleve[0]}")
                    x+=1

                reponse = input(f"Veuillez entrer le numéro de l'élève à retirer de la liste {numeros_retrait} : ")
                while not reponse.isnumeric():
                    reponse = input(f"Veuillez répondre en chiffres. Entrez le numéro de l'élève à retirer de la liste {numeros_retrait} : ")
                while int(reponse) not in numeros_retrait:
                    reponse = input(f"Réponse irrecevable. Veuillez entrer le numéro de l'élève à dispenser {numeros_retrait} : ")
                eleve_supprime = liste_eleves_dispenses[int(reponse)-1]
                liste_eleves_dispenses.remove(eleve_supprime)
                print(f"  --  L'élève {eleve_supprime[1]} {eleve_supprime[0]} a été supprimé(e) de la liste des élèves à dispenser du tirage.")


            # s'il n'y a pas d'élève dans la liste des dispensés, on sort de la boucle
            else :
                print("Il n'y a aucun élève dispensé pour l'instant.")

        # 3 - consulter la liste des élèves dispensés
        if reponse_dispense == '3':
            if len(liste_eleves_dispenses) != 0:
                print("  |  Liste des élèves dispensés du tirage :")
                for eleve in liste_eleves_dispenses:
                    print(f"  |    -- {eleve[1]} {eleve[0]}")
            else :
                print("  -- Aucun élève dispensé pour l'instant.")

        reponse_dispense = input("Que voulez-vous faire ?\n1 - Ajouter un élève à dispenser.\n2 - Retirer un élève à dispenser de la liste ci-dessus.\n3 - Consulter la liste des élèves dispensés.\n4 - Sortir de la gestion des élèves dispensés.")
        while reponse_dispense not in ['1','2','3','4']:
            reponse_dispense = input("Je n'ai pas compris votre réponse. Que voulez-vous faire ?\n 1 - Ajouter un élève à dispenser.\2 - Retirer un élève à dispenser de la liste ci-dessus.\n3 - Consulter la liste des élèves dispensés.\n4 - Sortir de la gestion des élèves dispensés.")

        if reponse_dispense == '4':
            return liste_eleves_dispenses

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

def repartition_equipes(fichier_eleves_csv):
    with open(fichier_eleves_csv,newline='') as db_eleves:
        lecteur = csv.reader(db_eleves,delimiter=';')
        liste_profs = []
        liste_eleves = []
        x=0 # on passe l'en-tête du fichier csv
        for ligne in lecteur:
            if x>=1:
                liste_profs.append(ligne[3])
                liste_eleves.append(ligne)
            x=x+1
        liste_profs = list(set(liste_profs)) # on supprime les doublons de la liste des profs

        # Pour chaque classe, on crée deux listes (filles et garçons)
        # sur lesquelles on effectue la fonction "attribuer_joueurs"
        for x in range(0,len(liste_profs)):
            liste_filles = []
            liste_garcons = []
            with open(fichier_eleves_csv, newline='') as eleves_classe:
                lecteur = csv.reader(eleves_classe, delimiter=';')
                y=0
                for eleve in lecteur:
                    if y >= 1 and eleve[3] == liste_profs[x]:
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

    with open('./tirage_equipes/equipes_eleves.csv', 'w', newline='',encoding='ansi') as equipes_attribuees:
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
    reponse_fichier_eleves = input("Voulez-vous l'utiliser pour la répartition (o/n) ? ")
    while reponse_fichier_eleves not in ['o','n']:
        reponse_fichier_eleves = input(f"Je n'ai pas compris votre réponse.\nVoulez-vous utiliser le fichier \"{liste_fichiers_csv[0][2:]}\" pour la répartition ? (o/n)")
    if reponse_fichier_eleves == 'n':
        print("Les équipes n'ont pas été réparties.\nFin du programme.")
    else:
        fichier_eleves = f'{liste_fichiers_csv[0][2:]}'
        nb_equipes_input = input("Combien d'équipes pour la répartition ? (répondre en chiffres) : ")
        while not nb_equipes_input.isnumeric():
            nb_equipes_input = input("Veuillez répondre en chiffres. Combien d'équipes pour la répartition ? ")
        nb_equipes = int(nb_equipes_input)
        # on initialise la liste pour que la fonction index_plus_petite_equipe fonctionne
        for i in range(0,nb_equipes):
            equipe = []
            toutes_eq.append(equipe)

        
        reponse = input("Que voulez-vous faire ?\n1 - Procéder au tirage.\n2 - Ajouter ou gérer des élèves à dispenser.")
        while reponse not in ['1','2']:
            reponse = input("Je n'ai pas compris votre réponse.\nQue voulez-vous faire ?\n1 - Procéder au tirage.\n2 - Ajouter ou gérer des élèves à dispenser.")
        
        #on établit une liste des élèves à dispenser du tirage
        while reponse=='2':
            gerer_eleves_dispenses(fichier_eleves)           

            print("Les élèves suivants ne feront pas partie du tirage des équipes :")
            for eleve in liste_eleves_dispenses:
                print(f"  -- {eleve[1]} {eleve[0]}")
            reponse = input("Que voulez-vous faire ?\n1 - Procéder au tirage des équipes.\n2 - Modifier la liste des élèves dispensés.")
            while reponse not in ['1','2']:
                reponse = input('Veuillez répondre "1" ou "2".\n1 - Procéder au tirage des équipes.\n2 - Modifier la liste des élèves dispensés.')

        if reponse == '1':
            repartition_equipes(fichier_eleves)
            print("Répartition des équipes effectuée.\nVous la trouverez dans le dossier \"tirage_equipes\"")
            input("Appuyez sur Entrée pour quitter le programme.")