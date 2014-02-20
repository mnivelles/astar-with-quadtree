#!/usr/bin/env python
# -*- coding: utf-8 -*-

class AStarNoeud(object):
    def __init__(self, ancetre, quadnoeud, cout_chemin, cout_estime):
        self.ancetre = ancetre
        self.quadnoeud = quadnoeud
        self.cout_total = cout_chemin + cout_estime
        self.cout_chemin = cout_chemin
        self.cout_estime = cout_estime

    def __str__(self):
        return "[" + str(self.quadnoeud.bas_gauche) + "," + str(self.quadnoeud.haut_droite) + "]"

    def __repr__(self):
        return "[" + str(self.quadnoeud.bas_gauche) + "," + str(self.quadnoeud.haut_droite) + "]"

    def renvoie_voisins(self):
        return self.quadnoeud.renvoie_voisins()

    def renvoie_distance_astar_noeud(self, autre_astar_noeud):
        return self.quadnoeud.renvoie_distance(autre_astar_noeud.quadnoeud)

    def renvoie_distance_quadnoeud(self, autre_quadnoeud):
        return self.quadnoeud.renvoie_distance(autre_quadnoeud)