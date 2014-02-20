#!/usr/bin/env python
# -*- coding: utf-8 -*-

# source : http://mathieuturcotte.ca/textes/quadtree/

from astar_noeud import *
from chemin_non_trouve_exception import CheminNonTrouveException
from modele.quadnoeud import Quadnoeud


class AStar(object):
    def __init__(self, quadnoeud_depart, quadnoeud_arrivee):
        self._quadnoeud_depart = quadnoeud_depart
        self._quadnoeud_arrivee = quadnoeud_arrivee
        self._liste_ouverte = list()
        self._liste_fermee = list()

    def _ajoute_liste_fermee(self, astar_noeud):
        self._liste_fermee.append(astar_noeud)
        try:
            self._liste_ouverte.remove(astar_noeud)
        except KeyError as e:
            print("Erreur _ajoute_liste_fermee : ", e)

    def _est_deja_present(self, quadnoeud, liste):
        for element in liste:
            if element.quadnoeud == quadnoeud:
                return True
        return False

    def _renvoie_astar_noeud(self, quadnoeud, liste):
        for element in liste:
            if element.quadnoeud == quadnoeud:
                return element
        return None

    def _ajoute_voisin(self, astar_noeud):
        voisins = astar_noeud.renvoie_voisins()
        foncteur_ordre_liste_ouverte = lambda x: x.cout_total
        for voisin in voisins:
            if not voisin.est_libre():
                continue

            if self._est_deja_present(voisin, self._liste_fermee):
                continue

            astar_noeud_liste_ouverte = self._renvoie_astar_noeud(voisin, self._liste_ouverte)

            if astar_noeud_liste_ouverte is not None:
                cout_chemin = astar_noeud.cout_chemin + astar_noeud.renvoie_distance_astar_noeud(
                    astar_noeud_liste_ouverte)

                # modification par une heuristique
                cout_chemin = self._renvoie_modifie_par_heuristique(astar_noeud, voisin, cout_chemin)

                if cout_chemin < astar_noeud_liste_ouverte.cout_chemin:
                    cout_estime = astar_noeud_liste_ouverte.cout_estime
                    astar_noeud_liste_ouverte.cout_chemin = cout_chemin
                    astar_noeud_liste_ouverte.cout_total = cout_estime + cout_chemin
                    astar_noeud_liste_ouverte.ancetre = astar_noeud
            else:
                cout_chemin = astar_noeud.cout_chemin + astar_noeud.renvoie_distance_quadnoeud(voisin)
                cout_estime = voisin.renvoie_distance(self._quadnoeud_arrivee)

                # modification par une heuristique
                cout_estime = self._renvoie_modifie_par_heuristique(astar_noeud, voisin, cout_estime)

                self._liste_ouverte.append(AStarNoeud(astar_noeud, voisin, cout_chemin, cout_estime))
                self._liste_ouverte.sort(key=foncteur_ordre_liste_ouverte, reverse=False)

    def _retrouve_chemin(self):
        chemin = list()
        courant_astar_noeud = self._renvoie_astar_noeud(self._quadnoeud_arrivee, self._liste_fermee)
        while courant_astar_noeud is not None:
            chemin.append(courant_astar_noeud.quadnoeud)
            courant_astar_noeud = courant_astar_noeud.ancetre
        chemin.reverse()
        return chemin

    def renvoie_chemin(self):
        courant = AStarNoeud(None, self._quadnoeud_depart, 0,
                             self._quadnoeud_depart.renvoie_distance(self._quadnoeud_arrivee))
        self._liste_ouverte.append(courant)
        self._ajoute_liste_fermee(courant)
        self._ajoute_voisin(courant)

        while not (len(self._liste_ouverte) == 0) and not (courant.quadnoeud == self._quadnoeud_arrivee):
            courant = self._liste_ouverte[0]
            self._ajoute_liste_fermee(courant)
            self._ajoute_voisin(courant)

        if courant.quadnoeud == self._quadnoeud_arrivee:
            return self._retrouve_chemin()
        else:
            raise CheminNonTrouveException("Le chemin n'a pas pu être trouvé.")

    def _est_correctement_oppose(self, astar_quadnoeud_courant, cote):
        if astar_quadnoeud_courant.ancetre is None:
            return True
        if astar_quadnoeud_courant.quadnoeud._renvoie_voisin(cote) is astar_quadnoeud_courant.ancetre.quadnoeud:
            return True
        return False

    def _est_correctement_aligne(self, quadnoeud_suivant, astar_quadnoeud_precedent):
        if quadnoeud_suivant.haut_droite.y >= astar_quadnoeud_precedent.quadnoeud.haut_droite.y and \
                        quadnoeud_suivant.bas_gauche.y <= astar_quadnoeud_precedent.quadnoeud.bas_gauche.y:
            return True
        elif quadnoeud_suivant.haut_droite.x >= astar_quadnoeud_precedent.quadnoeud.haut_droite.x and \
                        quadnoeud_suivant.bas_gauche.x <= astar_quadnoeud_precedent.quadnoeud.bas_gauche.x:
            return True
        elif astar_quadnoeud_precedent.quadnoeud.haut_droite.y >= quadnoeud_suivant.haut_droite.y and \
                        astar_quadnoeud_precedent.quadnoeud.bas_gauche.y <= quadnoeud_suivant.bas_gauche.y:
            return True
        elif astar_quadnoeud_precedent.quadnoeud.haut_droite.x >= quadnoeud_suivant.haut_droite.x and \
                        astar_quadnoeud_precedent.quadnoeud.bas_gauche.x <= quadnoeud_suivant.bas_gauche.x:
            return True
        else:
            return False

    def _renvoie_modifie_par_heuristique(self, astar_quadnoeud_courant, quadnoeud_suivant, cout_estime):
        cote_oppose = None
        if astar_quadnoeud_courant.quadnoeud._renvoie_voisin(Quadnoeud.Cote.SUD) is quadnoeud_suivant:
            cote_oppose = Quadnoeud.Cote.NORD
        elif astar_quadnoeud_courant.quadnoeud._renvoie_voisin(Quadnoeud.Cote.OUEST) is quadnoeud_suivant:
            cote_oppose = Quadnoeud.Cote.EST
        elif astar_quadnoeud_courant.quadnoeud._renvoie_voisin(Quadnoeud.Cote.NORD) is quadnoeud_suivant:
            cote_oppose = Quadnoeud.Cote.SUD
        elif astar_quadnoeud_courant.quadnoeud._renvoie_voisin(Quadnoeud.Cote.EST) is quadnoeud_suivant:
            cote_oppose = Quadnoeud.Cote.OUEST
        astar_quadnoeud_precedent = astar_quadnoeud_courant.ancetre
        for _ in self._liste_fermee:
            if astar_quadnoeud_precedent is None or cote_oppose is None:
                break
            if self._est_correctement_aligne(quadnoeud_suivant, astar_quadnoeud_precedent) is False and \
                            self._est_correctement_oppose(astar_quadnoeud_precedent, cote_oppose) is False:
                cout_estime *= 2
                break
            if self._est_correctement_oppose(astar_quadnoeud_precedent, cote_oppose) is False:
                cout_estime *= 2
                break
                pass
            astar_quadnoeud_precedent = astar_quadnoeud_precedent.ancetre
        return cout_estime
