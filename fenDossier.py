#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 07:08:22 2022

@author: Théo Chaloyard
"""


import paramiko
from PyQt5.QtWidgets import *
import dbm
from histoo import Historique
from PyQt5.QtGui import QFont


class Dossier(QWidget):
    def __init__(self, back):
        super().__init__()

        QToolTip.setFont(QFont('Arial', 14))

        self.histori = Historique(self)

        self.pb_medic = ""
        self.mot_pb = []
        self.symptomes = []
        self.medic_possible = []

        # Labels
        self.lname = QLabel("Nom")
        self.lfirst_name = QLabel("Prénom")
        self.lage = QLabel("Âge")
        self.lsex = QLabel("Sexe")

        # boutons du bas
        self.fermer = QPushButton("Fermer")
        self.enregistrer = QPushButton("Enregistrer")
        self.historique = QPushButton("Historique")
        self.fermer.setStyleSheet("background-color : #5CD2F5 ; border-style: outset ; border-width: 0 px; border-radius: 5px;  color : white ; padding: 4px")
        self.enregistrer.setStyleSheet("background-color : #5CD2F5 ; border-style: outset ; border-width: 0 px; border-radius: 5px;  color : white ; padding: 4px")
        self.historique.setStyleSheet("background-color : #5CD2F5 ; border-style: outset ; border-width: 0 px; border-radius: 5px;  color : white ; padding: 4px")

        self.historique.setToolTip("Afficher l'historique du patient")
        self.enregistrer.setToolTip("Enregistrer la fiche")
        self.fermer.setToolTip("Revenir à la fênetre principale")

        # zones de saisies et radio boutons
        self.name = QLineEdit()
        self.name.setPlaceholderText('Nom')
        self.first_name = QLineEdit()
        self.first_name.setPlaceholderText('Prénom')

        self.age = QLineEdit()
        self.age.setPlaceholderText('Âge')
        self.male = QRadioButton("Homme")
        self.female = QRadioButton("Femme")

        # Textes du mileu
        self.probleme = QTextEdit()
        self.medicament = QTextEdit()
        self.probleme.setPlaceholderText("Search..")
        self.medicament.setPlaceholderText("Médicament possible :")
        self.medicament.setReadOnly(True)

        self.fprec = back
        self.init_ui()

    def init_ui(self):
        # Radio bouton
        h_radio = QHBoxLayout()
        h_radio.addWidget(self.male)
        h_radio.addWidget(self.female)

        # label
        v_label = QVBoxLayout()
        v_label.addWidget(self.lname)
        v_label.addWidget(self.lfirst_name)
        v_label.addWidget(self.lage)
        v_label.addWidget(self.lsex)

        # saisies
        v_cases = QVBoxLayout()
        v_cases.addWidget(self.name)
        v_cases.addWidget(self.first_name)
        v_cases.addWidget(self.age)
        v_cases.addLayout(h_radio)

        # Blocs de gauche
        h_infos = QHBoxLayout()
        h_infos.addLayout(v_label)
        h_infos.addLayout(v_cases)

        # Bloc du haut
        h_haut = QHBoxLayout()
        h_haut.addLayout(h_infos)
        h_haut.addWidget(self.historique)

        # Blo du milieu
        h_text = QHBoxLayout()
        h_text.addWidget(self.probleme)
        h_text.addWidget(self.medicament)

        # Boutons du bas
        h_bas = QHBoxLayout()
        h_bas.addWidget(self.enregistrer)
        h_bas.addWidget(self.fermer)

        # Final
        v_final = QVBoxLayout()
        v_final.addLayout(h_haut)
        v_final.addLayout(h_text)
        v_final.addLayout(h_bas)

        v_box = QVBoxLayout()
        v_box.addLayout(v_final)

        self.setLayout(v_box)
        self.setWindowTitle('Bienvenue !')

        self.fermer.clicked.connect(self.btn_fermer)
        self.enregistrer.clicked.connect(self.btn_enregistrer)
        self.historique.clicked.connect(self.btn_historique)

        self.probleme.textChanged.connect(self.textSonDurum)

    def bdmedoc():
        print("bd importée")
        global hostname
        global username
        global password
        global port

        try:
            t = paramiko.Transport((hostname, port))
            t.connect(username=username, password=password)
            sftp = paramiko.SFTPClient.from_transport(t)

            nom_local = "dbmedicaments.txt"

            chemin_vm = "/Users/theo/exo/dbmedicaments.db"
            try:
                sftp.get(chemin_vm, nom_local)
            except:
                print("pas de bd")
        finally:
            t.close()

    def textSonDurum(self):

        self.mot_pb = self.probleme.toPlainText().split(' ')
        self.medic_possible = []
        self.medicament.clear()
        with dbm.open('dbmedicaments', 'c') as db:
            for pb in self.mot_pb:
                for medic in db.keys():
                    self.symptomes = []
                    self.symptomes.append(db[medic].decode('UTF-8').split(' '))
                    for symp in self.symptomes:
                        for symptome in symp:
                            if pb == symptome:
                                self.medic_possible.append(medic.decode('UTF-8'))
                                print(medic.decode('UTF-8'))


        db.close()

        afficher = "Médicament possible : "
        for i in self.medic_possible:
            afficher += "\n"
            afficher += str(i)
        self.medicament.setText(afficher)


    def btn_fermer(self):
        self.close()
        self.fprec.show()

    def btn_historique(self):
        global hostname
        global username
        global password
        global port

        kay = 0
        self.nom_prenomm = ""
        nm_pm = self.name.text().strip() + ',' + self.first_name.text().strip()
        try:
            t = paramiko.Transport((hostname, port))
            t.connect(username=username, password=password)
            sftp = paramiko.SFTPClient.from_transport(t)

            nom_local = "test.txt"

            chemin_vm = "/Users/theo/exo/liste.db"
            try:
                sftp.get(chemin_vm, nom_local)

                with dbm.open('liste', 'c') as db:
                    for i in db.keys():
                        self.nom_prenomm = []
                        fiche = str(db[i].decode('UTF-8')).split('$')
                        self.nom_prenomm = fiche[0]
                        print(self.nom_prenomm)

                        if self.nom_prenomm == nm_pm:
                            kay = i
                            self.histori.recvVal(kay)
                            self.histori.show()
                        else:
                            pass

                db.close()


                sftp.put(nom_local, chemin_vm)
            except:

                print("La personne n'a pas d'historique")

        finally:
            t.close()
            pass

    def btn_enregistrer(self):
        global hostname
        global username
        global password
        global port

        self.pb_medic = "Symptômes : " + self.probleme.toPlainText() + ' \n ' + self.medicament.toPlainText()
        #print(self.pb_medic)
        if self.male.isChecked():
            genre = "Homme"
        else:
            genre = "Femme"

        #print(genre)
        try:
            t = paramiko.Transport((hostname, port))
            t.connect(username=username, password=password)
            sftp = paramiko.SFTPClient.from_transport(t)

            nom_local = "test.txt"

            chemin_vm = "/Users/theo/exo/liste.db"
            try:
                sftp.get(chemin_vm, nom_local)
                print("yoo")
                symp_medoc = ""
                flag = 0

                with dbm.open('liste', 'c') as db:

                    for keyy in db.keys():
                        fiche = str(db[keyy].decode('UTF-8'))
                        nom_prenom = fiche.split('$')[0]

                        # Reste
                        reste = fiche.split('$')[1]
                        symp_medoc = reste.split(',')[2]

                        print("ok")
                        print(str(self.name.text().strip()) + ',' + str(self.first_name.text().strip()))
                        print(nom_prenom.strip())
                        if str(self.name.text().strip()) + ',' + str(self.first_name.text().strip()) == nom_prenom:
                            flag = 1
                            clee_du_type = keyy
                            sympomm = symp_medoc
                        else:
                            flag = 0

                        print(flag)
                    if flag == 1:
                        db[clee_du_type] = str(self.name.text().strip()) + ',' + str(self.first_name.text().strip()) \
                                        + '$' + str(self.age.text().strip()) + ',' + str(genre) + \
                                        ',' + sympomm + '\n\n' + str(self.pb_medic)
                    else:
                        long = len(db.keys()) + 1
                        db[str(long)] = str(self.name.text().strip()) + ',' + str(self.first_name.text().strip()) \
                                        + '$' + str(self.age.text().strip()) + ',' + str(genre) + \
                                        ',' + str(self.pb_medic)

                db.close()

                sftp.put(nom_local, chemin_vm)
            except:

                with dbm.open('liste', 'c') as db:
                    long = len(db.keys()) + 1
                    db[str(long)] = str(self.name.text().strip()) + ',' + str(self.first_name.text().strip()) \
                                    + '$' + str(self.age.text().strip()) + ',' + str(genre) + \
                                    ',' + str(self.pb_medic)

                db.close()

                sftp.put(nom_local, chemin_vm)

        finally:
            t.close()
            print("ssh end")


hostname = "ip"
username = "username"
password = "password"
port = 22
Dossier.bdmedoc()
