from email import header
import random
import numpy
import os
import pandas as pd
from requests import head
import xlsxwriter
from pathlib import Path
from glob import glob
import shutil
import sys

# nom du fichier utilisé comme base de données des élèves
fichier_eleves = ''

# liste globale de toutes les équipes
toutes_eq = []

# liste des élèves du fichier xlsx
liste_eleves = []

# liste éventuelle des élèves à enlever du tirage
liste_eleves_dispenses = []

# liste des noms des équipes, récupérée dans file_noms_eq
noms_equipes = []
path_noms_eq = Path('./noms_equipes/')
file_noms_eq = Path(f'{path_noms_eq}/noms_equipes.xlsx')
print(file_noms_eq)
# liste des noms d'équipe par défaut si absence de spécification par l'utilisateur
DefaultTeamNames = ['jaune','rouge','bleu','vert','violet','orange','blanc','noir','rose','gris']

def index_plus_petite_equipe(liste_equipes) :
    ''' Retourne l'index de l'équipe comptant le moins de joueurs '''
    tailles_equipes = []
    for i in range(0,(len(liste_equipes))):
        tailles_equipes.append(len(liste_equipes[i]))
    min_taille_equipes = min(tailles_equipes)
    index_min_taille_equipes = tailles_equipes.index(min_taille_equipes)
    return index_min_taille_equipes

def renommer_equipe(numero_equipe):
    ''' Attribue des noms aux équipes selon le contenu du fichier "noms_equipes" '''

    # il n'y a pas d'équipe 0, on l'a évité dans le code
    liste_numeros = [i for i in range(1,(len(noms_equipes)+1))]
    if int(numero_equipe[6:]) in liste_numeros:
        numero_equipe = noms_equipes[int(numero_equipe[6:])-1]
    return numero_equipe

def generer_xlsx(WB: xlsxwriter.Workbook, DF: pd.DataFrame, ExcelSheetName='Sheet1'):
    ''' Récupère les données du dataframe pandas pour ajouter une feuille Excel mise en page,\n
    dans le xlsxwriter.Workbook entré en paramètre.\n
    Gère automatiquement les largeurs de colonnes, couleurs et met en place les autofiltres.\n
    Retourne un Workbook XlsxWriter à clôturer (en cas de feuilles multiples). \n
    ExcelSheetName (facultatif) : str. Permet de spécifier le nom de la feuille dans le fichier Excel.'''
    
    # On vérifie que 'Équipes' fait partie des headers du dataframe
    # Le cas échéant, on crée une sous-liste des noms d'équipe par index
    TeamsIndex = []
    if 'Équipe' in DF.columns.values.tolist(): 
        TeamsIndex = DF["Équipe"].tolist()

    PlayersList = DF.values.tolist()
    headers = DF.columns.values.tolist()
    WS = WB.add_worksheet(ExcelSheetName)

    # règles de mise en forme des headers
    bold_red = WB.add_format({'bold': 1,'color':'red'})
    
    row=0
    col=0

    # on écrit les headers mis en forme, avec autofiltre
    WS.write_row(row,col,headers,bold_red)
    row += 1
    WS.autofilter(0,0,0,len(headers)-1)

    # on ajuste la largeur de colonne selon le plus long str (header compris)
    for i in range(0,len(PlayersList[0])):
        l = 0
        llist = [len(headers[i])]
        for eleve in PlayersList:
            llist.append(len(eleve[i]))
        l = max(llist)
        WS.set_column(i,i,width=l+2)

    ColorList = ['yellow','red','blue','green','purple','orange','white','black','pink','gray']
    WhiteFont_ColorList = ['blue','purple','black','green','red','pink']
    color_select = ''

    # on écrit les joueurs de la liste 
    for eleve in PlayersList:
        if TeamsIndex: # on écrit une feuille où la colonne "Équipe" apparaît
            t_id = TeamsIndex[PlayersList.index(eleve)] # retourne le nom de l'équipe associée à l'élève
            color_select = ColorList[noms_equipes.index(t_id)] # retourne la couleur associée à l'équipe
        else : # on est en train d'écrire une feuille de joueurs par équipes
            color_select = ColorList[noms_equipes.index(ExcelSheetName)]
    
        if color_select in WhiteFont_ColorList:
            bg_color = WB.add_format({'bg_color':f'{color_select}', 'font_color':'white'})
        else:
            bg_color = WB.add_format({'bg_color':f'{color_select}'})
        WS.write_row(row,0,eleve,bg_color) # appliquer un cell_format selon le nom de l'équipe
        row+=1

    return WB

