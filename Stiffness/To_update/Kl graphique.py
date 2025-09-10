from sympy import symbols, Eq, solve, pi, Sum
from scipy.optimize import fsolve
import numpy as np
import matplotlib.pyplot as plt


# Paramètres généraux
r_int = 22 #Rayon intérieur
ro = 200 #Rayon extérieur
delta_r1 = 10 #Si la première distance est différente que delta_r2, sinon mettre 0
delta_rmin = 1.35 #Distance minimale pour pas que le matériau se brise

# Paramètres K_barre, rigidité motif (mettre none si inconnu)
Thetas = np.linspace(0, 1, 70)[1:-1] #Ratio matériau/fente
N_thetas = np.arange(1, 7) #Nombre de fentes angulaires
N_r = None #Nombre de fentes radiales
K_barre = 23 #Rigité motif

#------------------------------------------------------------------------

# Calcul de r1
r1= r_int+delta_r1

# Fonction pour trouver inconnu
def trouver_N_r(Theta, N_theta, K_barre):

    # Résolution de l'équation de K_barre pour trouver N_r manquante
    serie = symbols('serie')
    eq = Eq((24 / pi**3) * (N_theta**4) * serie**-1 * ((1 + Theta) / (1 - Theta))**3, K_barre)
    solution = solve(eq, serie)
    
    return solution[0] 

def trouver_Theta(N_theta, serie, K_barre):

    # Résolution de l'équation de K_barre pour trouver Theta manquante
    Theta = symbols('Theta')
    eq = Eq((24 / pi**3) * (N_theta**4) * serie**-1 * ((1 + Theta) / (1 - Theta))**3, K_barre)
    solution = solve(eq, Theta)
    
    return solution[0] 

# Variables pour stocker les résultats
N_theta_values = []
Theta_values = []
Kl_values = []
size_fente_values = []

for Theta in Thetas:
    for N_theta in N_thetas:
        serie = trouver_N_r(Theta, N_theta, K_barre)

        # Définir les variables symboliques
        N_r = symbols('N_r', positive=True, real=True)
        j = symbols('j', integer=True)

        # Calcul de delta_r2
        delta_r2 = (ro - r1) / N_r  

        # Calcul de delta_r1
        if delta_r1 == 0:
            delta_r1=delta_r2

        # Calcul de rj, xj et delta_xj
        rj = delta_r2 * (j-1) + r1 
        rj_bar = rj + delta_r2/2
        xj_bar = rj_bar / ro 
        delta_xj = delta_r2 / ro

        equation = Eq(Sum(xj_bar**3 / delta_xj, (j, 1, N_r)).doit() - serie -((r1 + delta_r2/2)/ro)**3/(delta_r1/ro), 0)
        N_r = solve(equation, N_r)[0]

        # Arrondir N_r
        N_r = round(N_r)
        if N_r == 0:
            continue

        # Recalculer serie
        # Définir les variables symboliques
        serie = symbols('serie')
        j = symbols('j', integer=True)

        # Calcul de delta_r2
        delta_r2 = (ro - r1) / N_r  

        # Calcul de delta_r1
        if delta_r1 == 0:
            delta_r1=delta_r2

        # Calcul de rj, xj et delta_xj
        rj = delta_r2 * (j-1) + r1 
        rj_bar = rj + delta_r2/2
        xj_bar = rj_bar / ro 
        delta_xj = delta_r2 / ro

        equation = Eq(Sum(xj_bar**3 / delta_xj, (j, 1, N_r)).doit() - serie -((r1 + delta_r2/2)/ro)**3/(delta_r1/ro), 0)
        serie = solve(equation, serie)[0]

        # Trouver le nouveau Theta selon la nouvelle serie de N_r
        Thetavalue = trouver_Theta(N_theta, serie, K_barre)

        # Calcul de delta_r2 et delta_r1
        delta_r2 = (ro - r1) / N_r 
        delta_r1 = delta_r2

        # Critère Theta et N_theta
        if N_theta > (2*np.pi*r1*Thetavalue)/(delta_rmin*(1+Thetavalue)) or N_theta <=2 or Theta >= 1 or Theta<=0 :
            continue

        # Critère N_r
        if (ro - r1) / int(N_r) < delta_rmin:
            continue

        # Calcul de la série dans la formule de l
        seriel = r1/ro
        for j in range (2, round(N_r+1)):

            # Calcul de rj
            rj = delta_r2*(j-1) + r1

            # Calcul de xj
            xj = rj/ro

            # Calcul de la série
            seriel += xj
        
        # Calcul de l
        l = np.pi * ((1 - Thetavalue) / (1 + Thetavalue)) / N_theta * seriel

        # Calcul du facteur K_barre*l
        Kl = K_barre * l

        # Taille des fentes
        size_fente = 1 / (1 + Thetavalue) / N_theta 

        # Stocker les valeurs
        N_theta_values.append(N_theta)
        Theta_values.append(Thetavalue)
        Kl_values.append(Kl)
        size_fente_values.append(size_fente)

# Normaliser les valeurs de K_l pour utiliser dans les couleurs
norm_Kl = np.array(Kl_values) / np.max(Kl_values)

# Affichage du nuage de points avec les couleurs basées sur size_fente
plt.scatter(N_theta_values, Theta_values, c=size_fente_values, cmap='YlOrRd')
plt.title('Nuage de Points de N_theta en fonction de Theta')
plt.xlabel('N_theta')
plt.ylabel('Theta')
plt.colorbar(label='Taille des fentes')  # Ajouter une barre de couleur
plt.show()
 
# # Graphique Kl en fonction de la taille des fentes
# plt.scatter(size_fente_values, norm_Kl)
# plt.title('Kl en fonction de la taille des fentes')
# plt.xlabel('Taille des fentes')
# plt.ylabel('Kl')
# plt.show()

# # Graphique taille en fonction de Ntheta
# plt.scatter(N_theta_values, size_fente_values)
# plt.title('Taille des fentes en fonction de N_theta')
# plt.xlabel('N_theta')
# plt.ylabel('Taille des fentes')
# plt.show()