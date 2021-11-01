# HelioSolarTracker
*Helio.py : Calculation of solar ephemeris 
NOTICE :
Before cloning make sure to "pip install" all of :
  pip install sqlite3
  pip install pyqt5
  pip install pyqtgraph

TO DO :
Optimisation of classes and automation of the process of calculation,
python : by working with Functions parameters, to avoid redundancy. 
QtDesigner : make the window fixed (no-geometry changes) 
...
*time.c : make sure you have CodeBlocs installed in your machine, and compile the file so you can use on terminal mode the code.
THANKS!
I.	Logiciel de calcul des éphémérides solaires, et traitement de données.
1.	Introduction 

Afin de traiter les données graphiquement et obtenir les résultats automatiquement, un logiciel a été développé pour l’occasion, il s’agit d’un petit programme qui a été nommé Helio Solar Tracker, il  développé en Python (langage de programmation Fonctionnel/Orienté objet) pour l’implémentation et les calculs astronomiques (même calculs utilisés lors du calcul en langage C au chapitre IV), ensuite une librairie en C++ nommée Qt a été utilisée pour l’interface utilisateur graphique (GUI), ainsi que quelques lignes de codes en CSS (Cascading Style Sheets) ont servi au design du programme.

2.	. Présentation du programme
 
Le programme se présente sous forme d’une interface interactive, où l'utilisateur peut calculer les coordonnées solaires (Figure IV.1), selon la date, l’heure, les coordonnées GPS et le fuseau horaire du lieu (UTC), et le jour julien.
![image](https://user-images.githubusercontent.com/42687107/139695885-fe2e3dba-69ca-4f27-bdc0-5671554d6261.png)
Figure IV. 1 Helio Solar Tracker, Interface utilisateur
Le programme se décompose en quatre principales parties (Figure IV.2) différente parties du programme, Helio solar tracker:
●	La partie indicative (zone 1), qui comme son nom l'indique, montre la date et/ou l’heure pour laquelle les calculs se font.
●	La partie initialisation et calcul (zone 2); elle représente la partie dans laquelle sont sélectionnées les données via lesquelles on procède au calcul (Coordonnées GPS, UTC, Date et heure), et y sont contenues aussi les boutons permettant de procéder au calcul (Début. Et Calcul.).
●	La partie Affichage en temps réel (zone 3), il s’agit de la partie inférieure du code ou sont affichées les données astronomiques calculées au moment du clic sur l’un des boutons de calcul.
●	Et enfin, la zone de sélection et traitement des résultats (zone 4),  elle concerne l’affichage des données en tableaux après calcul, ainsi que l’affichage des données sous forme de graphes et courbes, avec la possibilité d’enregistrer les données sous différent formats (PNG, Jpeg, SVG…etc).

 
Figure IV. 2 Différentes parties du programme Helio Solar Tracker


3.	. Initialisation des données de calcul

La phase d’initialisation des données concerne en premier lieu, les coordonnées terrestres (Latitude λ et longitude φ) ici initier à la valeur des coordonnées GPS de la ville d’Alger, ensuite on sélectionne le fuseau horaire UTC (la correction étant noté C dans le programme), ensuite il s’agira de saisir la date et heure de calcul voulus. Afin de procéder au calcul il suffit de cliquer sur le bouton Calcul. Dans la zone 2, ou alors en cliquant sur Début. qui permettra de calculer en temps réel et d’afficher les résultats automatiquement selon l’heure exacte du clic et la date actuelle.
Une fois l’un des boutons cliqué la Zone 1  affichera la date et l’heure de calcul, la Zone 3 affichera les résultats calculés au moment du clic (Figure IV.3).

 
Figure IV. 3 Calcul/Affichage des ephémérides solaires pour l'heure et la date sélectionnées
En cliquant sur Calcul. après avoir sélectionné une heure et une date précise, le programme affiche les résultat instantanément, le temps solaire vrai et moyen (TSM et TSV) ainsi que l’équation du temps, les coordonnées horizontales et Equatoriales ainsi que l’heure du lever/coucher du soleil pour la date sélectionnée et l’heure d’ensoleillement.



4.	. Interprétation des données et résultats de calculs

Une fois que nous avons procédé au calcul, on récupère les résultats numériques un premier temps en cliquant dans la Zone 4 sur Affichage des données (Figure IV.4) et on interprète graphiquement les résultats en cliquant sur Données graphiques (Figure IV.5).
 
Figure IV. 4 mosaïque des différents résultats numériques après calcul


 
Figure IV. 5 Mosaïque. Affichage des résultats de calcul sous forme de Courbes
Pour chaque graph, en faisant un clic droit sur l’image du graph il est possible de l’exporter sous plusieurs formats afin de les utiliser comme support et/ou illustrations, comme dans la représentation des résultats au chapitres III.
5.	Conclusion

Le logiciel est conçu pour être open source et offrir une aide au calcul ou autre projets relatifs au suivi du soleil, comme support ou référence, son code source sera intégré à une plateforme de partage de logiciel et de codes sources et autres types de projets (https://github.com/indigene-way/HelioSolarTracker_usthb_GM_TE). 