def gerer_eleves_dispenses():
    ''' Affiche le menu de gestion des dispenses/absences d'élèves avant tirage '''
    
    afficher_menu = True
    reponse_dispense = '1'    
    while reponse_dispense in ['1','2','3','4'] and afficher_menu:
        while afficher_menu:
            print('')
            if reponse_dispense not in ['1','2','3','4']:
                print('  ---------------------------------')
                print("  Je n'ai pas compris votre réponse.")
                print("  Répondez parmi [1,2,3,4].")
                print('  ---------------------------------')
                print('')

            print("Que voulez-vous faire ?")
            print("1 - Ajouter un élève à dispenser.")
            print("2 - Retirer un élève à dispenser.")
            print("3 - Consulter la liste des élèves dispensés.")
            reponse_dispense = input("4 - Sortir de la gestion des élèves dispensés.")
            if reponse_dispense in ['1','2','3','4']:
                afficher_menu = False


        # 1 - ajouter un élève à dispenser
        if reponse_dispense == '1':
            ajouter_dispense()
            afficher_menu = True
        # 2 - retirer un élève de la liste des dispensés
        if reponse_dispense == '2':
            retirer_dispense()
            afficher_menu = True
        # 3 - consulter la liste des élèves dispensés
        if reponse_dispense == '3':
            consulter_dispense()
            afficher_menu = True
        # 4 - sortir de la gestion des dispenses, ne plus afficher le menu correspondant
        if reponse_dispense == '4':
            afficher_menu = False
    return None

def ajouter_dispense():
    ''' Ajoute un élève à la liste de ceux qu'il ne faut pas compter au tirage '''

    if liste_eleves_dispenses:
        print('')
        print("  |  Élèves déjà dispensés du tirage :")
        for eleve in liste_eleves_dispenses:
            print(f"  |    -- {eleve[1]} {eleve[0].upper()}")
            
    dispense_locale = []
    print('')
    prenom_eleve = input("Veuillez entrer le prénom (ou les premières lettres du prénom) d'un élève à dispenser du tirage : ")
    while not prenom_eleve.isalpha():
        prenom_eleve = input("Veuillez ne pas entrer de chiffres. Prénom (ou début de prénom) d'un élève à dispenser ? ")

    # on réduit le str à des minuscules pour éviter de rater les majuscules lors de la recherche
    # prenom_eleve = prenom_eleve.lower()

    for eleve in liste_eleves:
        if prenom_eleve.lower() in eleve[1][0:len(prenom_eleve)].lower():
            if eleve not in liste_eleves_dispenses:
                dispense_locale.append(eleve)
            else:
                print('')
                print("  --  Cet·te élève est déjà dispensé·e.")
    
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
                print(f"  {dispense_locale.index(eleve)+1} - {eleve[1]} {eleve[0].upper()}")
            print('')
            
            numeros_ajout = [i for i in range(1,(len(dispense_locale)+1))]
            consigne = input(f"Quel élève ajouter aux élèves dispensés ? {numeros_ajout}")
            while int(consigne) not in numeros_ajout:
                consigne = input(f"Veuillez répondre parmi {numeros_ajout} : ")
            liste_eleves_dispenses.append(dispense_locale[int(consigne)-1])
            
    return None

