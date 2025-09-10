from sympy import symbols, Eq, solve, pi, Sum
from scipy.optimize import fsolve
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from itertools import product


# Paramètres généraux
r_int = 6 #Rayon intérieur
ro = 60 #Rayon extérieur
delta_r1 = 0 #Si la première distance est différente que delta_r2, sinon mettre 0
delta_rmin = 1.35 #Distance minimale pour pas que le matériau se brise

# Paramètres K_barre, rigidité motif (mettre none si inconnu)
Thetas = np.linspace(0, 1, 30)[1:-1] #Ratio matériau/fente
N_thetas = np.arange(1, 6) #Nombre de fentes angulaires
N_rs = np.arange(1, 51) #Nombre de fentes radiales
K_barre = None #Rigité motif

#------------------------------------------------------------------------

# Calcul de r1
r1= r_int+delta_r1

# Fonction pour trouver inconnu
def trouver_K_barre(Theta, N_theta, serie):

    # Résolution de l'équation de K_barre pour trouver N_r manquante
    K_barre = symbols('K_barre')
    eq = Eq((24 / pi**3) * (N_theta**4) * serie**-1 * ((1 + Theta) / (1 - Theta))**3, K_barre)
    solution = solve(eq, K_barre)
    
    return solution[0] 

# Variables pour stocker les résultats
N_theta_values = []
Theta_values = []
Kl_values = []
size_fente_values = []
N_r_values = []

for N_r in N_rs:
    for Theta in Thetas:
        for N_theta in N_thetas:
            
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
            xj = rj / ro 
            delta_xj = delta_r2 / ro

            # Calcul de la serie
            equation = Eq(Sum(xj**3 / delta_xj, (j, 1, N_r)).doit() - serie -(r1/ro)**3/(r1/ro), 0)
            serie = solve(equation, serie)[0]

            # Calcul de K_barre
            K_barre = trouver_K_barre(Theta, N_theta, serie)

            # Calcul de delta_r2 et delta_r1
            delta_r2 = (ro - r1) / N_r 
            delta_r1 = delta_r2

             # Critère K_barre
            if K_barre <= 0:
                continue
            if K_barre > 23:
                continue

            # Critère Theta et N_theta
            if N_theta > (2*np.pi*r1*Theta)/(delta_rmin*(1+Theta)):
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
            l = np.pi * ((1 - Theta) / (1 + Theta)) / N_theta * seriel

            # Calcul du facteur K_barre*l
            Kl = K_barre

            # Taille des fentes
            size_fente = (1 + Theta) / N_theta  / Theta

            # Stocker les valeurs
            N_theta_values.append(N_theta)
            Theta_values.append(Theta)
            Kl_values.append(Kl)
            size_fente_values.append(size_fente)
            N_r_values.append(N_r)

# Normaliser les valeurs de Kl
norm_Kl = np.array(Kl_values) / np.max(Kl_values)

# Création du scatter 3D
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

# Afficher les points avec couleur basée sur norm_Kl
scatter = ax.scatter(
    Theta_values,
    N_theta_values,
    N_r_values,
    c=norm_Kl,  # Couleurs basées sur Kl normalisé
    cmap=plt.cm.YlOrRd,  # Palette de couleurs
    s=30,  # Taille des points
    alpha=0.8  # Transparence
)

# Ajouter une barre de couleur
fig.colorbar(scatter, ax=ax, shrink=0.6, aspect=10, label='Valeur de k')

# Ajouter des titres et labels
ax.set_title('k selon les paramètres')
ax.set_xlabel('Theta')
ax.set_ylabel('N_theta')
ax.set_zlabel('N_r')

# Afficher le graphique
plt.show()

# Affichage du nuage de points avec les couleurs basées sur K_l
plt.scatter(size_fente_values, N_r_values, c=norm_Kl, cmap='YlOrRd')
plt.title('Nuage de Points de kl en fonction de N_r et size_fente')
plt.xlabel('size_fente')
plt.ylabel('N_r')
plt.colorbar(label='Valeur de Kl')  # Ajouter une barre de couleur
plt.show()