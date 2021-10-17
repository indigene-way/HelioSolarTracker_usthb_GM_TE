#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include <string.h>
#include <locale.h>

#define  EQTIME1        229.18
#define  EQTIME2        0.000075
#define  EQTIME3        0.001868
#define  EQTIME4        0.032077
#define  EQTIME5        0.014615
#define  EQTIME6        0.040849


#define  DECL1          0.006918
#define  DECL2          0.399912
#define  DECL3          0.070257
#define  DECL4          0.006758
#define  DECL5          0.000907
#define  DECL6          0.002697
#define  DECL7          0.00148

#define  PI             3.14159265
#define rd              0.017453292
#define DEG             57.29577958


// ************************************Variables horaires :
int h, min, s, day, mois, an, JDay;
time_t now;
double TL,TU,TSM,TSV,hd,mind,sd,C;
//************************************COORDONNEE TERRESTRES tiaret(35.3673553 1.3220322):
double latitude, longitude;
//************************************COORDONNEE SOLAIRE
    //COORDONNEES EQUATORIALES
double Decli, EqTime, AngH;
    //COORDONNEES HORIZONTALE
double Hauteur, Azimith;
    //DUREE/LEVER/COUCHER SOLEIL
double DureeS, LeverS, CoucherS;

//INITITALITAION DES TABLEAU DE RECUP DE DONNEES
double TabTL[15],TabTU[15],TabTSM[15],TabEqT[15],TabTSV[15],TabAngH[15],TabDecli[15],TabHaut[15],TabAzim[15];

