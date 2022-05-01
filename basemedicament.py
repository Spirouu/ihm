#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 07:08:22 2022

@author: Théo Chaloyard
"""


import paramiko
import dbm

def verifbdmedicament():
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

            with dbm.open('dbmedicaments', 'c') as db:
                print(len(db.keys()))
                if len(db.keys()) == 10:
                    pass
                else:
                    db["Doliprane (antalgique)"] = "reduction des douleurs"
                    db["Dafalgan (antalgique)"] = "reduction des douleurs"
                    db["Efferalgan (antalgique)"] = "reduction des douleurs"
                    db["Kardegic (antiagrégant)"] = "pontage coronarien fibrillation auriculaire"
                    db["Spasfon (antispasmodique)"] = "atherosclerose infarctus crise cardiaque AVC pontage " \
                                                      "coronarien fibrillation auriculaire"
                    db["Gaviscon (antiacide d'action locale)"] = "mal de ventre remontees acides"
                    db["Dexeryl NE PAS PRESCRIRE (protecteur cutané)"] = "secheresse de la peau"
                    db["MeteoSpasmyl (antispasmodique à visée digestive)"] = "dereglements dereglement chronique de" \
                                                                             " l intestin"
                    db["Biseptine (antiseptique)"] = "plaies plaie peu profonde profondes et " \
                                                     "dans le traitement d appoint des lesions cutanees" \
                                                     " infectees ou exposees a un risque d infection"
                    db["Eludril (bain de douche antiseptique)"] = "affections de la bouche ou après une " \
                                                                  "opération des dents ou des gencives"
            db.close()
            sftp.put(nom_local, chemin_vm)

        except:

            with dbm.open('dbmedicaments', 'c') as db:
                db["Doliprane (antalgique)"] = "reduction douleurs douleur"
                db["Dafalgan (antalgique)"] = "reduction douleurs douleur"
                db["Efferalgan (antalgique)"] = "reduction douleurs douleur"
                db["Kardegic (antiagrégant)"] = "atherosclerose infarctus crise cardiaque AVC pontage " \
                                                  "coronarien fibrillation auriculaire"
                db["Spasfon (antispasmodique)"] = "mal ventre intestin urinaire uterus"
                db["Gaviscon (antiacide d'action locale)"] = "mal ventre remontees acides"
                db["Dexeryl NE PAS PRESCRIRE (protecteur cutané)"] = "secheresse peau"
                db["MeteoSpasmyl (antispasmodique à visée digestive)"] = "dereglements dereglement chronique " \
                                                                         "intestin"
                db["Biseptine (antiseptique)"] = "plaies plaieprofonde profondes " \
                                                 "dans traitement appoint lesions cutanees" \
                                                 " infectees exposees risque infection"
                db["Eludril (bain de douche antiseptique)"] = "affections bouche après " \
                                                              "opération dents gencives"

            db.close()
            sftp.put(nom_local, chemin_vm)

    finally:
        t.close()


hostname = "172.20.10.3"
username = "theo"
password = "Haribo04"
port = 22