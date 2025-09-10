# Code pour calculer K_barre avec la formule simplifiée, potentiellement mauvaise
import numpy

# Paramètres
Theta = 0.0757515
N_theta = 9
N_r = 35

# Calcul du K_barre
K_barre = (24 / numpy.pi**3) * (N_theta**4) * (N_r**6*(N_r+1)**2)**-1 * ((1 + Theta) / (1 - Theta))**3
print(K_barre)