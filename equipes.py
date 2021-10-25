import random
import csv
from pathlib import Path
from glob import glob

# liste globale de toutes les équipes
toutes_eq = []

# liste des élèves du fichier csv
liste_eleves = []

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

def gerer_eleves_dispenses():
    
    afficher_menu = True
    reponse_dispense = '1'    
    while afficher_menu and reponse_dispense in ['1','2','3','4']:
        print('')
        print("Que voulez-vous faire ?")
        print("1 - Ajouter un élève à dispenser.")
        print("2 - Retirer un élève à dispenser.")
        print("3 - Consulter la liste des élèves dispensés.")
        reponse_dispense = input("4 - Sortir de la gestion des élèves dispensés.")
        while reponse_dispense not in ['1','2','3','4']:
            print('')
            print("Je n'ai pas compris votre réponse.")
            print("Que voulez-vous faire ?")
            print("1 - Ajouter un élève à dispenser.")
            print("2 - Retirer un élève à dispenser.")
            print("3 - Consulter la liste des élèves dispensés.")
            reponse_dispense = input("4 - Sortir de la gestion des élèves dispensés.")


        # 1 - ajouter un élève à dispenser
        if reponse_dispense == '1':
            ajouter_dispense()
        # 2 - retirer un élève de la liste des dispensés
        if reponse_dispense == '2':
            retirer_dispense()
        # 3 - consulter la liste des élèves dispensés
        if reponse_dispense == '3':
            consulter_dispense()
        # 4 - sortir de la gestion des dispenses
        if reponse_dispense == '4':
            afficher_menu = False
    return None

def ajouter_dispense():

    if len(liste_eleves_dispenses) != 0:
        print('')
        print("Élèves dispensés du tirage :")
        for eleve in liste_eleves_dispenses:
            print(f"  -- {eleve[1]} {eleve[0]}")
        print('')
            
    # on consulte la liste de tous les élèves
    dispense_locale = []
    prenom_eleve = input("Veuillez entrer le prénom (ou les premières lettres du prénom) d'un élève à dispenser du tirage : ")
    while not prenom_eleve.isalpha():
        prenom_eleve = input("Veuillez ne pas entrer de chiffres. Prénom (ou début de prénom) d'un élève à dispenser ? ")

    for eleve in liste_eleves:
        if prenom_eleve in eleve[1][0:]:
            if eleve not in liste_eleves_dispenses:
                dispense_locale.append(eleve)
            else:
                print('')
                if eleve[2] == 'F':
                    print("  --  Cette élève est déjà dispensée.")
                elif eleve[2] in ['G','M']:
                    print("  --  Cet élève est déjà dispensé.")
                else:
                    print("  -- erreur : mauvais sexe renseigné pour cet/cette élève.")
                print('')
    
    liste_prenoms = [eleve[1] for eleve in liste_eleves[1:]]
    test_prenom = [s for s in liste_prenoms if prenom_eleve in s]
    if not test_prenom:
        print('')
        print('  --  Aucun élève trouvé pour cette saisie.')
        print('')

    if len(dispense_locale) != 0:
        if len(dispense_locale) == 1:
            liste_eleves_dispenses.append(dispense_locale[0])
            print('')
            print("L'élève suivant(e) a été ajouté(e) à la liste des élèves dispensés :")
            print(f"  --  {dispense_locale[0][1]} {dispense_locale[0][0]}")
        elif len(dispense_locale) > 1:
            print('')
            print("Les élèves suivants ont été trouvés pour cette saisie :")
            for eleve in dispense_locale:
                print(f"  {dispense_locale.index(eleve)+1} - {eleve[1]} {eleve[0]}")
            print('')
            
            numeros_ajout = [i for i in range(1,(len(dispense_locale)+1))]
            consigne = input(f"Quel élève ajouter aux élèves dispensés ? {numeros_ajout}")
            while int(consigne) not in numeros_ajout:
                consigne = input(f"Veuillez répondre parmi {numeros_ajout} : ")
            liste_eleves_dispenses.append(dispense_locale[int(consigne)-1])
            
    return None

def retirer_dispense():

    # si la liste n'est pas vide, on l'affiche
    if liste_eleves_dispenses:
        print('')
        print("Élèves dispensés du tirage :")
        numeros_retrait = [i for i in range(1,(len(liste_eleves_dispenses)+1))]
        for eleve in liste_eleves_dispenses:
            print(f"  {liste_eleves_dispenses.index(eleve)+1} -- {eleve[1]} {eleve[0]}")
        print('')

        reponse = input(f"Veuillez entrer le numéro de l'élève à retirer de la liste {numeros_retrait} : ")
        while not reponse.isnumeric():
            reponse = input(f"Veuillez répondre en chiffres. Entrez le numéro de l'élève à retirer de la liste {numeros_retrait} : ")
        while int(reponse) not in numeros_retrait:
            reponse = input(f"Réponse irrecevable. Veuillez entrer le numéro de l'élève à dispenser {numeros_retrait} : ")
        eleve_supprime = liste_eleves_dispenses[int(reponse)-1]
        liste_eleves_dispenses.remove(eleve_supprime)
        print('')
        print(f"  --  L'élève {eleve_supprime[1]} {eleve_supprime[0]} a été supprimé(e) de la liste des élèves à dispenser du tirage.")
        print('')

    # s'il n'y a pas d'élève dans la liste des dispensés, on sort de la boucle
    else :
        print('')
        print("  --  Il n'y a aucun élève dispensé pour l'instant.")

    return None

