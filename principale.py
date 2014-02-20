#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import math

from algorithme.astar import AStar
from algorithme.chemin_non_trouve_exception import CheminNonTrouveException
from modele.obstacle import Obstacle
from modele.quadtree import Quadtree
from modele.quadnoeud_obstrue_exception import QuadnoeudObstrueException
from modele.point import Point
from dessin_quadtree import *

def _affiche_infos(resolution, taille, temps):
    print("Trouver avec une résolution de " + str(resolution) + " un chemin de taille " +\
          str(taille) + " en " + str(temps) + " secondes.")

def _affiche_resultat_recherche_chemin(point_debut, point_fin, marge_securite, tps1):
    obstacles2 = list()
    LARGEUR_TABLE_JEU_MM = 2230
    HAUTEUR_TABLE_JEU_MM = 1140
    DIAMETRE_OBSTACLE_MM = 125
    taille_robot = math.ceil(197 * marge_securite + 197)
    taille_diagonale_robot_mm = math.ceil(taille_robot * math.sqrt(2) / 2.0)

    # Bords de la table
    obstacles2.append(Obstacle(Point(0, 0),
                               Point(taille_diagonale_robot_mm, LARGEUR_TABLE_JEU_MM)))
    obstacles2.append(Obstacle(Point(taille_diagonale_robot_mm, 0),
                               Point(HAUTEUR_TABLE_JEU_MM - taille_diagonale_robot_mm, taille_diagonale_robot_mm)))
    obstacles2.append(Obstacle(Point(taille_diagonale_robot_mm, LARGEUR_TABLE_JEU_MM - taille_diagonale_robot_mm),
                               Point(HAUTEUR_TABLE_JEU_MM - taille_diagonale_robot_mm, LARGEUR_TABLE_JEU_MM)))
    obstacles2.append(Obstacle(Point(HAUTEUR_TABLE_JEU_MM - taille_diagonale_robot_mm, 0),
                               Point(HAUTEUR_TABLE_JEU_MM, LARGEUR_TABLE_JEU_MM)))
    # Vrais positions_obstacles
    pos_obs1 = Point(620, 1310)
    pos_obs2 = Point(820, 740)
    pos_obs1 = Point(770, 740)
    pos_obs2 = Point(538, 1790)
    pos_obs1 = Point(860, 1240)
    pos_obs2 = Point(430, 1400)
    pos_obs1 = Point(832.460040536, 1690.910001)
    pos_obs2 = Point(303.610754033, 1166.21608976)
    taille_demi_obstacle = math.ceil((DIAMETRE_OBSTACLE_MM + 2 * taille_diagonale_robot_mm) / 2.0)
    obstacles2.append(Obstacle(Point(pos_obs1.x - taille_demi_obstacle, pos_obs1.y - taille_demi_obstacle),
                               Point(pos_obs1.x + taille_demi_obstacle, pos_obs1.y + taille_demi_obstacle)))
    obstacles2.append(Obstacle(Point(pos_obs2.x - taille_demi_obstacle, pos_obs2.y - taille_demi_obstacle),
                               Point(pos_obs2.x + taille_demi_obstacle, pos_obs2.y + taille_demi_obstacle)))

    debut = point_debut
    fin = point_fin
    try:
        resolution = 19 # 19 > LARGEUR_TABLE_JEU_MM/128
        quadtree2 = Quadtree(obstacles2, LARGEUR_TABLE_JEU_MM, resolution)

        debut_trouve = quadtree2.trouve_noeud(debut)
        fin_trouve = quadtree2.trouve_noeud(fin)

        astar2 = AStar(debut_trouve, fin_trouve)
        chemin2 = astar2.renvoie_chemin()
        tps2 = time.time()
        _affiche_infos(resolution, str(len(chemin2)), str(tps2 - tps1))
        affiche_quadtree(obstacles2, quadtree2._racine, chemin2, LARGEUR_TABLE_JEU_MM)
    except CheminNonTrouveException:
        try:
            resolution = 10 # 10 > LARGEUR_TABLE_JEU_MM/256
            quadtree2 = Quadtree(obstacles2, LARGEUR_TABLE_JEU_MM, resolution)

            debut_trouve = quadtree2.trouve_noeud(debut)
            fin_trouve = quadtree2.trouve_noeud(fin)

            astar2 = AStar(debut_trouve, fin_trouve)
            chemin2 = astar2.renvoie_chemin()
            tps2 = time.time()
            _affiche_infos(resolution, str(len(chemin2)), str(tps2 - tps1))
            affiche_quadtree(obstacles2, quadtree2._racine, chemin2, LARGEUR_TABLE_JEU_MM)
        except CheminNonTrouveException:
            try:
                resolution = 5 # 5 > LARGEUR_TABLE_JEU_MM/512
                quadtree2 = Quadtree(obstacles2, LARGEUR_TABLE_JEU_MM, resolution)

                debut_trouve = quadtree2.trouve_noeud(debut)
                fin_trouve = quadtree2.trouve_noeud(fin)

                astar2 = AStar(debut_trouve, fin_trouve)
                chemin2 = astar2.renvoie_chemin()
                tps2 = time.time()
                _affiche_infos(resolution, str(len(chemin2)), str(tps2 - tps1))
                affiche_quadtree(obstacles2, quadtree2._racine, chemin2, LARGEUR_TABLE_JEU_MM)
            except CheminNonTrouveException:
                try:
                    resolution = 3 # 3 > 22330/512
                    quadtree2 = Quadtree(obstacles2, LARGEUR_TABLE_JEU_MM, resolution)              

                    debut_trouve = quadtree2.trouve_noeud(debut)
                    fin_trouve = quadtree2.trouve_noeud(fin)

                    astar2 = AStar(debut_trouve, fin_trouve)
                    chemin2 = astar2.renvoie_chemin()
                    tps2 = time.time()
                    _affiche_infos(resolution, str(len(chemin2)), str(tps2 - tps1))
                    affiche_quadtree(obstacles2, quadtree2._racine, chemin2, LARGEUR_TABLE_JEU_MM)
                except CheminNonTrouveException:
                    resolution = 1
                    quadtree2 = Quadtree(obstacles2, LARGEUR_TABLE_JEU_MM, resolution)

                    debut_trouve = quadtree2.trouve_noeud(debut)
                    fin_trouve = quadtree2.trouve_noeud(fin)

                    astar2 = AStar(debut_trouve, fin_trouve)
                    chemin2 = astar2.renvoie_chemin()
                    tps2 = time.time()
                    _affiche_infos(resolution, str(len(chemin2)), str(tps2 - tps1))
                    affiche_quadtree(obstacles2, quadtree2._racine, chemin2, LARGEUR_TABLE_JEU_MM)


def affiche_recherche_chemin(point_debut, point_fin):
    """
     Faire ces différents essais avec des marges différentes permettent de proposé des parcours s'éloignant
     le plus possible des bords et des obstacles
    """
    try:
        tps1 = time.time()
        print("Marge : 10%")
        _affiche_resultat_recherche_chemin(point_debut, point_fin, 0.1, tps1)
    except QuadnoeudObstrueException:
        try:
            print("Marge : 5%")
            _affiche_resultat_recherche_chemin(point_debut, point_fin, 0.05, tps1)
        except QuadnoeudObstrueException:
            try:
                print("Marge : 0%")
                _affiche_resultat_recherche_chemin(point_debut, point_fin, 0.0, tps1)
            except QuadnoeudObstrueException as e:
                print("La position donnée n'est pas correcte." + str(e))


if __name__ == "__main__":
    # version grand quadtree mm
    print("\n### Version avec grand quadtree avec précision au mm près ###")

    debut = Point(928, 158)
    fin = Point(748, 1910)

    affiche_recherche_chemin(debut, fin)
