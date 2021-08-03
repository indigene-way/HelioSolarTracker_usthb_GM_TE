#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys, os
import re 
import uuid
import time
import math
import datetime

import sqlite3
from PyQt5.QtSql import *

from PyQt5 import QtCore, QtGui, uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from pyqtgraph import PlotWidget, plot, mkPen
import pyqtgraph as pg

# ============= EPHEMERIDES CALSS
class EphCalcul():
	def __init__(self):
		#DECLARATION DE VARIABLES ET CONSTANTES DE CALCUL
		#EQUATION DU TEMPS
		self.EQTIME1 = 229.18
		self.EQTIME2 = 0.000075
		self.EQTIME3 = 0.001868
		self.EQTIME4 = 0.032077
		self.EQTIME5 = 0.014615
		self.EQTIME6 = 0.040849

		#DECLINAISON
		self.DECL1 = 0.006918
		self.DECL2 = 0.399912
		self.DECL3 = 0.070257
		self.DECL4 = 0.006758
		self.DECL5 = 0.000907
		self.DECL6 = 0.002697
		self.DECL7 = 0.00148

		#TRIGONOMETRIQUES
		self.PI = 3.14159265
		self.rd = 0.017453292
		self.DEG = 57.29577958
		
		#TIME ZONE	
		self.localDateTime = time.strftime("%d-%m-%Y      %H:%M:%S")
		self.localDate = time.strftime("%d/%m/%Y")
		self.Date = time.strftime("%Y-%m-%d")
		self.now = time.strftime("%H:%M:%S")
		
		self.year = int(time.strftime("%Y"))
		self.month = int(time.strftime("%m"))
		self.day = int(time.strftime("%d"))
		
		self.hour = int(time.strftime("%H"))
		self.min = int(time.strftime("%M"))
		self.sec = int(time.strftime("%S"))
		
		self.TL = self.hour +(self.min / 60) + (self.sec / 3600);
		self.dayYear = 365
	
	#==========INIT CALCUL FUNCTIONS
	#JULIAN DAY
	def JulianDay(self,month, day):
		self.monthDays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
		self.jDay = 0
		
		if self.year % 4 == 0 :
			self.monthDays[1] = 29
			
		m = 0
		while m < month - 1 :
			self.jDay += self.monthDays[m]
			m+=1
		
		self.jDay = self.jDay + day;
	#TEMPS UNIVERSEL
	def TempsUniversel(self, lon, C):
		TU = self.TL - lon/15. - C 
		self.TU = TU
		
	#TEMPS SOLAIRE MOYEN
	def TempsSM(self, lon):
		self.TSM = self.TU + (lon/15.)
		
	#EQUATION TEMPS
	def EquaTime(self):
		Gamma =  2. * self.PI * (self.jDay + 1)/self.dayYear

		self.EqTime = self.EQTIME1 *(self.EQTIME2 + self.EQTIME3 * math.cos(Gamma) - self.EQTIME4*math.sin(Gamma)-\
		self.EQTIME5*math.cos(2. * Gamma) - self.EQTIME6 * math.sin(2. * Gamma))
	
	#TEMPS SOLAIRE VRAI
	def TempsSV(self, lon):
		self.TSV = self.TL - ((self.TL - self.TU) - (lon/15))+ (self.EqTime/60)
		
# ************************************COORDONNEES EQUATORIALES ******
# ************************************CALCUL DE LA DECLINAISON SOLAIRE

	def Declinaison(self):
		Gamma =  2 * self.PI * (self.jDay - 1)/self.dayYear

		self.Decli 	= (self.DEG)*(self.DECL1-self.DECL2*math.cos(Gamma)+self.DECL3*math.sin(Gamma)-\
		self.DECL4*math.cos(2. * Gamma)+self.DECL5 * math.sin(2. * Gamma)-\
		self.DECL6 * math.cos(3. * Gamma) + self.DECL7 * math.sin(3. * Gamma))
	#ANGLE HORAIRE
	def AngleHoraire(self):
		self.AngH = 15 * (12 - self.TSV)
		