def retirer_dispense():
    ''' Retire un élève de la liste des élèves non comptés au tirage (l'élève participe de nouveau au tirage aléatoire) '''

    # si la liste n'est pas vide, on l'affiche
    if liste_eleves_dispenses:
        print('')
        print("Élèves dispensés du tirage :")
        numeros_retrait = [i for i in range(1,(len(liste_eleves_dispenses)+1))]
        for eleve in liste_eleves_dispenses:
            print(f"  {liste_eleves_dispenses.index(eleve)+1} -- {eleve[1]} {eleve[0].upper()}")
        print('')

        reponse = input(f"Veuillez entrer le numéro de l'élève à retirer de la liste {numeros_retrait} : ")
        while not reponse.isnumeric():
            reponse = input(f"Veuillez répondre en chiffres. Entrez le numéro de l'élève à retirer de la liste {numeros_retrait} : ")
        while int(reponse) not in numeros_retrait:
            reponse = input(f"Réponse irrecevable. Veuillez entrer le numéro de l'élève à dispenser {numeros_retrait} : ")
        eleve_supprime = liste_eleves_dispenses[int(reponse)-1]
        liste_eleves_dispenses.remove(eleve_supprime)
        print('')
        print(f"  --  L'élève {eleve_supprime[1]} {eleve_supprime[0].upper()} a été supprimé(e) de la liste des élèves à dispenser du tirage.")

    # s'il n'y a pas d'élève dans la liste des dispensés, on sort de la boucle
    else :
        print('')
        print("  --  Il n'y a aucun élève dispensé pour l'instant.")

    return None

def consulter_dispense():
    ''' Affiche une liste contenant les élèves qui ne seront pas pris en compte au tirage aléatoire des équipes '''

    if len(liste_eleves_dispenses) != 0:
        print('')
        print("  |  Liste des élèves dispensés du tirage :")
        for eleve in liste_eleves_dispenses:
            print(f"  |    -- {eleve[1]} {eleve[0].upper()}")
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

def repartition_equipes(liste_eleves):
    ''' Génère pour chaque classe les listes de filles et de garçons à répartir dans les équipes,\n
    en mélange l'ordre aléatoirement, puis effectue l'attribution dans les fichiers Excel. '''

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
    for eleve in liste_eleves:
        if eleve[3] not in liste_profs:
            liste_profs.append(eleve[3])

    # Pour chaque classe, on crée deux listes (filles et garçons)
    # sur lesquelles on effectue la fonction "attribuer_joueurs"
    for x in range(0,len(liste_profs)):
        liste_filles = []
        liste_garcons = []

        for eleve in liste_eleves:
            if eleve[3] == liste_profs[x] and eleve[2] == 'F':
                liste_filles.append(eleve)
            elif eleve[3] == liste_profs[x] and eleve[2] in ['G','M']:
                liste_garcons.append(eleve)
            elif eleve[3] == liste_profs[x] and not eleve[2] in ['F','G','M']:
                random_gender = random.choice(['filles','garçons'])
                if random_gender == "filles":
                    liste_filles.append(eleve)
                else: # random_gender == "garçons"
                    liste_garcons.append(eleve)
                print('  /!\\   /!\\   /!\\   /!\\   /!\\   /!\\')
                print('  ---------------------------------------')
                print(f"  Erreur de renseignement du sexe de l'élève {eleve[1]} {eleve[0].upper()} (indiquez 'F' ou 'G').")
                print("  Veuillez vérifier vos informations.")
                print(f"  Pour ce tirage, l'élève sera réparti·e aléatoirement chez les {random_gender}.")
                print('  ---------------------------------------')
                print('  /!\\   /!\\   /!\\   /!\\   /!\\   /!\\')
                print('')

        random.shuffle(liste_filles)
        random.shuffle(liste_garcons)
        attribuer_joueur(liste_filles)
        attribuer_joueur(liste_garcons)

    # nettoyage éventuel des fichiers du dossier "tirage_equipes"
    pth = './tirage_equipes/'
    tirage = glob(pth+'*')

    for fichier in tirage:
        if os.path.isfile(fichier):
            os.remove(fichier)
        else:
            shutil.rmtree(fichier) 

    # création éventuelle du dossier pour placer les tirages
    path = Path('./tirage_equipes')
    path.mkdir(exist_ok=True)

    lj_att = [] #liste complète des joueurs avec équipes renommées et attribuées
    for equipe in toutes_eq:
        for joueur in equipe:
            joueur[4] = renommer_equipe(joueur[4])
            lj_att.append(joueur)
    lj_att.sort()

    
    DF_listejoueurs = pd.DataFrame(lj_att,columns=['NOM','Prénom','Sexe','Prof','Équipe'])


    # création du fichier Excel avec tirage global (une seule feuille)
    WB = xlsxwriter.Workbook('./tirage_equipes/tirage_global.xlsx')
    DF_listejoueurs = DF_listejoueurs[['NOM','Prénom','Équipe','Prof']]
    DF_listejoueurs = DF_listejoueurs.sort_values(by=['Prof','Équipe'])
    generer_xlsx(WB,DF_listejoueurs,'tirage général')
    WB.close()

    # création du fichier Excel avec tirage par profs (une feuille par prof)
    WB = xlsxwriter.Workbook('./tirage_equipes/tirage_profs.xlsx')
    for prof in liste_profs:
        DF_ListeJoueursParProf = DF_listejoueurs[DF_listejoueurs['Prof']==prof]
        DF_ListeJoueursParProf = DF_ListeJoueursParProf[['NOM','Prénom','Équipe']]
        generer_xlsx(WB,DF_ListeJoueursParProf,prof)
    WB.close() # on clôt seulement après avoir ajouté toutes les feuilles

    # on récupère une liste des noms d'équipes
    leq = []
    for eleve in lj_att:
        if eleve[4] not in leq:
            leq.append(eleve[4])
    
    # création du fichier Excel avec tirage par équipes (une feuille par équipe)
    WB = xlsxwriter.Workbook('./tirage_equipes/tirage_équipes.xlsx')
    for nom_eq in leq:
        DF_ListeJoueursParEquipe = DF_listejoueurs[DF_listejoueurs['Équipe']==nom_eq]
        DF_ListeJoueursParEquipe = DF_ListeJoueursParEquipe[['NOM','Prénom','Prof']]
        generer_xlsx(WB,DF_ListeJoueursParEquipe,nom_eq)
    WB.close() # on clôt seulement après avoir ajouté toutes les feuilles

