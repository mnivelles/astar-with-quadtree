#!/usr/bin/env python
# -*- coding: utf-8 -*-

from quadnoeud import Quadnoeud
from quadnoeud_obstrue_exception import QuadnoeudObstrueException
from point import Point


class Quadtree(object):
    def __init__(self, liste_obstacles, taille=2, resolution=1):
        if resolution < 1:
            raise RuntimeError("La résolution doit être supérieur à 0.")
        elif taille < resolution * 2:
            raise RuntimeError("La taille de la grille doit être supérieur ou égale à deux fois la résolution")
        self._racine = Quadnoeud(liste_obstacles, Point(0, 0), Point(taille, taille), resolution)

    def trouve_noeud(self, point):
        if self._racine.est_dedans(point) is False:
            raise RuntimeError("La position donnée est hors des limites")

        noeud = self._racine
        while noeud.est_feuille() is False:
            x_milieu = noeud.bas_gauche.x + noeud.renvoie_largeur() / 2
            y_milieu = noeud.bas_gauche.y + noeud.renvoie_hauteur() / 2

            if point.x < x_milieu:
                if point.y < y_milieu:
                    noeud = noeud.sud_ouest
                else:
                    noeud = noeud.nord_ouest
            else:
                if point.y < y_milieu:
                    noeud = noeud.sud_est
                else:
                    noeud = noeud.nord_est

        if noeud._status == Quadnoeud.Etat.OBSTRUE:
            raise QuadnoeudObstrueException(
                "Noeud obstrué. Il y a un obstacle à cet endroit. Votre position : {0}, quadnoeud : {1}.".format(point,
                                                                                                                 noeud))

        return noeud

    def __str__(self):
        return self._renvoie_arbre_par_niveau_chaine()

    def _renvoie_arbre_par_niveau_chaine(self):
        if self._racine is None:
            return
        niveau_courant = list()
        prochain_niveau = list()
        niveau_courant.append(self._racine)
        chaine = str()
        while len(niveau_courant) != 0:
            noeud_courant = niveau_courant.pop(0)
            if noeud_courant is not None:
                chaine += str(noeud_courant) + " "
                prochain_niveau.append(noeud_courant.nord_ouest)
                prochain_niveau.append(noeud_courant.nord_est)
                prochain_niveau.append(noeud_courant.sud_est)
                prochain_niveau.append(noeud_courant.sud_ouest)
            if len(niveau_courant) == 0:
                chaine += "\n"
                niveau_courant, prochain_niveau = prochain_niveau, niveau_courant
        return chaine