# ************************************COORDONNEES HORIZONTALES ******
	#HAUTEUR DU SOLEIL
	def Hauteur(self, lat):
		sinH = math.sin(lat *self.rd) * math.sin(self.Decli * self.rd) + math.cos(lat * self.rd)*math.cos(self.Decli * self.rd)*math.cos(self.AngH * self.rd)
		self.Haut = math.asin(sinH)
		self.Haut = self.Haut * (self.DEG)
		
	#AZIMUT
	def Azimut(self):		
		sinA = (math.cos(self.Decli  *(self.rd))*math.sin(self.AngH *(self.rd)))/math.cos(self.Haut  *(self.rd))
		self.Azim = math.asin(sinA)
		self.Azim = self.Azim * self.DEG

# ************************************DUREE JOUR/LEVER/COUCHER SOLEIL ******
	def Lever_Soleil(self, lat):
		Lsrad = math.acos(-math.tan(self.Decli * (self.rd))*math.tan(lat * (self.rd)))
		self.leverS = 12 - ((Lsrad * (self.DEG))/15)+ 1
		
	def Coucher_Soleil(self, lat):
		Lsrad = math.acos(-math.tan(self.Decli * (self.rd))*math.tan(lat * (self.rd)));
		self.coucherS = 12 + ((Lsrad * (self.DEG))/15) + 1;
		
	def Duree_Soleil(self):
		self.dureeS = self.coucherS - self.leverS
		