def programme_principal():
    ''' Interface de dialogue avec l'utilisateur, permettant de définir le nombre d'équipes,\n
    et l'éventuelle gestion des élèves absents/dispensés du tirage aléatoire des équipes. '''

    nb_equipes_input = input("Combien d'équipes pour la répartition ? (répondre en chiffres) : ")
    while not nb_equipes_input.isnumeric():
        nb_equipes_input = input("Veuillez répondre en chiffres : ")
    nb_equipes = int(nb_equipes_input)
    # on initialise la liste pour que la fonction index_plus_petite_equipe fonctionne
    for i in range(0,nb_equipes):
        equipe = []
        toutes_eq.append(equipe)

    # récupérer les noms d'élèves renseignés et les ajouter à la liste liste_eleves[] 
    DF_liste_eleves = pd.read_excel(fichier_eleves, index_col=None).values.tolist()
    for eleve in DF_liste_eleves:
        liste_eleves.append(eleve)

    afficher_menu = True
    reponse = '1'
    while afficher_menu and reponse in ['1','2']:
        while afficher_menu:
            print('')
            if reponse not in ['1','2']:
                print('  ---------------------------------')
                print("  Je n'ai pas compris votre réponse.")
                print('  Veuillez répondre parmi [1,2]')
                print('  ---------------------------------')
                print('')
            print("Que voulez-vous faire ?")
            print("1 - Procéder au tirage.")
            reponse = input("2 - Ajouter ou gérer des élèves à dispenser.")
            if reponse in ['1','2']:
                afficher_menu = False
                
        # on établit une liste des élèves à dispenser du tirage
        if reponse=='2':
            gerer_eleves_dispenses()
            if liste_eleves_dispenses:
                print('')
                print("  |  Les élèves suivants ne feront pas partie du tirage des équipes :")
                for eleve in liste_eleves_dispenses:
                    print(f"  |    -- {eleve[1]} {eleve[0].upper()}")
            afficher_menu = True # on réaffiche le menu principal à l'issue de la gestion des dispenses
        
        if reponse == '1':
            pth = Path('./tirage_equipes/')
            if pth.exists():
                print('')
                print('  ------------------------------------')
                print('  Le dossier "tirage_equipes" existe déjà.')
                print("  S'il contient des fichiers issus d'un tirage précédent, ces derniers seront ÉCRASÉS.")
                print('  ------------------------------------')
                print('')
                reponse = input("Procéder au tirage malgré tout (o/n) ? ")
                while reponse not in ['o','n']:
                    reponse = input('Veuillez répondre "o" ou "n" : ')
                
                if reponse == "o":
                    repartition_equipes(liste_eleves)
                    afficher_menu = False

                    
                    print("Noms des équipes utilisés pour ce tirage :")
                    print(noms_equipes[0:nb_equipes])
                    print('')

                    print("Répartition des équipes effectuée.")
                    print("Vous la trouverez dans le dossier \"tirage_equipes\".")
                    input("Appuyez sur Entrée pour quitter le programme.")
                else: # reponse == "n"
                    print("Répartition des équipes annulées.")
                    input("Appuyez sur Entrée pour mettre fin au programme.")
            else: # le dossier "./tirage_equipes" n'existe pas
                repartition_equipes(liste_eleves)
                afficher_menu = False

                
                print("Noms des équipes utilisés pour ce tirage :")
                print(noms_equipes[0:nb_equipes])
                print('')

                print("Répartition des équipes effectuée.")
                print("Vous la trouverez dans le dossier \"tirage_equipes\".")
                input("Appuyez sur Entrée pour quitter le programme.")


    return None

