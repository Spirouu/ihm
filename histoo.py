#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 07:08:22 2022

@author: Théo Chaloyard
"""


import paramiko
from PyQt5.QtWidgets import *
import dbm


class Historique(QWidget):
    def __init__(self, back):
        super().__init__()

        self.nom_prenom = []
        # Labels
        self.lnom = QLabel("Nom")
        self.lprenom = QLabel("Prénom")
        self.lagee = QLabel("Âge")

        # boutons du bas
        self.fermerr = QPushButton("Fermer")
        self.fermerr.setStyleSheet("background-color : #5CD2F5 ; border-style: outset ; border-width: 0 px; border-radius: 5px;  color : white ; padding: 4px")


        # zones de saisies et radio boutons
        self.name = QLineEdit()
        self.name.setPlaceholderText('Nom')
        self.name.setReadOnly(True)
        self.first_name = QLineEdit()
        self.first_name.setPlaceholderText('Prénom')
        self.first_name.setReadOnly(True)
        self.agee = QLineEdit()
        self.agee.setPlaceholderText('Âge')
        self.agee.setReadOnly(True)

        # Historique
        self.passe_patient = QTextEdit()
        self.passe_patient.setReadOnly(True)

        self.init_ui()

    def init_ui(self):
        # label
        vv_label = QVBoxLayout()
        vv_label.addWidget(self.lnom)
        vv_label.addWidget(self.lprenom)
        vv_label.addWidget(self.lagee)

        # saisies
        vv_cases = QVBoxLayout()
        vv_cases.addWidget(self.name)
        vv_cases.addWidget(self.first_name)
        vv_cases.addWidget(self.agee)

        # Blocs de gauche
        hh_infos = QHBoxLayout()
        hh_infos.addLayout(vv_label)
        hh_infos.addLayout(vv_cases)

        # Final
        vv_final = QVBoxLayout()
        vv_final.addLayout(hh_infos)
        vv_final.addWidget(self.passe_patient)
        vv_final.addWidget(self.fermerr)

        # Boutons appuyés
        self.fermerr.clicked.connect(self.btn_fermerr)

        self.setLayout(vv_final)
        self.setWindowTitle('Historique !')


    def btn_fermerr(self):
        self.close()

    def recvVal(self, fnom):
        print("biiiiiip")
        global hostname
        global username
        global password
        global port

        try:
            t = paramiko.Transport((hostname, port))
            t.connect(username=username, password=password)
            sftp = paramiko.SFTPClient.from_transport(t)

            nom_local = "test.txt"

            chemin_vm = "/Users/theo/exo/liste.db"
            try:
                sftp.get(chemin_vm, nom_local)

                with dbm.open('liste', 'c') as db:

                    fiche = str(db[fnom].decode('UTF-8'))
                    nom_prenom = fiche.split('$')[0]
                    nom = nom_prenom.split(',')[0]
                    prenom = nom_prenom.split(',')[1]
                    print("Le nom est ", nom, " et le prénom est ", prenom)
                    self.name.setText(nom)
                    self.first_name.setText(prenom)


                    # Reste
                    reste = fiche.split('$')[1]
                    age = reste.split(',')[0]
                    print("age : ", age)
                    self.agee.setText(age)
                    sexe = reste.split(',')[1]
                    print("sexe : ", sexe)
                    symp_medoc = reste.split(',')[2]
                    print("pb : ", symp_medoc)
                    self.passe_patient.setText(symp_medoc)

                    print(fiche)

                db.close()

                sftp.put(nom_local, chemin_vm)
            except:

                print("La personne n'a pas d'historique")

        finally:
            t.close()
            pass


hostname = "ip"
username = "username"
password = "password"
port = 22






