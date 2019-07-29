'''
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

'''
import math
from constants import DENSITY_OF_AIR, HEAT_CAPACITY_OF_AIR, LATENT_HEAT_WATER

# Fixed inputs
lai = 3 # their value 3.1.3
cultivation_area_coverage = 0.9 # their value 3.1.1
reflection_coefficient = 0.065 # 3.1.1 reflection coefficient of lettuce for PAR, is reported to be 5–8
mean_leaf_diameter = 0.11

aerodynamic_heat_resistance = 100 # 3.1.3 (100 air circulation on, 200 air circulation off)
epsilon = -999 # slope of saturation vapour pressure curve at air temperature 
air_speed = 0.15 # m s-1 - taken from Michael's report - could calculate from air change volumes?


# variables
ppfd = -999 # their calculation in umol m-2
temp_air = -999 # input parameter
lighting_radiation = -999
relative_humidty = -999



#jmht added
# From: http://www.fao.org/3/X0490E/x0490e0k.htm
saturated_vapour_pressure = 0.6108 * math.exp((17.27 * temp_air) / (temp_air + 237.3))
vapour_pressure = saturated_vapour_pressure * relative_humidty / 100

# Relate the vapour_pressure to concentration through the ideal gas law?: pV = nRT
# 

epsilon = 4098 * saturated_vapour_pressure / (temp_air + 237.3)^2


vapour_concentration_air = -999


temp_surface = -999 # calculated parameter

# 10. Submodel for aerodynamic boundary layer resistance
# ra = 350 * (1/u∞)0.5 * 1/LAI
# u∞: uninhibited air speed
# LAI: leaf active area index (they recommend 3)
vapour_resistance = 350 * (1 / air_speed)^0.5 * (mean_leaf_diameter/lai)

# 9. Submodel for stomatal resistance
# rs = 60 * (1500 + PPFD) / (220  + PPFD)
# PPFD: photosynthetic photon flux density (μmol/m2s)
stomatal_resistance = 60 * (1500 + ppfd) / (220 + ppfd)

# 8. Submodel for net radiation
# Rnet = (1 - ρr) * Ilighting * CAC
# ρr: reflection coefficient
# Ilighting: radiation
# CAC: cultivation area cover
net_radiation = (1 - reflection_coefficient) * lighting_radiation * cultivation_area_coverage

# 7. Relation of χs to χa
# χs = χa + (ρa * cp) / λ * ε * (Ts - Ta)
# ε: vapour concentration (slope of the saturation function curve)
vapour_concentration_surface = vapour_concentration_air + ((DENSITY_OF_AIR * HEAT_CAPACITY_OF_AIR) / LATENT_HEAT_WATER ) * \
                               epsilon * (temp_surface - temp_air)

# 6. Latent Heat Flux λE - I think this is the evapotranspiration rate
# λE = LAI * λ * (χs - χa) / (rs + ra)
# λ: latent heat of the evaporation of water
# χs: vapour concentration at the transpiring surface
# χa:  vapour concentration in surrounding air
# rs: surface (or stomatal) resistance
# ra: aerodynamic resistance to vapour transfer
latent_heat_flux = lai * LATENT_HEAT_WATER * ( (vapour_concentration_surface - vapour_concentration_air) / \
                                               (stomatal_resistance + vapour_resistance) )

# 5. Sensible heat exchange H
# H = LAI * ρa * cp * (Ts - Ta / ra)
# LAI: Leaf Area Index
# ρa: Density of air
# cp: Heat capacity of air - CHECK IS  ρacp in table
# Ts: temperature at the transpiring surface
# Ta: temperature of surrounding air
# ra: aerodynamic resistance to heat
sensible_heat_exchange = lai * DENSITY_OF_AIR * HEAT_CAPACITY_OF_AIR * ((temp_surface - temp_air) / aerodynamic_heat_resistance)


# 4. Crop Energy Balance
# Rnet - H - λE = 0
# Rnet: net radiation - the amount of radiation intercepted and absorbed by the crop
# H: sensible heat exchange
# λE: latent heat flux
net_radiation = sensible_heat_exchange + latent_heat_flux


