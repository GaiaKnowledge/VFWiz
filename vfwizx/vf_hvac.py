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


PV = nRT => n/V = P/RT

"""
import logging
import math

from scipy.optimize import root_scalar

# https://www.ohio.edu/mechanical/thermo/property_tables/air/air_cp_cv.html at 300K/26.85C
HEAT_CAPACITY_OF_AIR =  1003 # J kg-1 C-1

# Need canonical reference: https://en.wikipedia.org/wiki/Latent_heat
LATENT_HEAT_WATER = 2264705 # J Kg-1

# Valye from paper
PSYCHOMETRIC_CONSTANT = 65.0 # Pa/K

IDEAL_GAS_CONSTANT = 8.3145 # J mol-1 K-1

MOLAR_MASS_H2O = 18.01528 # g mol-1

ZERO_DEGREES_IN_KELVIN = 273.15


PLANK_CONSTANT = 6.626 * 10**-34
SPEED_OF_LIGHT =  2.998 * 10**8 # m s-1
AVOGADRO_NUMBER = 6.0221367 * 10**23

KG_TO_G = 1000

logger = logging.getLogger()


def calc_temp_surface(*, # Force all keyword arguments
                      temp_air,
                      ppfd,
                      relative_humidity,
                      lai,
                      vapour_resistance,
                      reflection_coefficient,
                      cultivation_area_coverage):
    logger.info("""Calculating surface temperature with:
    Air temperature: {}
    PPFD: {}
    Relative Humidity {}
    LAI: {}
    Vapour resistance: {}
    Reflection, coefficient: {}
    Cultivation Area Coverage: {}
""".format(temp_air, ppfd, relative_humidity, lai, vapour_resistance, reflection_coefficient, cultivation_area_coverage))

    def calc_residual(temp_surface, net_radiation):
        sensible_heat_exchange = calc_sensible_heat_exchange(temp_air, temp_surface, lai, vapour_resistance)
        latent_heat_flux = calc_latent_heat_flux(temp_air, temp_surface, relative_humidity, ppfd, lai, vapour_resistance)
        return net_radiation - sensible_heat_exchange - latent_heat_flux
    
    net_radiation = calc_net_radiation(ppfd, reflection_coefficient, cultivation_area_coverage)
    
    limit = 5.0
    xa = temp_air - limit
    xb = temp_air + limit
    args = (net_radiation,)
    result = root_scalar(calc_residual, bracket=[xa, xb], args=args)
    
    assert result.converged
    temp_surface = result.root
    return temp_surface


def calc_net_radiation(ppfd, reflection_coefficient, cultivation_area_coverage):
    """
    8. Submodel for net radiation
    Rnet = (1 - ρr) * Ilighting * CAC
    ρr: reflection coefficient
    Ilighting: radiation
    CAC: cultivation area cover
    
    NOTES
    -----
    cultivation_area_coverage = 0.9 # value from section 3.1.1 of paper
    reflection_coefficient = 0.05 # Luuk Gaamans personal communication
    """
    lighting_radiation = calc_lighting_radiation(ppfd)
    return (1 - reflection_coefficient) * lighting_radiation * cultivation_area_coverage


def calc_lighting_radiation(ppfd):
    """Values taken from paper
    
    
    # E = hf = hc/w
    photon_energy = AVOGADRO_NUMBER * PLANK_CONSTANT * n * SPEED_OF_LIGHT  / wavelength
    
    PPFD measured in mol m-2 s-1
    
    Flux density measured in W m-2
    
    
    # https://www.researchgate.net/post/Can_I_convert_PAR_photo_active_radiation_value_of_micro_mole_M2_S_to_Solar_radiation_in_Watt_m22
    # Rule of thumb is 1 W m-2 = 4.57 umol m-2 so 140 ppfd ~= 30.6
    
    
    