def consulter_dispense():
    if len(liste_eleves_dispenses) != 0:
        print('')
        print("  |  Liste des élèves dispensés du tirage :")
        for eleve in liste_eleves_dispenses:
            print(f"  |    -- {eleve[1]} {eleve[0]}")
    else :
        print('')
        print("    -- Aucun élève dispensé pour l'instant.")
    
    return None

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

def repartition_equipes():

    if liste_eleves_dispenses:
        print('')
        print(f"Nombre d'élèves avant dispense : {len(liste_eleves)}")
        # on supprime les éventuels élèves dispensés de la liste utilisée pour le tirage
        for eleve in liste_eleves_dispenses:
            liste_eleves.remove(eleve)
        print(f"Nombre d'élèves répartis après dispense : {len(liste_eleves)}")
        print('')
    else:
        print('')
        print(f"Nombre d'élèves répartis : {len(liste_eleves)}")
        print('')

    liste_profs = []
    for eleve in liste_eleves[1:]:
        liste_profs.append(eleve[3])
    liste_profs = list(set(liste_profs)) # on supprime les doublons de la liste des profs

    # Pour chaque classe, on crée deux listes (filles et garçons)
    # sur lesquelles on effectue la fonction "attribuer_joueurs"
    for x in range(0,len(liste_profs)):
        liste_filles = []
        liste_garcons = []

        for eleve in liste_eleves[1:]:
            if eleve[3] == liste_profs[x] and eleve[2] == 'F':
                liste_filles.append(eleve)
            elif eleve[3] == liste_profs[x] and eleve[2] in ['G','M']:
                liste_garcons.append(eleve)
            elif eleve[3] == liste_profs[x] and not eleve[2] in ['F','G','M']:
                print("Erreur de renseignement du sexe de l'élève")

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


#Vérification de la présence d'un fichier csv à traiter
pth ="./"
liste_fichiers_csv = glob(pth+"*.csv")

if not(liste_fichiers_csv):
    print("Aucune liste d'élèves à traiter (fichier csv) trouvée dans le répertoire.")
    print("Veuillez fournir une liste d'élèves avant de lancer ce programme.")
    input("Appuyez sur Entrée pour quitter.")

elif len(liste_fichiers_csv)>1:
    print("Il y a plusieurs fichiers csv dans le répertoire :")
    for fichier in liste_fichiers_csv:
        print(f"    -- {fichier[2:]}")
    print("Veuillez ne conserver que le fichier qui contient la liste des élèves à répartir, puis relancez le programme.")
    input("Appuyez sur Entrée pour mettre fin au programme.")
else:
    print(f"Le fichier \"{liste_fichiers_csv[0][2:]}\" a été trouvé dans le répertoire.")
    reponse_fichier_eleves = input("Voulez-vous l'utiliser pour la répartition (o/n) ? ")
    while reponse_fichier_eleves not in ['o','n']:
        print("Je n'ai pas compris votre réponse.")
        reponse_fichier_eleves = input(f"Voulez-vous utiliser le fichier \"{liste_fichiers_csv[0][2:]}\" pour la répartition ? (o/n)")
    if reponse_fichier_eleves == 'n':
        print("Les équipes n'ont pas été réparties.\nFin du programme.")
    else:
        fichier_eleves = f'{liste_fichiers_csv[0][2:]}'
        nb_equipes_input = input("Combien d'équipes pour la répartition ? (répondre en chiffres) : ")
        while not nb_equipes_input.isnumeric():
            nb_equipes_input = input("Veuillez répondre en chiffres : ")
        nb_equipes = int(nb_equipes_input)
        # on initialise la liste pour que la fonction index_plus_petite_equipe fonctionne
        for i in range(0,nb_equipes):
            equipe = []
            toutes_eq.append(equipe)

        with open(fichier_eleves,newline='') as db_eleves:
            lecteur = csv.reader(db_eleves,delimiter=';')
            x=0
            for eleve in lecteur:
                if x>0:
                    liste_eleves.append(eleve)
                x+=1 # on passe l'en-tête du csv
            print(f"Nombres d'élèves trouvés dans le fichier : {len(liste_eleves)}")


        afficher_menu = True
        reponse = '1'

        while afficher_menu == True and reponse in ['1','2']:
            print('')
            print("Que voulez-vous faire ?")
            print("1 - Procéder au tirage.")
            reponse = input("2 - Ajouter ou gérer des élèves à dispenser.")
            while reponse not in ['1','2']:
                print('')
                print("  -->  Je n'ai pas compris votre réponse.")
                print('')
                print("Que voulez-vous faire ?")
                print("1 - Procéder au tirage.")
                reponse = input("2 - Ajouter ou gérer des élèves à dispenser.") 
                   
            # on établit une liste des élèves à dispenser du tirage
            if reponse=='2':
                gerer_eleves_dispenses()           

                if liste_eleves_dispenses:
                    print('')
                    print("  |  Les élèves suivants ne feront pas partie du tirage des équipes :")
                    for eleve in liste_eleves_dispenses:
                        print(f"  |    -- {eleve[1]} {eleve[0]}")
            
            if reponse == '1':
                repartition_equipes()
                afficher_menu = False
                print("Répartition des équipes effectuée.")
                print("Vous la trouverez dans le dossier \"tirage_equipes\".")
                input("Appuyez sur Entrée pour quitter le programme.")