#Vérification de la présence d'un fichier xlsx à traiter
pth ="./"
liste_fichiers_xlsx = glob(pth+"*.xlsx")

if not(liste_fichiers_xlsx):
    print("Aucune liste d'élèves à traiter (fichier xlsx) trouvée dans le répertoire.")
    print("Veuillez fournir une liste d'élèves avant de lancer ce programme.")
    input("Appuyez sur Entrée pour quitter.")

else: # il y a bien un ou plusieurs fichiers xlsx dans le répertoire racine

    if len(liste_fichiers_xlsx)>1:
        print("Il y a plusieurs fichiers xlsx dans le répertoire :")
        print('')
        numeros_fichiers = [i for i in range(1,len(liste_fichiers_xlsx)+1)]
        for fichier in liste_fichiers_xlsx:
            print(f"    {(liste_fichiers_xlsx.index(fichier))+1} --  {fichier[2:]}")
        print('')
        choix_f_el = input(f"Veuillez indiquer celui qui contient la liste des élèves parmi {numeros_fichiers} : ")
        while int(choix_f_el) not in numeros_fichiers:
            print('')
            choix_f_el = input(f"Veuillez indiquer un choix parmi {numeros_fichiers} : ")
        fichier_eleves = f'{liste_fichiers_xlsx[int(choix_f_el)-1][2:]}'
        print('')
        print(f"  --  Fichier conservé pour la répartition : \"{fichier_eleves}\"")
        print('')

    else:
        print(f"Le fichier \"{liste_fichiers_xlsx[0][2:]}\" a été trouvé dans le répertoire.")
        print("Il sera utilisé comme source de données des élèves pour le tirage.")
        fichier_eleves = f'{liste_fichiers_xlsx[0][2:]}'

    # gestion du fichier contenant les noms des équipes 
    #vérifier la présence du dossier "nom_equipes", créer si inexistant
    if not path_noms_eq.exists():
        path_noms_eq.mkdir()
    if not file_noms_eq.exists():
        print('')
        print('   ----------------------------')
        print("   | Noms des équipes par défaut.")
        print('   | Vous pouvez personnaliser les noms des équipes dans le fichier "noms_equipes.xlsx"')
        print('   | se situant dans le répertoire "/noms_equipes", puis recommencer un tirage, si vous le souhaitez.') 
        print('   ----------------------------')
        print('')
        # créer le fichier des noms d'équipes par défaut

        # créer un data frame pandas à partir de la liste par défaut des noms d'équipes,
        # puis créer le fichier Excel et y insérer le data frame
        df = pd.DataFrame({'Data':DefaultTeamNames})
        writer = pd.ExcelWriter(file_noms_eq)
        df.to_excel(writer, sheet_name='sheet_test', header=False, index=False)
        writer.save()

    # récupérer les noms d'équipes renseignés et les ajouter à la liste noms_equipes[] 
    noms_eq_df = pd.read_excel(file_noms_eq, header=None, index_col=None)
    noms_eq_df = noms_eq_df.values.tolist() # chaque objet récupéré avec tolist() est une liste

    # on recrée donc une liste simple à partir de ces données
    for i in range(0,len(noms_eq_df)):
        noms_equipes.append(noms_eq_df[i][0])
    print(noms_equipes)
    
    programme_principal()