#     import scipy.integrate
#     ppfd = 140 #umol
#     def pe(wavelength, ppfd):
#         # ppfd in umol
#         # wavelength in nm
#         n = ppfd * 10**-6 #
#         return AVOGADRO_NUMBER * PLANK_CONSTANT * SPEED_OF_LIGHT * n / (wavelength * 10**-9)
#     #r = scipy.integrate.quad(pe, 400, 700)
#     #print(pe(700))
#     #print(r)
#     
# #     ppfd = 140 
# #     e = 20.82
# #     w = 804.4165185104332
#     ppfd = 200
#     e = 41.0
#     #w = 555
#     #e = AVOGADRO_NUMBER * PLANK_CONSTANT * SPEED_OF_LIGHT * ppfd * 10**-6  / (w * 10**-9)
#    # print(e)
#     
#     w = AVOGADRO_NUMBER * PLANK_CONSTANT * SPEED_OF_LIGHT * ppfd * 10**-6 / (e * 10**-9)
#     
#     print(w)
    
    """
    # Guess from paper
    if ppfd == 140:
        lighting_radiation = 28
    elif ppfd == 200:
        lighting_radiation = 41
    elif ppfd == 300:
        lighting_radiation = 59
    elif ppfd == 400:
        lighting_radiation = 79.6
    elif ppfd == 450:
        lighting_radiation = 90.8
    elif ppfd == 600:
        lighting_radiation = 120
    else:
        assert False
    return lighting_radiation


def calc_sensible_heat_exchange(temp_air, temp_surface, lai, vapour_resistance):
    """
    5. Sensible heat exchange H
    H = LAI * ρa * cp * (Ts - Ta / ra)
    LAI: Leaf Area Index
    ρa: Density of air
    cp: Heat capacity of air
    Ts: temperature at the transpiring surface
    Ta: temperature of surrounding air
    ra: aerodynamic resistance to heat
    """
    return lai * HEAT_CAPACITY_OF_AIR * ((temp_surface - temp_air) / vapour_resistance)


def calc_latent_heat_flux(temp_air, temp_surface, relative_humidity, ppfd, lai, vapour_resistance):
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
    logger.debug('vapour pressure air: {}'.format(vapour_pressure_air))
    vapour_pressure_surface = calc_vapour_pressure_surface(temp_air, temp_surface, vapour_pressure_air)
    logger.debug('vapour pressure surface: {}'.format(vapour_pressure_surface))
    
#     vapour_concentration_air = vapour_concentration_from_pressure(vapour_pressure_air, temp_air)
#     logger.debug('vapour concentration air: {}'.format(vapour_concentration_air))
#     vapour_concentration_surface = vapour_concentration_from_pressure(vapour_pressure_surface, temp_surface)
#     logger.debug('vapour concentration surface: {}'.format(vapour_concentration_surface))
    
    stomatal_resistance = calc_stomatal_resistance(ppfd)
    return lai * LATENT_HEAT_WATER * KG_TO_G * ( (vapour_pressure_surface - vapour_pressure_air) / (stomatal_resistance + vapour_resistance) )
#     return lai * LATENT_HEAT_WATER* KG_TO_G * ( (vapour_concentration_surface - vapour_concentration_air) / (stomatal_resistance + vapour_resistance) )


def calc_vapour_pressure_air(temp_air, relative_humidity):
    """
    jmht added - seems to get different results from below
    From: http://www.fao.org/3/X0490E/x0490e0k.htm
    saturated_vapour_pressure = 0.6108 * math.exp((17.27 * temp_air) / (temp_air + 237.3))
    Luuk Gaamans personal communication:
        Vapour concentration in the air = Relative humidity * saturated vapour concentration at air temperature (g m-3)
        Additional information:
        https://www.engineeringtoolbox.com/water-vapor-saturation-pressure-air-d_689.html
        https://www.engineeringtoolbox.com/relative-humidity-air-d_687.html
    """
    saturated_vapour_pressure = calc_saturated_vapour_pressure_air(temp_air)
    return saturated_vapour_pressure * relative_humidity / 100


def calc_saturated_vapour_pressure_air(temp_air):
    """Saturated vapour pressure of air in Pascals
     given air temperature in Degress Celsius
    From: https://www.engineeringtoolbox.com/water-vapor-saturation-pressure-air-d_689.html
    """
    temp_air_k = temp_air + ZERO_DEGREES_IN_KELVIN
    return math.exp(77.345 + (0.0057 * temp_air_k) - (7235 / temp_air_k) ) / temp_air_k**8.2


def calc_saturated_vapour_pressure_air_FAO(temp_air):
    """
    From: http://www.fao.org/3/X0490E/x0490e0k.htm
    Results are in kPa so multiply by 1000
    slightly different results from above
    
    """
    return 0.611 * math.exp((17.27 * temp_air) / (temp_air + 237.3)) * 1000


def calc_vapour_pressure_surface(temp_air, temp_surface, vapour_pressure_air):
    """
    7. Relation of χs to χa
    χs = χa + (ρa * cp) / λ * ε * (Ts - Ta)
    λ: latent heat of the evaporation of water
    ρa: Density of air
    cp: Heat capacity of air - CHECK IS  ρacp in table
    χs: vapour concentration at the transpiring surface
    χa:  vapour concentration in surrounding air
    ε: vapour concentration (slope of the saturation function curve)

    """
    epsilon = calc_epsilon(temp_air)
    return vapour_pressure_air + (HEAT_CAPACITY_OF_AIR / LATENT_HEAT_WATER * KG_TO_G) * \
           epsilon * (temp_surface - temp_air)


def calc_epsilon(temp_air):
    """
    Unitless but for kPa - so need to make sure everything else matches
    
    epsilon relates the vapour_pressure to concentration. Explanation from Luuk:
        The simplest way to calculate it is epsilon = delta / gamma
        Where delta = 0.04145*exp(0.06088*T_s) (kPa/C)
        Gamma = 66.5  (Pascal/K) (gamma is a psychometric constant)
    """
    delta = 0.04145 * math.exp(0.06088 * temp_air)
    return delta / PSYCHOMETRIC_CONSTANT   

def calc_epsilon_FAO(temp_air):
    """    
    From: http://www.fao.org/3/X0490E/x0490e0k.htm
    Disagrees by order of magnitude with above - even with factor of 1000
    """
    return ((2504 * math.exp((17.27 * temp_air) / (temp_air + 237.2))) / math.pow((temp_air + 237.2), 2)) / 1000


def vapour_concentration_from_pressure(vapour_pressure, temperature):
    """Calculate concentration in kg m-3 from pressure in Pascals for water
    
    Ideal Gas Law:
    PV = nRT => n/V = P/RT
    
    Multiply by molar mass to get concentration in kg m-3
    """
    return vapour_pressure / (IDEAL_GAS_CONSTANT * (temperature + ZERO_DEGREES_IN_KELVIN)) * (MOLAR_MASS_H2O / 1000)
#     return vapour_pressure / (IDEAL_GAS_CONSTANT * (temperature + ZERO_DEGREES_IN_KELVIN)) * (MOLAR_MASS_H2O)


def calc_stomatal_resistance(ppfd):
    return 60 * (1500 + ppfd) / (200 + ppfd)



if __name__ == '__main__':
    
#     print(calc_epsilon(20))
#     print(calc_epsilon(21))
#     print(calc_epsilon(22))
#     print(calc_epsilon(23))
#     print(calc_epsilon(24))
#     epsilon = calc_epsilon(24)
#     # 0.0027489543738581732
#     y = HEAT_CAPACITY_OF_AIR / LATENT_HEAT_WATER * KG_TO_G
#     print(y)
#     # 0.0005332757688087411
#     x = y * epsilon
#     print(x)
#     # 1.465950757139369e-06
    
    logging.basicConfig(level=logging.DEBUG)
      
    # variables
    temp_air = 21 # degrees celsius
    ppfd = 600 #  umol m-2
    relative_humidity = 73 # %
    lai = 3 # no units
    vapour_resistance = 100 #  s m-1
    reflection_coefficient = 0.05
    cultivation_area_coverage = 1.0
        
    temp_surface = calc_temp_surface(temp_air=temp_air,
                                     ppfd=ppfd,
                                     relative_humidity=relative_humidity,
                                     lai=lai,
                                     vapour_resistance=vapour_resistance,
                                     reflection_coefficient=reflection_coefficient,
                                     cultivation_area_coverage=cultivation_area_coverage)
    logger.info("Calculated surface temperature of: {}".format(temp_surface))
        
    net_radiation = calc_net_radiation(ppfd, reflection_coefficient, cultivation_area_coverage)
    sensible_heat_exchange = calc_sensible_heat_exchange(temp_air, temp_surface, lai, vapour_resistance)
    latent_heat_flux = calc_latent_heat_flux(temp_air, temp_surface, relative_humidity, ppfd, lai, vapour_resistance)
     
     
    svp = calc_saturated_vapour_pressure_air(temp_air)
    svc = vapour_concentration_from_pressure(svp, temp_air)
    print("VAPOUR PRESSURE DEFICIT ", svc * (1-(relative_humidity/100)) * 1000)
         
    print("SURFACE TEMPERATURE ",temp_surface)
    print("NET RADIATION: ",net_radiation)
    print("SENSIBLE HEAT EXCHANGE ", sensible_heat_exchange)
    print("LATENT HEAT FLUX ", latent_heat_flux)
    print("STOMATAL RESISTANCE", calc_stomatal_resistance(ppfd))




