#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import turtle
import re

#Constantes
LARGEUR, HAUTEUR = 1640, 1480
POS_X = POS_Y = 50
NOM_IMAGE = "Turtle resolver"

def recapitule():
    """Fonction pour recapituler la largeur, la hauteur,
    la couleur et l'image de la fenetre turtle"""
    print("largeur : {} px".format(turtle.window_width()))
    print("hauteur : {} px".format(turtle.window_height()))
  
if __name__ == "__main__":
    #On ouvre la fenetre en choisissant dimensions et positions
    turtle.setup(LARGEUR, HAUTEUR, POS_X, POS_Y)
    #On recapitule la configuration de la fenetre hormis la position
    recapitule()
    #On ferme la fenetre s'il y a un clique gauche

    with open('input') as f:
        lines = f.readlines()
    for line in lines:
        match_avance = re.search(r'Avance', line)
        match_recule = re.search(r'Recule', line)
        match_tourne_droite = re.search(r'Tourne droite de', line)
        match_tourne_gauche = re.search(r'Tourne gauche de', line)
        if match_avance:
            advance = line.split(' ')
            print "avance", advance[1]
            turtle.fd(float(advance[1]))
        elif match_recule:
            recule = line.split(' ')
            print "recule", recule[1]
            turtle.bk(float(recule[1]))
        elif match_tourne_droite:
            Tourne_droite = line.split(' ')
            print "Tourne_droite", Tourne_droite[3]
            turtle.right(float(Tourne_droite[3]))
        elif match_tourne_gauche:
            Tourne_gauche = line.split(' ')
            print "Tourne_gauche", Tourne_gauche[3]
            turtle.left(float(Tourne_gauche[3]))

    turtle.exitonclick()