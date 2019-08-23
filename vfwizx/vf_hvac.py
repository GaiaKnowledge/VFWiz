"""
The MATLAB (2016) model executes an iterative process to simultaneously solve (Eqs. 4–7), processing the net PAR flux density,
the sur- face and aerodynamic resistances as outlined above (Eqs. 8–10).

The iterative process is based on the aforementioned equations and is performed in a continuous loop. For each set interval of Ta,
the model calculates the corresponding Ts at which the energy balance (Rnet– H–λE) is closest to zero. The model utilises a
continuous loop to ap- proach this value at the set discretisation and consequently indexes the value closest to zero.
Finally, the model lists the different variables congruent with this zero energy balance, in particular the quantity of the 
sensible (H) and latent (λE) heat exchange.


REM:
https://www.engineeringtoolbox.com/relative-humidity-air-d_687.html
Relative humidity can also be expressed as the ratio of the vapor density of the air - 
to the saturation vapor density at the the actual dry bulb temperature.

relative_humidity = vapor_density / saturation_vapor_density

http://hyperphysics.phy-astr.gsu.edu/hbase/Kinetic/watvap.html
saturation_vapor_density = 618 g/m-3 at 20C


https://appgeodb.nancy.inra.fr/biljou/pdf/Allen_FAO1998.pdf
http://www.fao.org/3/X0490E/x0490e0k.htm

"""
import math
from constants import DENSITY_OF_AIR, HEAT_CAPACITY_OF_AIR, LATENT_HEAT_WATER, PSYCHOMETRIC_CONSTANT


# Calculation-specific constants
LAI = 3 # their value 3.1.3
CULTIVATION_AREA_COVERAGE = 0.9 # their value 3.1.1
REFLECTION_COEFFICIENT = 0.05 # Luuk Gaamans personal communication

VAPOUR_RESISTANCE = 200 # air circulation off
VAPOUR_RESISTANCE = 100 # air circulation on


def calc_vapour_pressure_air(temp_air, relative_humidty):
    """
    jmht added - seems to get different results from below
    From: http://www.fao.org/3/X0490E/x0490e0k.htm
    saturated_vapour_pressure = 0.6108 * math.exp((17.27 * temp_air) / (temp_air + 237.3))
    vapour_pressure = saturated_vapour_pressure * relative_humidty / 100
    Luuk Gaamans personal communication:
        Vapour concentration in the air = Relative humidity * saturated vapour concentration at air temperature (g m-3)
        Additional information:
        https://www.engineeringtoolbox.com/water-vapor-saturation-pressure-air-d_689.html
        https://www.engineeringtoolbox.com/relative-humidity-air-d_687.html
    """
    temp_air_k = temp_air + 273
    saturated_vapour_pressure = math.exp(77.345 + (0.0057 * temp_air_k) - (7235 / temp_air_k) ) / temp_air_k**8.2
    return saturated_vapour_pressure * relative_humidty / 100


def calc_vapour_pressure_surface(temp_air, temp_surface, vapour_pressure_air, relative_humidity):
    """
    7. Relation of χs to χa
    χs = χa + (ρa * cp) / λ * ε * (Ts - Ta)
    ε: vapour concentration (slope of the saturation function curve)
    
    
     epsilon relates the vapour_pressure to concentration. Explanation from Luuk:
        The simplest way to calculate it is epsilon = delta / gamma
        Where delta = 0.04145*exp(0.06088*T_s) (kPa/C)
        Gamma = 66.5  (Pascal/K) (gamma is a psychometric constant)
    """
    delta = 0.04145 * math.exp(0.06088 * temp_surface)
    epsilon = delta / PSYCHOMETRIC_CONSTANT
    return vapour_pressure_air + ((DENSITY_OF_AIR * HEAT_CAPACITY_OF_AIR) / LATENT_HEAT_WATER) * \
           epsilon * (temp_surface - temp_air)


def calc_net_radiation(ppfd):
    """
    8. Submodel for net radiation
    Rnet = (1 - ρr) * Ilighting * CAC
    ρr: reflection coefficient
    Ilighting: radiation
    CAC: cultivation area cover
    """
    # Guess from paper
    if ppfd == 600:
        lighting_radiation = 120
    elif ppfd == 140:
        lighting_radiation = 28
    else:
        assert False
    return (1 - REFLECTION_COEFFICIENT) * lighting_radiation * CULTIVATION_AREA_COVERAGE


def calc_latent_heat_flux(temp_air, temp_surface, relative_humidity, ppfd):
    """
    9. Submodel for stomatal resistance
    rs = 60 * (1500 + PPFD) / (220  + PPFD)
    PPFD: photosynthetic photon flux density (μmol/m2s)
    
    6. Latent Heat Flux λE - I think this is the evapotranspiration rate
    λE = LAI * λ * (χs - χa) / (rs + ra)
    λ: latent heat of the evaporation of water
    χs: vapour concentration at the transpiring surface
    χa:  vapour concentration in surrounding air
    rs: surface (or stomatal) resistance
    ra: aerodynamic resistance to vapour transfer
    """
    vapour_pressure_air = calc_vapour_pressure_air(temp_air, relative_humidity)
    vapour_pressure_surface = calc_vapour_pressure_surface(temp_air, temp_surface, vapour_pressure_air, relative_humidity)
    stomatal_resistance = 60 * (1500 + ppfd) / (220 + ppfd)
    
    return LAI * LATENT_HEAT_WATER * ( (vapour_pressure_surface - vapour_pressure_air) / (stomatal_resistance + VAPOUR_RESISTANCE) )


def calc_sensible_heat_exchange(temp_air, temp_surface):
    """
    5. Sensible heat exchange H
    H = LAI * ρa * cp * (Ts - Ta / ra)
    LAI: Leaf Area Index
    ρa: Density of air
    cp: Heat capacity of air - CHECK IS  ρacp in table
    Ts: temperature at the transpiring surface
    Ta: temperature of surrounding air
    ra: aerodynamic resistance to heat
    """
    return LAI * DENSITY_OF_AIR * HEAT_CAPACITY_OF_AIR * ((temp_surface - temp_air) / VAPOUR_RESISTANCE)


# variables
temp_air = 21 # degrees celsius
ppfd = 600 #  umol m-2
relative_humidity = 73
net_radiation = calc_net_radiation(ppfd)

def calc_residual(temp_surface, net_radiation):
    sensible_heat_exchange = calc_sensible_heat_exchange(temp_air, temp_surface)
    latent_heat_flux = calc_latent_heat_flux(temp_air, temp_surface, relative_humidity, ppfd)
    return net_radiation - sensible_heat_exchange - latent_heat_flux

from scipy.optimize import root_scalar

limit = 5.0
xa = temp_air - limit
xb = temp_air + limit
args = (net_radiation,)
result = root_scalar(calc_residual, bracket=[xa, xb], args=args)

assert result.converged
temp_surface = result.root


sensible_heat_exchange = calc_sensible_heat_exchange(temp_air, temp_surface)
latent_heat_flux = calc_latent_heat_flux(temp_air, temp_surface, relative_humidity, ppfd)
 
print("NET RADIATION: ",net_radiation)
print("SENSIBLE HEAT EXCHANGE ", sensible_heat_exchange)
print("LATENT HEAT FLUX ", latent_heat_flux)
stomatal_resistance = 60 * (1500 + ppfd) / (220 + ppfd)
print("STOMATAL RESISTANCE", stomatal_resistance)



