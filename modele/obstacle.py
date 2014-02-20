#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Obstacle(object):
    def __init__(self, bas_gauche, haut_droite):
        self.bas_gauche = bas_gauche
        self.haut_droite = haut_droite

    def intersecte(self, bas_gauche, haut_droite):
        # TODO Partie à vérifier
        espace_x = self.bas_gauche.x < haut_droite.x and self.haut_droite.x > bas_gauche.x

        espace_y = self.bas_gauche.y < haut_droite.y and self.haut_droite.y > bas_gauche.y

        return espace_x and espace_y

    def obstrue(self, bas_gauche, haut_droite):
        # TODO Partie à vérifier
        obstruction_x = self.bas_gauche.x <= bas_gauche.x and self.haut_droite.x >= haut_droite.x

        obstruction_y = self.bas_gauche.y <= bas_gauche.y and self.haut_droite.y >= haut_droite.y

        return obstruction_x and obstruction_y

    def __repr__(self):
        return str(self.bas_gauche) + " " + str(self.haut_droite)