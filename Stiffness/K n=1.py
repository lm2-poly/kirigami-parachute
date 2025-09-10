from sympy import symbols, Eq, solve, pi, Sum
from scipy.optimize import fsolve
import numpy


# Paramètres grandeurs
r_int = 21.4 #Rayon intérieur du trou pour le payload
ro = 300 #Rayon extérieur
delta_r1 = 10 #Si la première distance est différente que delta_r2, sinon mettre 0
delta_rmin = 1.35 #Distance minimale pour pas que le matériau se brise

# Paramètres motifs (mettre none si inconnu)
Theta = 0.2 #Ratio matériau/fente
N_theta = 14 #Nombre de fentes angulaires
N_r = 114 #Nombre de fentes radiales
K_barre = None #Rigité motif

# Paramètres du matériau
E_young = 4E9 #Module de Young du matériau
t = 311E-6 #Épaisseur du matériau

#------------------------------------------------------------------------

# Calcul de r1
r1= r_int+delta_r1

# Fonction pour trouver inconnu
def trouver_inconnu(delta_r1, r1, ro, Theta, N_theta, N_r, K_barre):
    # Calculs serie si N_r connu

    if N_r != None:
        
        # Calcul de delta_r2
        delta_r2 = (ro - r1) / N_r
        
        # Calcul de delta_r1
        if delta_r1 == 0:
            delta_r1=delta_r2

        # Calcul de la série dans la formule de K_barre
        serie = 0
        for j in range (1, N_r+1):
            
            # Calcul de rj
            rj = delta_r2*(j-1) + r1

            # Calcul de rj_bar
            rj_bar = rj + delta_r2/2

            # Calcul de xj_bar
            xj_bar = rj_bar/ro

            # Calcul de la série
            if j == 1 :
                delta_xj = delta_r1/ro
            else:
                delta_xj = delta_r2/ro

            serie += xj_bar**3/delta_xj
    else:
        serie = None

    # Résolution de l'équation de K_barre pour trouver la variable manquante
    def solve_equation(equation, **kwargs):
        variables = {k: symbols(k) for k in kwargs.keys()}
        known_values = {variables[k]: v for k, v in kwargs.items() if v is not None}
        unknown_var = [variables[k] for k, v in kwargs.items() if v is None][0]

        solution = solve(equation.subs(known_values), unknown_var)
        return unknown_var, solution[0]

    N_theta_res, Theta_res, serie_res, K_barre_res = symbols('N_theta_res Theta_res serie_res K_barre_res') 

    eq = Eq((24 / pi**3) * (N_theta_res**4) * serie_res**-1 * ((1 + Theta_res) / (1 - Theta_res))**3, K_barre_res)

    unknown, value = solve_equation(eq, N_theta_res=N_theta, K_barre_res=K_barre, serie_res=serie, Theta_res=Theta)
    
    return unknown, value

unknown, value = trouver_inconnu(delta_r1, r1, ro, Theta, N_theta, N_r, K_barre)

# Trouver N_r si inconnu est serie
if unknown.name == "serie_res":
    unknown = "N_r"

    # Définir les variables symboliques
    N_r = symbols('N_r', positive=True, real=True)
    j = symbols('j', integer=True)

    # Calcul de delta_r2
    delta_r2 = (ro - r1) / N_r  

    # Calcul de delta_r1
    if delta_r1 == 0:
        delta_r1=delta_r2

    # Calcul de rj, rj_bar, xj_bar et delta_xj
    rj = delta_r2 * (j-1) + r1  
    rj_bar = rj + delta_r2/2
    xj_bar = rj_bar/ro
    delta_xj = delta_r2/ro

    # Résolution de la serie pour trouver N_r
    equation = Eq(Sum(xj_bar**3 / delta_xj, (j, 1, N_r)).doit() - value - ((r1 + delta_r2/2)/ro)**3/(delta_r1/ro), 0)
    value = solve(equation, N_r)[0]
else:
    unknown = unknown.name.replace("_res", "")

print("La variable inconnue est: ", unknown)

# Pour recalculer Theta afin d'arrondir N_r ou N_theta
if unknown == "N_r":
    choix = input("Voulez-vous recalculer Theta pour arrondir N_r? (oui/non) ")
    while True:
        if choix == "oui":
            N_r = round(value)
            Theta = None
            unknown, Theta = trouver_inconnu(delta_r1, r1, ro, Theta, N_theta, N_r, K_barre)
            print(f"Les paramètres sont: N_r = {N_r} ; N_theta = {N_theta} ; Theta = {Theta}")
            break
        elif choix == "non":
            N_r = value
            print(f"Les paramètres sont: N_r = {N_r} ; N_theta = {N_theta} ; Theta = {Theta}")
            break
        else:
            choix = input("Voulez-vous recalculer Theta pour arrondir N_r? (oui/non) ")

elif unknown == "N_theta":
    choix = input("Voulez-vous recalculer Theta pour arrondir N_theta? (oui/non) ")
    while True:
        if choix == "oui":
            N_theta = round(-value)
            Theta = None
            unknown, Theta = trouver_inconnu(delta_r1, r1, ro, Theta, N_theta, N_r, K_barre)
            print(f"Les paramètres sont: N_r = {N_r} ; N_theta = {N_theta} ; Theta = {Theta}")
            break

        elif choix == "non":
            N_theta = -value
            print(f"Les paramètres sont: N_r = {N_r} ; N_theta = {N_theta} ; Theta = {Theta}")
            break
        else:
            choix = input("Voulez-vous recalculer Theta pour arrondir N_theta? (oui/non) ")

elif unknown == "K_barre":
        K_barre = value
        print(f"Les paramètres sont: N_r = {N_r} ; N_theta = {N_theta} ; Theta = {Theta}")

elif unknown == "Theta":
        Theta = value
        print(f"Les paramètres sont: N_r = {N_r} ; N_theta = {N_theta} ; Theta = {Theta}")

print("La valeur de K_barre est: ", K_barre) 

# Calcul de K_total
K_total = K_barre * (E_young * t**3 / 12) / ro**2
print("La valeur de K_total est: ", K_total)

# Calcul de delta_r2
delta_r2 = (ro - r1) / N_r 
print("La valeur de delta_r2 est: ", delta_r2)

# # Calcul de la série dans la formule de l
# seriel = 0
# for j in range (1, round(N_r+1)):
#     # Calcul de rj
#     rj = delta_r2*(j-1) + r1

#     # Calcul de rj_bar
#     rj_bar = rj + delta_r2/2

#     # Calcul de xj_bar
#     xj_bar = rj_bar/ro

#     # Calcul de la série
#     seriel += xj_bar     

# # Calcul de l
# l = numpy.pi * ((1 - Theta) / (1 + Theta)) * seriel / N_theta 
# print("La valeur de l est: ", l)
# Le = ro * l
# print("La valeur de Le est: ", Le)

# # Calcul du facteur K_barre*l
# Kl = K_barre * l
# print("La valeur de Kl est: ", Kl)

# Critère K_barre
if K_barre <= 28:
    print("Le critère K_barre est respecté")
else:
    print("Le critère K_barre n'est pas respecté")

# Critère Theta et N_theta
if N_theta <= (2*numpy.pi*r1*Theta)/(delta_rmin*(1+Theta)) and N_theta > 2 and Theta < 1 and Theta > 0:
    print("Le critère Theta et N_theta est respecté")
else:
    print("Le critère Theta et N_theta n'est pas respecté")

# Critère N_r
if (ro - r1) / N_r < delta_rmin:
    print("Le critère N-r n'est pas respecté")
else:
    print("Le critère N_r est respecté")