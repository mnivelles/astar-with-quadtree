#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Tkinter as tk
from twisted.internet import tksupport


def affiche_quadtree(liste_obstacles, racine_quadtree, chemin, taille, chemin_positions=None):
    if not chemin_positions: chemin_positions = []
    rapport = 400.0 / float(taille)

    largeur = 500
    hauteur = 500
    racine = tk.Tk()
    racine.geometry("{0}x{1}+400+100".format(largeur, hauteur))
    racine.resizable(0, 0)
    racine.title("Dessin du quadtree avec les obstacles")
    app = tk.Frame(racine, width=largeur, height=hauteur, background="#333333")
    app.pack(fill=tk.BOTH, expand=1)

    plateau = tk.Canvas(app, width=400, height=400, background="#f0f0f0")
    plateau.config(highlightbackground="#999")
    plateau.place(x=50, y=50)

    couleurs = ["#409Ff9", "#1F8BBF", "#01619F", "#0E4EAD"]
    i = 0
    for obstacle in liste_obstacles:
        x1 = obstacle.bas_gauche.x * rapport
        y1 = obstacle.bas_gauche.y * rapport
        x2 = obstacle.haut_droite.x * rapport
        y2 = obstacle.haut_droite.y * rapport
        x1, y1 = y1, x1 # ajustement des axes
        x2, y2 = y2, x2 # ajustement des axes
        plateau.create_rectangle(x1, y1, x2, y2, width=0, fill=couleurs[i % 4])
        i += 1

    for quadnoeud in chemin:
        x1 = int(float(quadnoeud.bas_gauche.x) * rapport)
        y1 = int(float(quadnoeud.bas_gauche.y) * rapport)
        x2 = int(float(quadnoeud.haut_droite.x) * rapport)
        y2 = int(float(quadnoeud.haut_droite.y) * rapport)
        x1, y1 = y1, x1 # ajustement des axes
        x2, y2 = y2, x2 # ajustement des axes
        plateau.create_rectangle(x1, y1, x2, y2, width=1, fill="#00b05a")

    positions = list()
    for position in chemin_positions:
        x = int(float(position.x) * rapport)
        y = int(float(position.y) * rapport)
        x, y = y, x
        positions.append((x, y))
    if len(positions) > 0:
        plateau.create_line(positions, fill="purple", width=2)

    tksupport.install(racine)
    racine.mainloop()


def renvoie_arbre_par_niveau(racine):
    if racine is None:
        return
    niveau_courant = list()
    prochain_niveau = list()
    niveau_courant.append(racine)
    liste = list()
    while len(niveau_courant) != 0:
        noeud_courant = niveau_courant.pop(0)
        if noeud_courant is not None:
            liste.append(noeud_courant)
            prochain_niveau.append(noeud_courant.nord_ouest)
            prochain_niveau.append(noeud_courant.nord_est)
            prochain_niveau.append(noeud_courant.sud_est)
            prochain_niveau.append(noeud_courant.sud_ouest)
        if len(niveau_courant) == 0:
            niveau_courant, prochain_niveau = prochain_niveau, niveau_courant
    return liste
