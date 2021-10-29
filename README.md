# EquipesEleves
Script python permettant la génération aléatoire et paritaire d'équipes, notamment entre plusieurs classes.

Le fonctionnement du script en soi consiste à être le plus simple possible : il suffit de placer un fichier csv (format exportable depuis n'importe quel logiciel de tableur type Excel/LibreOffice Calc) dans le même répertoire que le fichier du script, et de lancer ce dernier.

Les renseignements fournis par le fichier csv doivent être organisés d'une certaine manière, comme dans le fichier "liste_eleves.csv" (version Windows ANSI ou UTF-8) disponible dans le dépot.

**Il suffit de respecter la nomenclature suivante :
  -> première ligne :
  "nom" ; "prenom" ; "sexe" ; "prof"**
  
Puis de renseigner les informations des élèves. 
Ce sont généralement des données aisément disponibles dans la plupart des écoles.
Notez bien que renseigner une classe (type "CE1" ou "6èmeB") en lieu et place d'un nom de professeur est tout à fait envisageable.

Pour le reste, il suffit de lancer le script et de se laisser guider pour procéder au tirage aléatoire des équipes.

Le résultat du tirage se trouvera dans un dossier "tirage_equipes" situé au même endroit que le fichier du script. Il contient le résultat du tirage sous plusieurs formes différentes : un tirage global contenant toutes les informations (que vous pourrez parcourir à l'aide d'un tableur en vous servant de la première ligne comme filtre, par exemple), mais aussi les tirages par classe/prof ou par équipes, ce qui peut faciliter l'impression des résultats.

--------------------

**Optionnel : choisir soi-même le nom des équipes.**

Par défaut, le script génère des noms d'équipes basées sur des couleurs (ce qui permet d'attribuer des chasubles correspondantes aux élèves), mais vous pouvez très bien imaginer autre chose (dans le cadre d'un tournoi par exemple).

Une fois le premier tirage effectué, un dossier "noms_equipes" apparaîtra dans le répertoire du script, qui contient un fichier csv contenant les noms des équipes.
Vous pouvez changer l'ordre d'attribution des couleurs (par exemple, si vous générez 4 équipes, seules les 4 premières couleurs du fichier seront attribuées, ce qui ne correspond peut-être pas à votre matériel), ou bien changer complètement les noms des équipes pour les tirages ultérieurs.