int main()
{
setlocale(LC_CTYPE,"");

printf("\tINITIALISATION DES COORDONEES GEOGRAPHIQUES \n\n");
		printf("Saisir la latitude du lieu (Alger 36.752887°) : ");
		scanf("%lf", &latitude);
		printf("Saisir la longitude du lieu (Alger 3.042048°) : ");
		scanf("%lf", &longitude);
		printf("Saisir le fuseau horaire UTC + (1 pour DZ): ");
		scanf("%lf", &C);

//PHASE FONCTIONS
void Timer()
{
  // Renvoie l'heure actuelle
    time(&now);
  // Convertir au format heure locale
    //printf("\n\n\t\tAujourd'hui : %s", ctime(&now));
    struct tm *local = localtime(&now);
        h = local->tm_hour;
        min = local->tm_min;
        s = local->tm_sec;
        day = local->tm_mday;
        mois = local->tm_mon + 1;
        an = local->tm_year + 1900;
}

//************************************CONVERSION HORAIRES
double Convert_Time(double heure)
{
    double h,min;
    h = floor(heure);
    min = 60*(heure - h);

    return(heure);
}

double Convert_Degre(double degre)
{
    double deg,min,tester;
    deg = floor(degre);
    if (deg > 0){
        deg = deg - 1;
        tester = (degre - deg);
        min = (tester*60);
    }
    else{
        deg = deg + 1;
        tester = (degre - deg);
        min = -(tester*60);
    }
}

//************************************CALCUL DU JOUR JULIAN
int Julian_day(int annee, int mois, int jour)
{
    int m;
	int month[13] = {0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
	JDay = 0;
	if(annee%4==0) month[1] = 29;
	for(m = 0; m<= mois-1; m++) JDay += month[m];
	JDay = JDay + jour;
	return(JDay);
}
//************************************CALCUL DU TEMPS LEGALE
  double Temps_Legal(double h, double min, double s)
  {
    hd = h;
    mind = min;
    sd = s;
    TL = h +(mind / 60) + (sd / 3600);
    return(TL);
  }
//************************************CALCUL DU TEMPS SOLAIRE MOYEN
double Temps_Solaire_Moyen(double TU, double lon)
{
	TSM = TU + (lon/15.);
	return(TSM);
}
//************************************CALCUL DU TEMPS UNIVERSEL
double Temps_Universel(double TL, double lonR, double C)
{
	TU = TL - lonR/15. - C ;
	return(TU);
}

//************************************CALCUL EQUATION DU TEMPS
double EqTemps( int JDay, int DayYear)
{
	double Gamma;

	Gamma =  2. * PI * (JDay + 1)/DayYear;


	EqTime = EQTIME1 *(EQTIME2 + EQTIME3 * cos(Gamma) - EQTIME4*sin(Gamma)-
		  EQTIME5*cos(2. * Gamma) - EQTIME6 * sin(2. * Gamma)) ;

	return(EqTime);
}
//************************************CALCUL DU TEMPS SOLAIRE VRAI
double TempsSolairVrai(double UTime, double TL, double longitude, double EqTime)
{
    double Dt;
    //Dt = 9.87 * sin((360/365)*(JDay-81)) - 7.35 * cos((360/365)*(JDay - 81)) - 1.5 * sin((360/365)* (JDay-81));
    TSV = TL - ((TL - UTime) - (longitude/15))+ (EqTemps(JDay, 365)/60);
    return(TSV);
}
//************************************COORDONNEES EQUATORIALES ******
//************************************CALCUL DE LA DECLINAISON SOLAIRE
double SolairDecli(int JDay, int DayYear)
{
	double  Gamma;

	Gamma =  2 * PI * (JDay - 1)/DayYear;

	Decli 	= (DEG)*(DECL1-DECL2*cos(Gamma)+DECL3*sin(Gamma)-
		  DECL4*cos(2. * Gamma)+DECL5 * sin(2. * Gamma)-
		  DECL6 * cos(3. * Gamma) + DECL7 * sin(3. * Gamma)) ;

	return(Decli);
}
//************************************CALCUL DE L'ANGLE HORAIRE
double Angle_Horaire()
{
	AngH = 15 * (12 -TSV);
	return(AngH);
}
//************************************COORDONNEES HORIZONTALES ******

//************************************HAUTEUR DU SOLEIL
double Hauteur_Soleil(double lat,double AngH, double decli)
{
    double sin1, sin2, sinH;
    //sin(h) = sin(lat)*sin(Decli) + cos(lat)*cos(Decli)*cos(H)
    sinH = sin(lat *rd) * sin(decli * rd) + cos(lat *rd)*cos(decli * rd)*cos(AngH * rd);
    Hauteur = asin(sinH);
    Hauteur = Hauteur * (DEG);
    return(Hauteur);
}

//************************************AZIMUTH DU SOLEIL
double Azimuth_Soleil(double decli, double hauteur, double angH)
{
    double tanA, y, sinA;
    sinA = (cos(decli  *(rd))*sin(angH  *(rd)))/cos(hauteur  *(rd));
    Azimith = asin(sinA);
    Azimith = Azimith * DEG;

    return(Azimith);
}

//************************************DUREE JOUR/LEVER/COUCHER SOLEIL :
//LEVER DU SOLEIL
double Lever_Soleil(double lat, double decli)
{
    double Lsrad, Th,Tmin,Ts;
    Lsrad = acos(-tan(decli * (rd))*tan(lat * (rd)));
    LeverS = 12 - ((Lsrad * (DEG))/15)+ 1;

	return(LeverS);

}
//COUCHER DU SOLEIL
double Coucher_Soleil(double lat, double decli)
{
    double Lsrad, Th,Tmin,Ts;
    Lsrad = acos(-tan(decli * (rd))*tan(lat * (rd)));
    CoucherS = 12 + ((Lsrad * (DEG))/15) + 1;

	return(CoucherS);

}
//DUREE JOUR
double Duree_Soleil(double Tl, double Tc)
{
    DureeS = Tc - Tl;
	return(DureeS);
}

//************************************RECUPERATION DES DONNEES ******

//FONCTIONS DE CALCUL JOURNALIER
void PositionActuel(){
//DONNEES HORAIRES :
    Timer();
    Julian_day(an, mois, day);//JULIAN DAY
    Temps_Legal(h, min, s);//TEMPS LEGALE
    Convert_Time(TL);

    Temps_Universel(TL, longitude, C);//TEMPS LEGAL
    Convert_Time(TU);

    Temps_Solaire_Moyen(TU, longitude);//TEMPS SOLAIRE MOYEN
    Convert_Time(TSM);

//EqTemps(JDay, 365);//EQUATION DU TEMPS
    TempsSolairVrai(TU, TL, longitude, EqTime);//TEMPS SOLAIRE VRAI II
    Convert_Time(TSV);

//COORDONNEES EQUATORIALES :
    SolairDecli(JDay, 365);//DECLINAISON SOLAIRE
    Angle_Horaire();//ANGLE HORAIRE

//COORDONNEES HORIZONTALES  (ORIENTATION SUD):
    Hauteur_Soleil(latitude, AngH, Decli);//HAUTEUR DU SOLEIL
    Azimuth_Soleil(Decli, Hauteur, AngH);//AZIMUTH DU SOLEIL

    Lever_Soleil(latitude, Decli);//LEVER DU SOLEIL
    Coucher_Soleil(latitude, Decli);//COUCHER DU SOLEIL
    Duree_Soleil(LeverS, CoucherS);//COUCHER DU SOLEIL

    //DUREE D'NSOLATION
    if (mois < 10){
    printf("\n\n\tDONNEES D'ENSOLEILLEMENT %d-0%d-%d\n\n",day,mois,an);}
    else{
    printf("\n\n\tDONNEES D'ENSOLEILLEMENT %d-%d-%d\n\n",day,mois,an);}

    printf("Lever   Coucher\t   Ensoleillement\n");

    //AFFICHAGE RESULTAT

        printf("%.4lfh %.4lfh   %.4lfh\n", LeverS, CoucherS, DureeS);

    if (mois < 10){
    printf("\n\tDONNEES ACTUELLES %d-0%d-%d heure : %d:%d:%d\n\n",day,mois,an,h,min,s);}
    else{
    printf("\n\tDONNEES ACTUELLES %d-%d-%d heure : %d:%d:%d\n\n",day,mois,an,h,min,s);}

    printf("TL\t TU\t  TSM\t    EQTime    TSV \n");
    printf("%.4lf  %.4lf  %.4lf   %.4lf   %.4lf \n\n", TL, TU, TSM, EqTime, TSV);

    printf("TL\tDeclinaison Angle horraire Hauteur  Azimut \n");
    printf("%.4lf\t%.4lf     %.4lf       %.4lf  %.4lf\n\n", TL, Decli, AngH, Hauteur, Azimith);
}

void CoordonneesJour(){

    //INITIALISATION DES DONNEES
    int i=0;
    TL = LeverS;
    if (mois < 10){
    printf("\n\tDONNEES QUOTIDIENNES %d-0%d-%d\n\n",day,mois,an);}
    else{
    printf("\n\tDONNEES QUOTIDIENNES %d-%d-%d\n\n",day,mois,an);}
    printf("TL\t  TU\t  TSM\t   EQTime   TSV    Declinaison  Angle horraire  Hauteur   Azimut \n\n");

    while(TL <= CoucherS ){

    //DONNEES HORAIRES :
        Temps_Universel(TL, longitude, C);//TEMPS LEGAL
        Temps_Solaire_Moyen(TU, longitude);//TEMPS SOLAIRE MOYEN

    //EqTemps(JDay, 365);//EQUATION DU TEMPS
        TempsSolairVrai(TU, TL, longitude, EqTime);//TEMPS SOLAIRE VRAI

    //COORDONNEES EQUATORIALES :
        SolairDecli(JDay, 365);//DECLINAISON SOLAIRE
        Angle_Horaire();//ANGLE HORAIRE

    //COORDONNEES HORIZONTALES  (ORIENTATION SUD):
        Hauteur_Soleil(latitude, AngH, Decli);//HAUTEUR DU SOLEIL
        Azimuth_Soleil(Decli, Hauteur, AngH);//AZIMUTH DU SOLEIL


    //AFFICHAGE RESULTAT

        printf("%.4lf  %.4lf  %.4lf   %.4lf   %.4lf   %.4lf     %.4lf       %.4lf   %.4lf\n", TL, TU, TSM, EqTime, TSV, Decli, AngH, Hauteur, Azimith);

    //REMPLISSAGE DES TABLEAUX

     TabTL[i] = TL;
     TabTU[i] = TU;
     TabTSM[i] = TSM;
     TabEqT[i] = EqTime;
     TabTSV[i] = TSV;
     TabAngH[i] = AngH;
     TabDecli[i] = Decli;
     TabHaut[i] = Hauteur;
     TabAzim[i] = Azimith;

    //INCREMENTATION
    TL+=1;
    i+=1;
    }
}

void CoordonneesEquat(){

    //INITIALISATION DES DONNEES
    int i=0;
    TL = LeverS;
    if (mois < 10){
    printf("\n\n\tDONNEES EQUATORIALES QUOTIDIENNES %d-0%d-%d\n\n",day,mois,an);}
    else{
    printf("\n\tDONNEES EQUATORIALES QUOTIDIENNES %d-%d-%d\n\n",day,mois,an);}
    printf("TL      Declinaison Angle horraire\n\n");

    while(TL <= CoucherS ){

    //DONNEES HORAIRES :
        Temps_Universel(TL, longitude, C);//TEMPS LEGAL
        Temps_Solaire_Moyen(TU, longitude);//TEMPS SOLAIRE MOYEN

    //EqTemps(JDay, 365);//EQUATION DU TEMPS
        TempsSolairVrai(TU, TL, longitude, EqTime);//TEMPS SOLAIRE VRAI

    //COORDONNEES EQUATORIALES :
        SolairDecli(JDay, 365);//DECLINAISON SOLAIRE
        Angle_Horaire();//ANGLE HORAIRE

    //AFFICHAGE RESULTAT

        printf("%.4lf  %.4lf     %.4lf\n", TL, Decli, AngH);
    //INCREMENTATION
    TL+=1;
    i+=1;
    }
}

void CoordonneesHorz(){

    //INITIALISATION DES DONNEES
    int i=0;
    TL = LeverS;
    if (mois < 10){
    printf("\n\n\tDONNEES HORIZONTALES QUOTIDIENNES %d-0%d-%d\n\n",day,mois,an);}
    else{
    printf("\n\tDONNEES HORIZONTALES QUOTIDIENNES %d-%d-%d\n\n",day,mois,an);}
    printf("TL\tHauteur   Azimut\n\n");

    while(TL <= CoucherS ){

    //DONNEES HORAIRES :
        Temps_Universel(TL, longitude, C);//TEMPS LEGAL
        Temps_Solaire_Moyen(TU, longitude);//TEMPS SOLAIRE MOYEN

    //EqTemps(JDay, 365);//EQUATION DU TEMPS
        TempsSolairVrai(TU, TL, longitude, EqTime);//TEMPS SOLAIRE VRAI

    //COORDONNEES EQUATORIALES :
        SolairDecli(JDay, 365);//DECLINAISON SOLAIRE
        Angle_Horaire();//ANGLE HORAIRE

    //COORDONNEES HORIZONTALES  (ORIENTATION SUD):
        Hauteur_Soleil(latitude, AngH, Decli);//HAUTEUR DU SOLEIL
        Azimuth_Soleil(Decli, Hauteur, AngH);//AZIMUTH DU SOLEIL

    //AFFICHAGE RESULTAT

        //printf("%.4lf  %.4lf   %.4lf\n", TL, Hauteur, Azimith);
        printf("%.4lf  %.4lf   %.4lf\n", TabTL[i], TabHaut[i], TabAzim[i]);
    //INCREMENTATION
    TL+=1;
    i+=1;
    }
}

//RECUPERATION DE DONNEES
PositionActuel();
CoordonneesJour();
CoordonneesEquat();
CoordonneesHorz();

}

