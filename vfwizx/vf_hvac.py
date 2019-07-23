'''
Created on 18 Jul 2019

@author: jmht




The MATLAB (2016) model executes an iterative process to simultaneously solve (Eqs. 4–7), processing the net PAR flux density,
the sur- face and aerodynamic resistances as outlined above (Eqs. 8–10).

The iterative process is based on the aforementioned equations and is performed in a continuous loop. For each set interval of Ta,
the model calculates the corresponding Ts at which the energy balance (Rnet– H–λE) is closest to zero. The model utilises a
continuous loop to ap- proach this value at the set discretisation and consequently indexes the value closest to zero.
Finally, the model lists the different variables congruent with this zero energy balance, in particular the quantity of the 
sensible (H) and latent (λE) heat exchange.

4. Crop Energy Balance
Rnet - H - λE = 0

Rnet: net radiation - the amount of radiation intercepted and absorbed by the crop
H: sensible heat exchange
λE: latent heat flux

5. Sensible heat exchange H
H = LAI * ρa * cp * (Ts - Ta / ra)

LAI: Leaf Area Index
ρa: Density of air
cp: Heat capacity of air - CHECK IS  ρacp in table
Ts: temperature at the transpiring surface
Ta: temperature of surrounding air
ra: aerodynamic resistance to heat

6. Latent Heat Flux λE - I think this is the evapotranspiration rate
λE = LAI * λ * (χs - χa) / (rs + ra)

λ: latent heat of the evaporation of water
χs: vapour concentration at the transpiring surface
χa:  vapour concentration in surrounding air
rs: surface (or stomatal) resistance
ra: aerodynamic resistance to vapour transfer

7. Relation of χs to χa
χs = χa + (ρa * cp) / λ * ε * (Ts - Ta)
ε: vapour concentration (slope of the saturation function curve)

8. Submodel for net radiation
Rnet = (1 - ρr) * Ilighting * CAC
ρr: reflection coefficient
Ilighting: radiation
CAC: cultivation area cover - they suggest using 0.9 (90%)

9. Submodel for stomatal resistance
rs = 60 * (1500 + PPFD) / (220  + PPFD)
PPFD: photosynthetic photon flux density (μmol/m2s)

10. Submodel for aerodynamic boundary layer resistance
ra = 350 * (1/u∞)0.5 * 1/LAI
u∞: uninhibited air speed
LAI: leaf active area index (they recommend 3)

'''
from constants import DENSITY_OF_AIR, HEAT_CAPACITY_OF_AIR, LATENT_HEAT_WATER

# Fixed inputs
lai = 3 # their value 3.1.3
cultivation_area_coverage = 0.9 # their value 3.1.1
aerodynamic_heat_resistance = 100 # 3.1.3 (100 air circulation on, 200 air circulation off)
epsilon = -999 # vapour concentration (slope of the saturation function curve)
air_speed = -999

# variables
ppfd = -999
temp_surface = -999
temp_air = -999
vapour_concentration_air = -999
vapour_concentration_surface = -999
reflection_coefficient = -999
lighting_radiation = -999


# 10. Submodel for aerodynamic boundary layer resistance
# ra = 350 * (1/u∞)0.5 * 1/LAI
# u∞: uninhibited air speed
# LAI: leaf active area index (they recommend 3)
vapour_resistance = 350 * (1 / air_speed)^0.5 * (1/lai)

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




                               








