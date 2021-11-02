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

![image](https://user-images.githubusercontent.com/42687107/139696199-360f292a-ecba-4c4f-bc45-d5c297cbb523.png) 
 
Figure IV. 2 Différentes parties du programme Helio Solar Tracker


3.	. Initialisation des données de calcul

La phase d’initialisation des données concerne en premier lieu, les coordonnées terrestres (Latitude λ et longitude φ) ici initier à la valeur des coordonnées GPS de la ville d’Alger, ensuite on sélectionne le fuseau horaire UTC (la correction étant noté C dans le programme), ensuite il s’agira de saisir la date et heure de calcul voulus. Afin de procéder au calcul il suffit de cliquer sur le bouton Calcul. Dans la zone 2, ou alors en cliquant sur Début. qui permettra de calculer en temps réel et d’afficher les résultats automatiquement selon l’heure exacte du clic et la date actuelle.
Une fois l’un des boutons cliqué la Zone 1  affichera la date et l’heure de calcul, la Zone 3 affichera les résultats calculés au moment du clic (Figure IV.3).

![image](https://user-images.githubusercontent.com/42687107/139696269-96709a5d-d2f2-4f3b-9902-421505c21dc7.png)
 
Figure IV. 3 Calcul/Affichage des ephémérides solaires pour l'heure et la date sélectionnées
En cliquant sur Calcul. après avoir sélectionné une heure et une date précise, le programme affiche les résultat instantanément, le temps solaire vrai et moyen (TSM et TSV) ainsi que l’équation du temps, les coordonnées horizontales et Equatoriales ainsi que l’heure du lever/coucher du soleil pour la date sélectionnée et l’heure d’ensoleillement.



4.	. Interprétation des données et résultats de calculs

Une fois que nous avons procédé au calcul, on récupère les résultats numériques un premier temps en cliquant dans la Zone 4 sur Affichage des données (Figure IV.4) et on interprète graphiquement les résultats en cliquant sur Données graphiques (Figure IV.5).

![image](https://user-images.githubusercontent.com/42687107/139696358-3c3331d0-09b7-4726-bfbf-bff50fb41b1d.png)

Figure IV. 4 mosaïque des différents résultats numériques après calcul

![image](https://user-images.githubusercontent.com/42687107/139696423-543ad6eb-7347-4e8a-85f3-92325aa26648.png)
 
Figure IV. 5 Mosaïque. Affichage des résultats de calcul sous forme de Courbes
Pour chaque graph, en faisant un clic droit sur l’image du graph il est possible de l’exporter sous plusieurs formats afin de les utiliser comme support et/ou illustrations, comme dans la représentation des résultats au chapitres III.
5.	Conclusion

Le logiciel est conçu pour être open source et offrir une aide au calcul ou autre projets relatifs au suivi du soleil, comme support ou référence, son code source sera intégré à une plateforme de partage de logiciel et de codes sources et autres types de projets (https://github.com/indigene-way/HelioSolarTracker_usthb_GM_TE). 

#C CODE RESULTS
4.	Résultats obtenus 
On compilant le code dans un IDE (CodeBlocks),  on obtient un terminal (Figure III.1) où seront affichés les résultats de calculs ainsi que les demandes de saisi :

![image](https://user-images.githubusercontent.com/42687107/139963423-4eeebbfe-16cd-4b28-9ceb-dd18928fb699.png)
 
Figure III. 1 Saisi des coordonnée GPS et fuseau horaire de la zone
Une fois les coordonnées GPS saisi le code procède aux calculs et retourne les valeurs voulues (Figure III.2). Dans un premier temps on a les données de lever/coucher du soleil ainsi que la durée d’ensoleillement (Tableau III.1 et III.2), puis les données de position du soleil et horaire en temps réel. Dans la deuxième partie des résultats s’affiche un tableau qui répertorie les éphémérides de la journée du lever au coucher du soleil (Tableau III.3).

![image](https://user-images.githubusercontent.com/42687107/139963471-c4eada83-259a-4992-bf65-2e4194d3c5c6.png)

Figure III. 2 Résultats de calculs en fonction du temps légal actuel et de la durée d’ensoleillement 

On obtient après mise en tableau des résultats :
Pour les données en temps réel pour le 18-06-2021 à 18:36:18:

![image](https://user-images.githubusercontent.com/42687107/139964322-0d31a308-73f8-4ab8-8841-74d5f2aadce4.png)

Tableau III. 1 Données d'ensoleillement pour la journée sélectionnée

![image](https://user-images.githubusercontent.com/42687107/139964360-d660e774-6d56-48c6-bdf4-677be2e2cb01.png)

Tableau III. 2 Données horaires et éphémérides en temps réel
Pour les données quotidiennes :

![image](https://user-images.githubusercontent.com/42687107/139964424-cfacedeb-91da-4b35-8aab-8187f6fc8174.png)

La seconde partie des résultats affichés, répertorié dans deux tableaux séparés tous des coordonnées équatoriales de la journée et les coordonnées horizontales (du lever au coucher du soleil) (Figure III.3 et Tableau III.4) :

![image](https://user-images.githubusercontent.com/42687107/139964444-2826b7b4-0d48-4b46-8202-28cd6c1cf110.png)

Tableau III. 4 Coordonnées équatoriales et horizontales de la journée sélectionnée

![image](https://user-images.githubusercontent.com/42687107/139963572-f01f94a9-5a9a-410f-8973-28393f2e3190.png)

Figure III. 3 Récupération des résultats de calcul des coordonnées équatoriales et horizontales
Afin de traiter les données graphiquement et obtenir les résultats automatiquement, un logiciel a été développé pour l’occasion (Chapitre V).
5.	Représentation graphique des résultats

●	Données équatoriales

![image](https://user-images.githubusercontent.com/42687107/139963596-756b63ba-648d-41d3-91cf-088943f75c2d.png)
 
Courbe III. 1 Coordonnées Graphique des équations équatoriales

![image](https://user-images.githubusercontent.com/42687107/139963611-354cc6b9-ee28-4cee-a7fa-7ef13386bb50.png)

Courbe III. 2 Coordonnées Graphique de l’angle horaire

![image](https://user-images.githubusercontent.com/42687107/139963637-05269df5-e729-452e-b870-6582dc0db8af.png) 

Courbe III. 3 Coordonnées Graphique de la déclinaison solaire
●	Données Horizontales

 ![image](https://user-images.githubusercontent.com/42687107/139963660-ecdd688d-4a17-454b-a453-27d99d88fe67.png)

Courbe III. 4 Coordonnées Graphique des équations horizontales

![image](https://user-images.githubusercontent.com/42687107/139963871-1127dcbf-7c0b-4bfd-94b2-632c2ca226ab.png)
 
Courbe III. 5 Coordonnées Graphique Azimut

![image](https://user-images.githubusercontent.com/42687107/139963881-b699e950-318e-49e2-8668-32405b7e048c.png)
 
Courbe III. 6 Coordonnées Graphique Hauteur

●	Données horaire

![image](https://user-images.githubusercontent.com/42687107/139963906-88ec425a-e26c-483a-8443-c94e7851fca9.png)

Courbe III. 7 Horaire et temps solaire vrai

.	Conclusion

Le choix du langage C a été fait en fonction de la proximité du langage avec le langage de programmation du module Arduino Uno (Chapitre VI), afin de directement pouvoir utiliser les résultats obtenus dans la maquette électronique, mais aussi pour des questions de fiabilité des résultats, sachant que le langage C représente l’un des langage bas niveau les plus fiables.
