from scipy.optimize import fsolve
import numpy

# Paramètres K_barre (rigidité motifs)
# Paramètres communs
Theta = 0.0757515 #Ratio fente/matériau
N_theta = 9 #Nombre de fentes angulaires
r_int = 20 #Rayon intérieur
ro = 250 #Rayon extérieur
n = 1 #Augmentation exponnentielle des delta_r

# Paramètres méthode N_r
N_r = 37 #Nombre de fentes radiales

# Paramètres méthode delta_x
delta_x = 0.0248497 #Ratio delta_r2/ro

# delta_r1 méthode delta_x
delta_r1 = 10 #Espacement rayon intérieur - première fente

#*Les codes pythons pour générer les motifs utilisent : automotique - N_r*

# Paramètres B (rigidité en flexion du matériau)
E = 1 #Module de Young du matériau
t = 0.5 #Épaisseur du matériau

#------------------------------------------------------------------------

# Décision de la méthode de calcul
print("Utilisation du N_r (r) ou du delta_x (x)?")
choix = input("N_r = r, delta_x = x : ")

# delta_r1 méthode N_r
if choix == "r":
    delta_r1 = r_int/ro
elif choix == "x":
    pass
else:
    print("Utilisation du N_r (r) ou du delta_x (x)?")
    choix = input("N_r = r, delta_x = x : ")

# Calcul de r1
r1= r_int+delta_r1

# Calcul de delta_r2 si méthode delta_x
delta_r2 = ro*delta_x

#Calcul de delta_x et delta_r2 si méthode N_r
def radialSlits(delta_r1, delta_r2, n, N_r):
    x = delta_r1 + delta_r2
    dx = delta_r2
    for i in range(N_r-1):
        dx = (1+dx)**n - 1
        x += dx
    return x

if choix == "r":
    func = lambda delta_r2: radialSlits(delta_r1, delta_r2, n, N_r) - 1
    delta_x = fsolve(func, 0.1)[0]
    delta_r2 = ro*delta_x

# Calcul de la série dans la formule de K_barre
j=0
rj=0
serie = 0

if choix == "x":
    while True:
        j+=1
        sommation=0

        # Calcul de delta_rj
        delta_rj = ro*((1+delta_r2/ro)**(n**j)-1)

        # Condition pour s'assurer de ne pas dépasser ro
        if ro-rj < delta_rj:
            print("N_r est égale à", j)
            break

        # Calcul de delta_xj
        delta_xj = delta_rj/ro

        # Calcul de la série pour rj
        for i in range (2, j+1):
            sommation += (1+delta_r2/ro)**(n**j)-1
        
        # Calcul de rj
        rj = ro*sommation + r1

        # Calcul de xj
        xj = rj/ro

        # Calcul de la série
        serie += xj**3/delta_xj

elif choix == "r":
    for j in range (1, N_r):
        sommation=0

        # Calcul de delta_rj
        delta_rj = ro*((1+delta_r2/ro)**(n**j)-1)

        # Calcul de delta_xj
        delta_xj = delta_rj/ro

        # Calcul de la série pour rj
        for i in range (2, j+1):
            sommation += (1+delta_r2/ro)**(n**j)-1
        
        # Calcul de rj
        rj = ro*sommation + r1

        # Calcul de xj
        xj = rj/ro

        # Calcul de la série
        serie += xj**3/delta_xj

# Calcul de K_barre, rigité du motif
K_barre = (24 / numpy.pi**3) * (N_theta**4) * serie**-1 * ((1 + Theta) / (1 - Theta))**3
print("K_barre est égale à", K_barre)

# Calcul de K_total
K = K_barre * (E*t**3/12) / ro**2
print("K_total est égale à", K)