# =============UI SOLAR DATA CLASS DIALOG		
qtHelio= "DESIGN/Helios.ui"
Ui_Helios, QtBaseClass = uic.loadUiType(qtHelio)	
class Helios(QDialog, Ui_Helios):#EDIT : MODIF Product Name,Price DIALOG
	
	def __init__(self):
		QDialog.__init__(self)
		Ui_Helios.__init__(self)
		self.setupUi(self)
		self.show()
		
		self.setWindowTitle("Helio Solar Tracker.")
		
		#TIME ZONE	
		self.localDateTime = time.strftime("%d-%m-%Y      %H:%M:%S")
		self.localDate = time.strftime("%d/%m/%Y")
		self.Date = time.strftime("%Y-%m-%d")
		self.now = time.strftime("%H:%M:%S")
		
		self.year = int(time.strftime("%Y"))
		self.month = int(time.strftime("%m"))
		self.day = int(time.strftime("%d"))
		
		self.hour = int(time.strftime("%H"))
		self.min = int(time.strftime("%M"))
		self.sec = int(time.strftime("%S"))
		
		#INSTANCE DE CLASS
		self.Calcul = EphCalcul()
		
		#SIGNALS
		self.buttonsSignal()
		
		#function
		self.TableWidgetInit()#PRINT AND CONVERT TIME AND DATES,and DATA
		self.ActualCalcul()#PRINT AND CONVERT TIME AND DATES,and DATA
		self.DailyCalcul()
		
		#VARIABLES
		self.nowTime = 0
		
	def TableWidgetInit(self):	#INIT TABLE WIDGET COLUMN, ALIGNEMENT
		self.tableWidget.clear()
		self.tableWidget.clearContents()
		self.tableWidget.setRowCount(0)
		
		self.tableWidget.setColumnCount(8)
		self.tableWidget.setColumnWidth(0, 71)
		self.tableWidget.setColumnWidth(1, 71)
		self.tableWidget.setColumnWidth(2, 71)
		self.tableWidget.setColumnWidth(3, 71)
		self.tableWidget.setColumnWidth(4, 71)
		self.tableWidget.setColumnWidth(5, 71)
		self.tableWidget.setColumnWidth(6, 71)
		
		self.tableWidget.setHorizontalHeaderLabels(['TL', 'TU', 'TSV','EqT', 'δ°', 'ω°','H°','ψ°'])
		self.header = self.tableWidget.horizontalHeader()
		self.header.setDefaultAlignment(Qt.AlignHCenter)
		
	def buttonsSignal(self):
		self.timeInit.clicked.connect(self.ActualCalcul)
		self.timeCalcul.clicked.connect(self.DailyCalcul)
		
		self.clear.clicked.connect(self.Clear)
		
		self.gpsLong.valueChanged.connect(self.ActualCalcul)
		self.gpsLat.valueChanged.connect(self.ActualCalcul)
		
		
		self.dataHSun.clicked.connect(self.DailyHSun)
		self.dataEqHo.clicked.connect(self.DailyEqHo)
		self.dataEq.clicked.connect(self.DailyEq)
		self.dataHo.clicked.connect(self.DailyHo)
		self.dataNow.clicked.connect(self.DailyCalcul)
		self.clearTab.clicked.connect(self.TableWidgetInit)
		
		#GRAPHICAL BUTTONS
		self.graphEq.clicked.connect(self.GraphSlot)
		self.graphDecli.clicked.connect(self.GraphSlot)
		self.graphAngH.clicked.connect(self.GraphSlot)
		
		self.graphH.clicked.connect(self.GraphSlot)
		self.graphA.clicked.connect(self.GraphSlot)
		self.graphHo.clicked.connect(self.GraphSlot)
		
		self.graphSun.clicked.connect(self.GraphSlot)
		
		# self.clearDock.clicked.connect(self.GraphSlot)
					
	def ConvertDegre(self,degre):
		deg = math.floor(degre)
		if deg > 0 :
			deg = deg - 1
			tester = (degre - deg)
			min = (tester*60)
			if min < 10 :
				min = f'{min:.2f}'[:-1]
				degre = str(deg)+"°"+str(min)
				return degre

			else :
				min = f'{min:.2f}'[:-1]
				degre = str(deg)+"°"+str(min)
				return degre
		
		else :
			deg = deg + 1
			tester = (degre - deg)
			min = -(tester*60)
			if min < 10 :
				min = f'{min:.2f}'[:-1]
				degre = str(deg)+"°"+str(min)
				return degre

			else :
				min = f'{min:.2f}'[:-1]
				degre = str(deg)+"°"+str(min)
				return degre
			
	def ConvertTime(self,heure):
		h = math.floor(heure)
		m = 60*(heure - h)
		if m < 10 and h < 10 :
			heure = "0"+str(h)+" : 0"+str(int(m))
		elif m > 10 and h < 10 :
			heure = "0"+str(h)+" : "+str(int(m))
		elif m < 10 and h > 10 :
			heure = str(h)+" : 0"+str(int(m))
		else :
			heure = str(h)+" : "+str(int(m))
		return heure
		
	def Clear(self):
		#INDICATE DATE 
		self.indicator.setText("Calcul des éphémérides solaires ")
		#CLEAR DATA
		
		self.solarTSM.display(0)
		self.solarEqt.display(0)
		self.solarTSV.display(0)
		self.solarH.display(0)
		self.solarA.display(0)
		self.solarD.display(0)
		self.solarAngH.display(0)
		self.sunRise.display(0)
		self.sunSet.display(0)
		self.sunDuration.display(0)
		
	def ActualCalcul(self):	
		
		self.now = time.strftime("%H:%M:%S")
		self.year = int(time.strftime("%Y"))
		self.month = int(time.strftime("%m"))
		self.day = int(time.strftime("%d"))
		
		self.hour = int(time.strftime("%H"))
		self.min = int(time.strftime("%M"))
		self.sec = int(time.strftime("%S"))
		#INDICATE DATE 
		self.indicator.setText("Calcul des éphémérides solaires pour le : "+self.Date+" à "+self.now)
		
		#LOCAL TIME/DATE
		self.timeDate.setDisplayFormat("dd/MM/yyyy")
		self.timeDate.setDate(QtCore.QDate(int(self.year),int(self.month), int(self.day)))
		
		#TIME
		self.timeTime.setDisplayFormat("hh:mm:ss")
		self.timeTime.setTime(QtCore.QTime(int(self.hour),int(self.min), int(self.sec)))
		
		#Time conversion in hours
		self.nowTime = (int(self.timeTime.time().hour()) + int(self.timeTime.time().minute()) / 60 + int(self.timeTime.time().second()) / 3600)
		self.Calcul.TL = self.hour +(self.min / 60) + (self.sec / 3600);
		#JDAY
		self.Calcul.JulianDay(self.timeDate.date().month(),self.timeDate.date().day())
		self.JDay.setText(str(self.Calcul.jDay))

		#CALCUL DES DONNEES HORAIRE
		self.Calcul.TempsUniversel( self.gpsLong.value(), self.gpsC.value())
		self.Calcul.TempsSM(self.gpsLong.value())
		self.Calcul.EquaTime()
		self.Calcul.TempsSV(self.gpsLong.value())
		
		#RECUPERATION DATA
		tsm = self.ConvertTime(self.Calcul.TSM)
		eqT = self.Calcul.EqTime
		tsv = self.ConvertTime(self.Calcul.TSV)
		
		#AFFICHAGE DATA
		self.solarTSM.display(tsm)
		self.solarEqt.display(eqT)
		self.solarTSV.display(tsv)
		
		#CALCUL DES COORDONNEES 
		self.Calcul.Declinaison()
		self.Calcul.AngleHoraire()
		self.Calcul.Hauteur(self.gpsLat.value())
		self.Calcul.Azimut()
		
		#RECUPERATION DATA
		decli = self.ConvertDegre(self.Calcul.Decli)
		angH = self.ConvertDegre(self.Calcul.AngH)
		hauteur = self.ConvertDegre(self.Calcul.Haut)
		azimut = self.ConvertDegre(self.Calcul.Azim)
		
		#AFFICHAGE DATA
		self.solarH.display(hauteur)
		self.solarA.display(azimut)
		self.solarD.display(decli)
		self.solarAngH.display(angH)
		
		#CALCUL DES DONNEES HORAIRE
		self.Calcul.Lever_Soleil(self.gpsLat.value())
		self.Calcul.Coucher_Soleil(self.gpsLat.value())
		self.Calcul.Duree_Soleil()
		
		#RECUPERATION DATA
		sR = self.ConvertTime(self.Calcul.leverS)
		sS = self.ConvertTime(self.Calcul.coucherS)
		sD = self.ConvertTime(self.Calcul.dureeS)
		
		#AFFICHAGE DATA
		self.sunRise.display(sR)
		self.sunSet.display(sS)
		self.sunDuration.display(sD)

		#TABLEWIDGET
		self.TableWidgetInit()
		
		self.tableWidget.clearContents()
		self.tableWidget.setRowCount(0)
		self.rowPosition = self.tableWidget.rowCount()
		self.tableWidget.insertRow(self.rowPosition)
		#self.tableWidget.setSortingEnabled(True)
		self.tableWidget.setItem(self.rowPosition , 0, QTableWidgetItem(str(self.now)))
		self.tableWidget.setItem(self.rowPosition , 1, QTableWidgetItem(str(self.ConvertTime(self.Calcul.TU))))
		self.tableWidget.setItem(self.rowPosition , 2, QTableWidgetItem(str(tsv)))
		self.tableWidget.setItem(self.rowPosition , 3, QTableWidgetItem(str(eqT)))
		self.tableWidget.setItem(self.rowPosition , 4, QTableWidgetItem(str(decli)))
		self.tableWidget.setItem(self.rowPosition , 5, QTableWidgetItem(str(angH)))
		self.tableWidget.setItem(self.rowPosition , 6, QTableWidgetItem(str(hauteur)))
		self.tableWidget.setItem(self.rowPosition , 7, QTableWidgetItem(str(azimut)))

	def DailyCalcul(self):
	
		#INDICATE DATE 
		self.indicator.setText("Calcul des éphémérides solaires pour le : "+str(self.timeDate.date().day())+"/"+str(self.timeDate.date().month())\
		+"/"+str(self.timeDate.date().year()))
		#Time conversion in hours
		self.Calcul.TL = (int(self.timeTime.time().hour()) + int(self.timeTime.time().minute()) / 60 + int(self.timeTime.time().second()) / 3600)
		
		#JDAY
		self.Calcul.JulianDay(self.timeDate.date().month(),self.timeDate.date().day())
		self.JDay.setText(str(self.Calcul.jDay))
		
	#CALCUL SUR 24h LEVER/COUCHER
		
		#CALCUL DES DONNEES HORAIRE
		self.Calcul.Lever_Soleil(self.gpsLat.value())
		self.Calcul.Coucher_Soleil(self.gpsLat.value())
		self.Calcul.Duree_Soleil()
		
		#RECUPERATION DATA
		sR = self.ConvertTime(self.Calcul.leverS)
		sS = self.ConvertTime(self.Calcul.coucherS)
		sD = self.ConvertTime(self.Calcul.dureeS)
		
		#AFFICHAGE DATA
		self.sunRise.display(sR)
		self.sunSet.display(sS)
		self.sunDuration.display(sD)

		#CALCUL DES DONNEES HORAIRE
		self.Calcul.TempsUniversel( self.gpsLong.value(), self.gpsC.value())
		self.Calcul.TempsSM(self.gpsLong.value())
		self.Calcul.EquaTime()
		self.Calcul.TempsSV(self.gpsLong.value())
		
		#RECUPERATION DATA
		tsm = self.ConvertTime(self.Calcul.TSM)
		eqT = self.Calcul.EqTime
		tsv = self.ConvertTime(self.Calcul.TSV)
		
		#AFFICHAGE DATA
		self.solarTSM.display(tsm)
		self.solarEqt.display(eqT)
		self.solarTSV.display(tsv)
		
		#CALCUL DES COORDONNEES 
		self.Calcul.Declinaison()
		self.Calcul.AngleHoraire()
		self.Calcul.Hauteur(self.gpsLat.value())
		self.Calcul.Azimut()
		
		#RECUPERATION DATA
		decli = self.ConvertDegre(self.Calcul.Decli)
		angH = self.ConvertDegre(self.Calcul.AngH)
		hauteur = self.ConvertDegre(self.Calcul.Haut)
		azimut = self.ConvertDegre(self.Calcul.Azim)
		
		#AFFICHAGE DATA
		self.solarH.display(hauteur)
		self.solarA.display(azimut)
		self.solarD.display(decli)
		self.solarAngH.display(angH)

		#TABLEWIDGET
		
		#CLEAN TABLE WIDGET
		self.TableWidgetInit()
		self.tableWidget.clearContents()
		self.tableWidget.setRowCount(0)
		self.rowPosition = self.tableWidget.rowCount()
		self.tableWidget.insertRow(self.rowPosition)
		#self.tableWidget.setSortingEnabled(True)
		self.tableWidget.setItem(self.rowPosition , 0, QTableWidgetItem(str(self.ConvertTime(self.Calcul.TL))))
		self.tableWidget.setItem(self.rowPosition , 1, QTableWidgetItem(str(self.ConvertTime(self.Calcul.TU))))
		self.tableWidget.setItem(self.rowPosition , 2, QTableWidgetItem(str(tsv)))
		self.tableWidget.setItem(self.rowPosition , 3, QTableWidgetItem(str(eqT)))
		self.tableWidget.setItem(self.rowPosition , 4, QTableWidgetItem(str(decli)))
		self.tableWidget.setItem(self.rowPosition , 5, QTableWidgetItem(str(angH)))
		self.tableWidget.setItem(self.rowPosition , 6, QTableWidgetItem(str(hauteur)))
		self.tableWidget.setItem(self.rowPosition , 7, QTableWidgetItem(str(azimut)))
	
	#TU INIT TO LOOP AND LISTS
		i = 0
		self.TLlist = []
		self.TUlist = []
		self.EqTlist = []
		self.TSMlist = []
		self.TSVlist = []
		self.Declilist = []
		self.AngHlist = []
		self.Hautlist = []
		self.Azimlist = []
		self.Calcul.TL = self.Calcul.leverS
		
		while self.Calcul.TL <= self.Calcul.coucherS :
			#CALCUL DES DONNEES HORAIRE
			self.Calcul.TempsUniversel( self.gpsLong.value(), self.gpsC.value())
			self.Calcul.TempsSM(self.gpsLong.value())
			self.Calcul.EquaTime()
			self.Calcul.TempsSV(self.gpsLong.value())
			
			#RECUPERATION DATA
			tsm = self.ConvertTime(self.Calcul.TSM)
			eqT = self.Calcul.EqTime
			tsv = self.ConvertTime(self.Calcul.TSV)
			
			#CALCUL DES COORDONNEES 
			self.Calcul.Declinaison()
			self.Calcul.AngleHoraire()
			self.Calcul.Hauteur(self.gpsLat.value())
			self.Calcul.Azimut()
			
			#RECUPERATION DATA
			decli = self.ConvertDegre(self.Calcul.Decli)
			angH = self.ConvertDegre(self.Calcul.AngH)
			hauteur = self.ConvertDegre(self.Calcul.Haut)
			azimut = self.ConvertDegre(self.Calcul.Azim)
			
			#APPEND ON LIST
			self.TLlist.append(self.Calcul.TL)
			self.TUlist.append(self.Calcul.TU)
			self.EqTlist.append(self.Calcul.EqTime)
			self.TSMlist.append(self.Calcul.TSM)
			self.TSVlist.append(self.Calcul.TSV)
			self.Declilist.append(self.Calcul.Decli)
			self.AngHlist.append(self.Calcul.AngH)
			self.Hautlist.append(self.Calcul.Haut)
			self.Azimlist.append(self.Calcul.Azim)
			
			self.Calcul.TL +=1
			i+=1
			
		# self.Graph(self.TLlist,self.Hautlist, "Hauteur du soleil","H = F(TU)","Temps U","Hauteur")
		self.Graph1(self.TLlist,self.Hautlist,"Hauteur sur la durée de l'esoleillement","Temps légal (H)","Hauteur (°)")

	def DailyHSun(self):
		try:
			#TABLEWIDGET
			#CLEAN TABLE WIDGET
			self.tableWidget.clear()
			self.tableWidget.clearContents()
			self.tableWidget.setRowCount(0)
			
			self.tableWidget.setColumnCount(5)
			self.tableWidget.setColumnWidth(0, 114)
			self.tableWidget.setColumnWidth(1, 114)
			self.tableWidget.setColumnWidth(2, 114)
			self.tableWidget.setColumnWidth(3, 114)
			self.tableWidget.setColumnWidth(4, 114)
			
			self.tableWidget.setHorizontalHeaderLabels(['TL', 'TU', 'TSM','EqT','TSV'])
			self.header = self.tableWidget.horizontalHeader()
			self.header.setDefaultAlignment(Qt.AlignHCenter)
			i=0
			for item in self.TLlist:
			
				self.rowPosition = self.tableWidget.rowCount()
				self.tableWidget.insertRow(self.rowPosition)
				#self.tableWidget.setSortingEnabled(True)
				self.tableWidget.setItem(self.rowPosition , 0, QTableWidgetItem(str(self.ConvertTime(item))))
				self.tableWidget.setItem(self.rowPosition , 1, QTableWidgetItem(str(self.ConvertTime(self.TUlist[i]))))
				self.tableWidget.setItem(self.rowPosition , 2, QTableWidgetItem(str(self.ConvertTime(self.TSMlist[i]))))
				self.tableWidget.setItem(self.rowPosition , 3, QTableWidgetItem(str(self.EqTlist[i])))
				self.tableWidget.setItem(self.rowPosition , 4, QTableWidgetItem(str(self.ConvertTime(self.TSVlist[i]))))
				i+=1
		except:
			self.DailyCalcul()
			
	def DailyEqHo(self):
		try:
			#TABLEWIDGET
			#CLEAN TABLE WIDGET
			self.tableWidget.clear()
			self.tableWidget.clearContents()
			self.tableWidget.setRowCount(0)
			
			self.tableWidget.setColumnCount(5)
			self.tableWidget.setColumnWidth(0, 114)
			self.tableWidget.setColumnWidth(1, 114)
			self.tableWidget.setColumnWidth(2, 114)
			self.tableWidget.setColumnWidth(3, 114)
			self.tableWidget.setColumnWidth(4, 114)
			
			self.tableWidget.setHorizontalHeaderLabels(['TL', 'δ°', 'ω°','H°','ψ°'])
			self.header = self.tableWidget.horizontalHeader()
			self.header.setDefaultAlignment(Qt.AlignHCenter)
			i=0
			for item in self.TLlist:
			
				self.rowPosition = self.tableWidget.rowCount()
				self.tableWidget.insertRow(self.rowPosition)
				#self.tableWidget.setSortingEnabled(True)
				self.tableWidget.setItem(self.rowPosition , 0, QTableWidgetItem(str(self.ConvertTime(item))))
				self.tableWidget.setItem(self.rowPosition , 1, QTableWidgetItem(str(self.ConvertDegre(self.Declilist[i]))))
				self.tableWidget.setItem(self.rowPosition , 2, QTableWidgetItem(str(self.ConvertDegre(self.AngHlist[i]))))
				self.tableWidget.setItem(self.rowPosition , 3, QTableWidgetItem(str(self.ConvertDegre(self.Hautlist[i]))))
				self.tableWidget.setItem(self.rowPosition , 4, QTableWidgetItem(str(self.ConvertDegre(self.Azimlist[i]))))
				i+=1
		except:
			self.DailyCalcul()
		
	def DailyHo(self):
		try:
			#TABLEWIDGET
			#CLEAN TABLE WIDGET
			self.tableWidget.clear()
			self.tableWidget.clearContents()
			self.tableWidget.setRowCount(0)
			
			self.tableWidget.setColumnCount(3)
			self.tableWidget.setColumnWidth(0, 187)
			self.tableWidget.setColumnWidth(1, 187)
			self.tableWidget.setColumnWidth(2, 187)
			
			self.tableWidget.setHorizontalHeaderLabels(['TL','H°','ψ°'])
			self.header = self.tableWidget.horizontalHeader()
			self.header.setDefaultAlignment(Qt.AlignHCenter)
			i=0
			for item in self.TLlist:
			
				self.rowPosition = self.tableWidget.rowCount()
				self.tableWidget.insertRow(self.rowPosition)
				#self.tableWidget.setSortingEnabled(True)
				self.tableWidget.setItem(self.rowPosition , 0, QTableWidgetItem(str(self.ConvertTime(item))))
				self.tableWidget.setItem(self.rowPosition , 1, QTableWidgetItem(str(self.ConvertDegre(self.Hautlist[i]))))
				self.tableWidget.setItem(self.rowPosition , 2, QTableWidgetItem(str(self.ConvertDegre(self.Azimlist[i]))))
				i+=1
		except:
			self.DailyCalcul()
		
	def DailyEq(self):
		try :
			#TABLEWIDGET
			#CLEAN TABLE WIDGET
			self.tableWidget.clear()
			self.tableWidget.clearContents()
			self.tableWidget.setRowCount(0)
			
			self.tableWidget.setColumnCount(3)
			self.tableWidget.setColumnWidth(0, 187)
			self.tableWidget.setColumnWidth(1, 187)
			self.tableWidget.setColumnWidth(2, 187)
			
			self.tableWidget.setHorizontalHeaderLabels(['TL', 'δ°', 'ω°'])
			self.header = self.tableWidget.horizontalHeader()
			self.header.setDefaultAlignment(Qt.AlignHCenter)
			i=0
			for item in self.TLlist:
			
				self.rowPosition = self.tableWidget.rowCount()
				self.tableWidget.insertRow(self.rowPosition)
				#self.tableWidget.setSortingEnabled(True)
				self.tableWidget.setItem(self.rowPosition , 0, QTableWidgetItem(str(self.ConvertTime(item))))
				self.tableWidget.setItem(self.rowPosition , 1, QTableWidgetItem(str(self.ConvertDegre(self.Declilist[i]))))
				self.tableWidget.setItem(self.rowPosition , 2, QTableWidgetItem(str(self.ConvertDegre(self.AngHlist[i]))))
				i+=1
		except:
			self.DailyCalcul()

	def Stat(self,listx,listy, labelP,titre,labelx,labely):
	#List on X,List on Y, Label plot,label X/Y, indicator for second plot ..SAME P2
	
		x=[]
		y=[]
		i=0
		for item in listx:
			absis = str(listx[i]).strip("(',')")
			try:
				x.append(int(absis))
			except:
				x.append(absis)
			absis = str(listy[i]).strip("(',')")
			try:
				y.append(int(absis))
			except:
				y.append(absis)
			i+=1
		plt.ylim(min(y), max(y))
		plt.scatter(x, y)
		plt.plot(x, y, label=labelP)  # Plot some data on the (implicit) axes.
		# plt.plot(x, x**3, label='cubic')
		plt.xlabel(labelx)
		plt.ylabel(labely)
		plt.title(titre)
		plt.legend()
		plt.show()

	def Graph1(self,listx,listy,title,titlex,titley) :
		self.graphWidget = pg.PlotWidget()
		#STYLING
		self.graphWidget.setBackground('#f9fafc')
		self.graphWidget.setTitle(title)
		styles = {'color':'r', 'font-size':'12px'}
		self.graphWidget.setLabel('left', titley, **styles)
		self.graphWidget.setLabel('bottom', titlex, **styles)
		self.graphWidget.showGrid(x=True, y=True)

		self.dockWidget.setWidget(self.graphWidget)

		x = listx
		y = listy

		# plot data: x, y values
		pen = pg.mkPen("#3c80e5")
		self.graphWidget.plot(x, y, pen=pen, symbol='+', symbolSize=5, symbolBrush=("#3c80e5"))	
	
	def Graph2(self,listx,listy,title,titlex,titley,listk,titlek) :
		self.graphWidget = pg.PlotWidget()
		#STYLING
		self.graphWidget.setBackground('#f9fafc')
		self.graphWidget.setTitle(title)
		style1 = {'color':'r', 'font-size':'12px'}
		style2 = {'color':'b', 'font-size':'12px'}
		self.graphWidget.setLabel('left', titley, **style1)
		self.graphWidget.setLabel('bottom', titlex, **style1)
		self.graphWidget.setLabel('left', titlek, **style2)
		self.graphWidget.showGrid(x=True, y=True)
		mkPen('y', width=3, style=QtCore.Qt.DashLine)          ## Make a dashed yellow line 2px wide
		mkPen(0.5)                                             ## solid grey line 1px wide
		mkPen(color=(200, 200, 255), style=QtCore.Qt.DotLine)  ## Dotted pale-blue line

		self.dockWidget.setWidget(self.graphWidget)

		x = listx
		y = listy
		k = listk

		# plot data: x, y values
		self.plot(x, y, "#3c80e5")
		self.plot(x, k,"r")

	def plot(self, x, y, color):
		pen = pg.mkPen(color=color)
		self.graphWidget.plot(x, y, pen=pen, symbol='+', symbolSize=5, symbolBrush=(color))		

	def GraphSlot(self):
		sender = self.sender()
		try:
			if sender == self.graphEq :
				self.Graph2(self.TLlist,self.Declilist,"C.Equatoriales sur la la durée de l'esoleillement","Temps légal (H)","Declinaison (°)",\
				self.AngHlist,"Angle Horaire/Déclinaison")
			if sender == self.graphDecli :
				self.Graph1(self.TLlist,self.Declilist,"Declinaison sur la durée de l'esoleillement","Temps légal (H)","Declinaison (°)")
			if sender == self.graphAngH :
				self.Graph1(self.TLlist,self.AngHlist,"Angle Horaire sur la durée de l'esoleillement","Temps légal (H)","AngleHoraire (°)")
				
			if sender == self.graphHo :
				self.Graph2(self.TLlist,self.Hautlist,"C.Horizontales sur la la durée de l'esoleillement","Temps légal (H)","Hauteur (°)",\
				self.Azimlist,"Azimut/Hauteur")
			if sender == self.graphH :
				self.Graph1(self.TLlist,self.Hautlist,"Hauteur sur la durée de l'esoleillement","Temps légal (H)","Hauteur (°)")
			if sender == self.graphA :
				self.Graph1(self.TLlist,self.Azimlist,"Azimut sur la durée de l'esoleillement","Temps légal (H)","Azimut (°)")
				
			if sender == self.graphSun :
				self.Graph1(self.TLlist,self.TSVlist,"Heure Solaire Vraie sur la durée de l'esoleillement","Temps légal (H)","TSV (°)")
		except:
			self.DailyCalcul()
	
if __name__ == '__main__':
    
	app = QApplication(sys.argv)
	ex = Helios()
    
	sys.exit(app.exec_())