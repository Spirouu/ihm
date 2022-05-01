#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 07:08:22 2022

@author: Théo Chaloyard
"""


import paramiko
from PyQt5.QtWidgets import *
import dbm
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore


class Importation(QWidget):
    def __init__(self, back):
        super().__init__()

        self.fermer = QPushButton("Fermer")
        self.fermer.setStyleSheet("background-color : #5CD2F5 ; border-style: outset ; border-width: 0 px; border-radius: 5px;  color : white ; padding: 4px")

        self.fermer.setToolTip("Revenir à la fênetre principale")


        self.fprec = back

        self.init_ui()

    def init_ui(self):
        h_bas = QHBoxLayout()
        h_bas.addWidget(self.fermer)
        self.setLayout(h_bas)

        self.fermer.clicked.connect(self.btn_fermer)


    def btn_fermer(self):
        self.fprec.show()



