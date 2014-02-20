#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import enumeration
from point import Point


class Quadnoeud(object):
    """
              Nord
          .----.----.
          | NO | NE |
    Ouest '----'----' Est
          | SO | SE |
          '----'----'
              Sud
    """
    Cote = enumeration.enum("NORD", "EST", "SUD", "OUEST")
    Quadrant = enumeration.enum("NORD_OUEST", "NORD_EST", "SUD_EST", "SUD_OUEST")
    Etat = enumeration.enum("LIBRE", "MIXTE", "OBSTRUE")

    ADJACENT = [#  NO     NE     SE     SO
                [True, True, False, False], # N
                [False, True, True, False], # E
                [False, False, True, True], # S
                [True, False, False, True]  # O
    ]

    REFLET = [#         NO                  NE                   SE                  SO
              [Quadrant.SUD_OUEST, Quadrant.SUD_EST, Quadrant.NORD_EST, Quadrant.NORD_OUEST], # N
              [Quadrant.NORD_EST, Quadrant.NORD_OUEST, Quadrant.SUD_OUEST, Quadrant.SUD_EST], # E
              [Quadrant.SUD_OUEST, Quadrant.SUD_EST, Quadrant.NORD_EST, Quadrant.NORD_OUEST], # S
              [Quadrant.NORD_EST, Quadrant.NORD_OUEST, Quadrant.SUD_OUEST, Quadrant.SUD_EST]  # O
    ]

    #            N          E           S          O
    OPPOSE = [Cote.SUD, Cote.OUEST, Cote.NORD, Cote.EST]

    def __init__(self, liste_obstacles, bas_gauche, haut_droite, resolution, parent=None):
        if parent is None:
            self._construit_racine(liste_obstacles, bas_gauche, haut_droite, resolution)
        else:
            self._construit_noeud(liste_obstacles, bas_gauche, haut_droite, resolution, parent)

    def _construit_racine(self, liste_obstacles, bas_gauche, haut_droite, resolution):
        self._parent = None
        self.nord_ouest = None
        self.nord_est = None
        self.sud_est = None
        self.sud_ouest = None
        self.bas_gauche = bas_gauche
        self.haut_droite = haut_droite
        self._status = Quadnoeud.Etat.MIXTE

        self._subdivise(liste_obstacles, resolution)

    def _construit_noeud(self, liste_obstacles, bas_gauche, haut_droite, resolution, parent):
        self._parent = parent
        self.nord_ouest = None
        self.nord_est = None
        self.sud_est = None
        self.sud_ouest = None
        self.bas_gauche = bas_gauche
        self.haut_droite = haut_droite
        self._status = Quadnoeud.Etat.MIXTE

        for obstacle in liste_obstacles:
            if obstacle.intersecte(bas_gauche, haut_droite):
                if obstacle.obstrue(bas_gauche, haut_droite) \
                    or self.renvoie_largeur() <= resolution \
                    or self.renvoie_hauteur <= resolution:
                    self._status = Quadnoeud.Etat.OBSTRUE
                else:
                    self._subdivise(liste_obstacles, resolution)
                return

        self._status = Quadnoeud.Etat.LIBRE

    def __str__(self):
        return "{" + str(self.bas_gauche) + ", " + str(self.haut_droite) + "}"

    def __repr__(self):
        return "{" + str(self.bas_gauche) + ", " + str(self.haut_droite) + "}"

    def _subdivise(self, liste_obstacles, resolution):
        self._status = Quadnoeud.Etat.MIXTE

        # Ne fonctionne pas avec des flottant
        x0 = self.bas_gauche.x                                  #  y2 .----.-------.
        x1 = self.bas_gauche.x + self.renvoie_largeur() / 2     #     |    |       |
        x2 = self.haut_droite.x                                 #     | NO |  NE   |
        #     |    |       |
        y0 = self.bas_gauche.y                                  #  y1 '----'-------'
        y1 = self.bas_gauche.y + self.renvoie_hauteur() / 2     #     | SO |  SE   |
        y2 = self.haut_droite.y                                 #  y0 '----'-------'
        #     x0   x1     x2
        self.nord_ouest = Quadnoeud(liste_obstacles, Point(x0, y1), Point(x1, y2), resolution, self)
        self.nord_est = Quadnoeud(liste_obstacles, Point(x1, y1), Point(x2, y2), resolution, self)
        self.sud_est = Quadnoeud(liste_obstacles, Point(x1, y0), Point(x2, y1), resolution, self)
        self.sud_ouest = Quadnoeud(liste_obstacles, Point(x0, y0), Point(x1, y1), resolution, self)

    def _est_adjacent(self, cote, quadrant):
        return Quadnoeud.ADJACENT[cote][quadrant]

    def _renvoie_reflet(self, cote, quadrant):
        return Quadnoeud.REFLET[cote][quadrant]

    def _renvoie_oppose(self, cote):
        return Quadnoeud.OPPOSE[cote]

    def _renvoie_quadrant(self):
        if self._parent is None:
            raise RuntimeError("Le quadrant du noeud racine n'est pas défini.")
        if self._parent.nord_ouest == self:
            return Quadnoeud.Quadrant.NORD_OUEST
        elif self._parent.nord_est == self:
            return Quadnoeud.Quadrant.NORD_EST
        elif self._parent.sud_est == self:
            return Quadnoeud.Quadrant.SUD_EST
        else:
            return Quadnoeud.Quadrant.SUD_OUEST

    def renvoie_enfant(self, quadrant):
        if quadrant == Quadnoeud.Quadrant.NORD_OUEST:
            return self.nord_ouest
        elif quadrant == Quadnoeud.Quadrant.NORD_EST:
            return self.nord_est
        elif quadrant == Quadnoeud.Quadrant.SUD_EST:
            return self.sud_est
        elif quadrant == Quadnoeud.Quadrant.SUD_OUEST:
            return self.sud_ouest
        else:
            raise RuntimeError("Le quadrant passé n'est pas valide.")

    def _ajoute_enfants(self, cote, liste_retour_enfants):
        if self.est_feuille():
            return

        if cote == Quadnoeud.Cote.NORD:
            noeud1 = self.nord_est
            noeud2 = self.nord_ouest
        elif cote == Quadnoeud.Cote.EST:
            noeud1 = self.nord_est
            noeud2 = self.sud_est
        elif cote == Quadnoeud.Cote.SUD:
            noeud1 = self.sud_est
            noeud2 = self.sud_ouest
        elif cote == Quadnoeud.Cote.OUEST:
            noeud1 = self.nord_ouest
            noeud2 = self.sud_ouest
        else:
            raise RuntimeError("Le côté passé n'est pas valide.")

        if noeud1.est_feuille():
            liste_retour_enfants.append(noeud1)
        else:
            noeud1._ajoute_enfants(cote, liste_retour_enfants)

        if noeud2.est_feuille():
            liste_retour_enfants.append(noeud2)
        else:
            noeud2._ajoute_enfants(cote, liste_retour_enfants)

    def _renvoie_voisin(self, cote, quadrant=None):
        if quadrant is None:
            if self._parent is not None and self._est_adjacent(cote, self._renvoie_quadrant()):
                voisin = self._parent._renvoie_voisin(cote)
            else:
                voisin = self._parent

            if voisin is not None and not voisin.est_feuille():
                return voisin.renvoie_enfant(self._renvoie_reflet(cote, self._renvoie_quadrant()))
            else:
                return voisin
        else:
            quadnoeud = self._renvoie_voisin(cote)

            if quadnoeud is None:
                return None

            while quadnoeud.est_feuille():
                quadnoeud = quadnoeud.renvoie_enfant(self._renvoie_reflet(cote, quadrant))

            return quadnoeud

    def _ajoute_voisins(self, cote, liste_retour_voisins):
        quadnoeud = self._renvoie_voisin(cote)

        if quadnoeud is not None:
            if quadnoeud.est_feuille():
                liste_retour_voisins.append(quadnoeud)
            else:
                quadnoeud._ajoute_enfants(self._renvoie_oppose(cote), liste_retour_voisins)

    def renvoie_voisins(self):
        voisins = list()
        self._ajoute_voisins(Quadnoeud.Cote.NORD, voisins)
        self._ajoute_voisins(Quadnoeud.Cote.SUD, voisins)
        self._ajoute_voisins(Quadnoeud.Cote.EST, voisins)
        self._ajoute_voisins(Quadnoeud.Cote.OUEST, voisins)
        return voisins

    def renvoie_largeur(self):
        return self.haut_droite.x - self.bas_gauche.x

    def renvoie_hauteur(self):
        return self.haut_droite.y - self.bas_gauche.y

    def renvoie_origine(self):
        return self.bas_gauche

    def est_feuille(self):
        return self._status != Quadnoeud.Etat.MIXTE

    def est_libre(self):
        return self._status == Quadnoeud.Etat.LIBRE

    def renvoie_distance(self, autre_quadnoeud):
        x1 = self.bas_gauche.x + self.renvoie_largeur() / 2.0
        y1 = self.bas_gauche.y + self.renvoie_hauteur() / 2.0

        x2 = autre_quadnoeud.bas_gauche.x + autre_quadnoeud.renvoie_largeur() / 2.0
        y2 = autre_quadnoeud.bas_gauche.y + autre_quadnoeud.renvoie_hauteur() / 2.0

        a = math.fabs(x1 - x2)
        b = math.fabs(y1 - y2)

        return math.sqrt(a ** 2 + b ** 2)

    def est_dedans(self, point):
        return (self.bas_gauche.x <= point.x <= self.haut_droite.x) \
            and (self.bas_gauche.y <= point.y <= self.haut_droite.y)
