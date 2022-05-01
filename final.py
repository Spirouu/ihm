#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 07:08:22 2022
   
@author: Théo Chaloyard
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore

from fenDossier import Dossier
from importation import Importation
from basemedicament import verifbdmedicament


class View(QWidget):
    def __init__(self, ctrl):
        super().__init__()

        self.dossier = Dossier(self)
        self.importer = Importation(self)
        self.verif_medicament = verifbdmedicament()

        self.myCtrl = ctrl
        self.setGeometry(0, 0, 400, 400)
        self.setFixedWidth(400)
        self.setFixedHeight(400)

        self.b1 = QPushButton('Créer un dossier')
        self.b2 = QPushButton('Importer un dossier')
        self.b1.setStyleSheet("background-color : #5CD2F5 ; border-style: outset ; border-width: 0 px; border-radius: 5px;  color : white ; padding: 4px")
        self.b2.setStyleSheet("background-color : #5CD2F5 ; border-style: outset ; border-width: 0 px; border-radius: 5px;  color : white ; padding: 4px")
        self.b1.setToolTip("Ouvrir la fenêtre permettant la créeation d'une fiche patient")
        self.b2.setToolTip("Importer la fiche d'un patient")

        self.com1 = QLabel("The platforme ;)")
        self.com2 = QLabel("Bienvenue !")
        self.com1.setAlignment(QtCore.Qt.AlignCenter)
        self.com2.setAlignment(QtCore.Qt.AlignCenter)

        self.image = QLabel(self)
        self.pixmap = QPixmap('imagee$.png')
        self.image.setPixmap(self.pixmap.scaled(100,100))
        self.image.setAlignment(QtCore.Qt.AlignCenter)

        self.init_ui()
        self.show()

    def init_ui(self):
        h_box = QVBoxLayout()
        h_box.addWidget(self.b1)
        h_box.addWidget(self.b2)

        h_box2 = QVBoxLayout()
        h_box2.addStretch()
        h_box2.addWidget(self.image)
        h_box2.addStretch()

        v_box = QVBoxLayout()
        v_box.addLayout(h_box2)
        v_box.addWidget(self.com1)
        v_box.addWidget(self.com2)
        v_box.addLayout(h_box)

        self.setLayout(v_box)
        self.setWindowTitle('Bienvenue !')

        self.b1.clicked.connect(self.btn1_click)
        self.b2.clicked.connect(self.btn2_click)

    def btn1_click(self):
        self.hide()
        self.verif_medicament
        self.dossier.show()

    def btn2_click(self):
        print("Ok")
        self.hide()
        self.importer.show()


#%%
class Controller:
    def __init__(self, model):
        self.myModel = model


#%%
class Model:
    def __init__(self):
        self.myMoney = 0


if __name__ == '__main__':
    app = QApplication(sys.argv)
    model = Model()
    ctrl = Controller(model)
    view = View(ctrl)
    sys.exit(app.exec_())
