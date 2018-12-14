from math import exp, cos
Salut RO
from numpy import *
from scipy import *

sigma = 5.67036713 * 10 ** (-8)
chaleur_latente_eau = 2257
flux_direct_test = 900
capacite_calo_air = 1000
enthalpie_vap_eau = 2264.76
pression_atmo = 101325
R = 8.31
temp_evap = 373.15
masse_moleculaire_eau = 18.01528
alpha = 0

"""Module environement """


def pression_saturation(temperature_ambiante):
    p_sat = pression_atmo * exp(-enthalpie_vap_eau / R * (1 / temperature_ambiante - 1 / temp_evap))
    return p_sat


def humidite_absolue(temperature_ambiante):
    Y_abs = (pression_saturation(temperaure_ambiante) * masse_moleculaire_eau) / temperature_ambiante * R
    return Y_abs


def rayonnement_indirect(humidite_relative_ambiante, temperature_ambiante):
    temperature_rosee = ((humidite_relative_ambiante * 100) ** (1 / 8)) * (
            112 + 0.9 * temperature_ambiante) + 0.1 * temperature_ambiante - 112
    temperature_ciel = temperature_ambiante * (
            (0.711 + 0.0056 * temperature_rosee + 7.3 * temperature_rosee ** 2 * 10 ** (-5)) ** (1 / 4))
    rayonnements_i = sigma * (temperature_ciel ** 4)
    return rayonnements_i


def rayonnement_direct():
    Fd = (R - rayonnement_indirect(humidité_relative_ambiante, temperaure_ambiante)) / cos(alpha)
    return Fd


"""Module Ventilation"""


def vitesse_evaporation(kg_de_matiere_a_secher, humidite_initial_du_produit, humidite_final_du_produit,
                        temps_de_sechage):
    vitesse_evaporation_h2o = (humidite_initial_du_produit - humidite_final_du_produit) * kg_de_matiere_a_secher / (
            1 + humidite_initial_du_produit) * 1 / temps_de_sechage
    return vitesse_evaporation_h2o


def ventilation(humidite_relative_ambiante, humidite_relative_finale):
    debit = vitesse_evaporation(kg_de_matiere_à_sécher, humidité_initiale_du_produit, humidité_finale_du_produit,
                                temps_de_séchage) / (humidite_relative_finale - humidite_relative_ambiante)
    return debit


"""Module Effet de serre"""

def puissance():
    puissance_total = ventilation(humidité_relative_ambiante, humidité_relative_finale) * capacite_calo_air * (
            T - temperaure_ambiante) + chaleur_latente_eau * vitesse_evaporation(kg_de_matiere_à_sécher,
                                                                                 humidité_initiale_du_produit,
                                                                                 humidité_finale_du_produit,
                                                                                 temps_de_séchage)
    return puissance_total




def effet_de_serre(z):
    k = 10
    T_amb = 65
    sigma = 5.67 * (10 ** (-8))
    Fi, Fd = rayonnement_indirect(humidite_relative_ambiante, temperaure_ambiante)

    P = z[0]
    T_P = z[1]
    T_S = z[2]
    F_P = z[3]
    F_S = z[4]

    f = [0] * 5

    f[0] = k * (T_P - T_amb) + k * (T_S - T_amb) - P
    f[1] = (sigma * (T_P) ** 4) - F_P
    f[2] = (sigma * (T_S) ** 4) - F_S
    f[3] = P + F_P - F_i - F_d
    f[4] = F_S + (k * (T_S - T_amb)) - (F_d + F_P)

    print(f)  # Debug

    return f


zGuess = [100, 30, 30, 50, 60]
z = fsolve(effet_de_serre, zGuess)
print(effet_de_serre([0, 0, 0, 0, 0]))

def convection():
    mu = 1.8 * 10 ** (-5)  # viscosité dynamique
    rho = 1.225  # masse volumique varie en fct de la Temp
    U =  # vitesse de l'air
    c = 1004  # capacité thermique massique J/Kg K
    v =  # viscosité cinématique
    lamb = 0.026  # conductivité thermique [W/mK]

    Reynolds = rho * abs(U) * l / mu

    Nu_naturelle = 0.5 * Reynolds ** (1 / 4)
    a = lamb / rho.c  # diffusivité thermique 20*10**(-6) air à 20°C m²/s
    Pr = v / a  # nombre Prandtl
    Nu_interne = 0.023 * Pr ** (1 / 3) * Reynolds ** (4 / 5)
    Nu = (Nu_naturelle ** 3 + Nu_interne ** 3) ** (1 / 3)
    k_fluid = 101000  # pa de l'air module d'elasticité isostatique
    h = Nu * k_fluid / L
    return h


"""Code Principal"""

kg_de_matiere_à_sécher = float(input("Kg de matière à sécher (Kg):  "))
humidité_initiale_du_produit = float(input("Humidité initiale du produit (kgH2O/kg produit sec) : "))
humidité_finale_du_produit = float(input("Humidité finale du produit (kgH2O/kg produit sec) : "))
temperaure_ambiante = float(input("Tempéraure ambiante (°C) : "))
T = float(input("Température maximum souhaitée (°C): "))
humidité_relative_ambiante = float(input("Humidité relative de l'air au moment du séchage (%) : "))
humidité_relative_finale = float(input("Humidité relative finale de l'air souhaitée (%) : "))
temps_de_séchage = float(input("Temps de séchage (Heure) : "))
flux_total = float(input("Rayonnement Total (W/m²) : "))
