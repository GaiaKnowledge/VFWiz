#  Main Code for VF Wiz - Francis Baumont De Oliveira

import json
import math
# class inputContainer(object):

def get_input_scenario(input_file):
   with open(input_file) as f:
       inputs = json.load(f)
   input_scenario = inputContainer()
   input_scenario.iLights = inputs['light_type']
   input_scenario.iCrop = inputs['crop']
   input_scenario.iArea = inputs['grow_area']
   input_scenario.iSurface = inputs['surface_area']
   input_scenario.iVolume = inputs['farm_volume']
   input_scenario.iBuilding = inputs['building_type']
   input_scenario.iSystem = inputs['grow_system']
   input_scenario.iEnergy = inputs['energy_price']
   input_scenario.Toutdoors = inputs['average_outdoor_temperature']
   input_scenario.iCrop_price = inputs['crop_price_per_kilo']
   input_scenario.iWages = inputs['minimum_wage']
   return input_scenario
input_file = 'input_file.json'
input_scenario = get_input_scenario(input_file)

# System

def number_of_racks(grow_system, grow_area):

   if grow_system == 'ziprack_8':
      no_of_racks = math.floor(grow_area/4.62963)  # 54 Zipracks per 250 sq-m (including aisles, work bench and plumbing kit)
   else:
      no_of_racks = 'unknown'
   return no_of_racks

# Harvest weight

def crop(crop_type):

   if crop_type = "lettuce":
      harvest_weight = 0.5  # kg
   else:
      harvest_weight = "unknown"
   return harvest_weight

# Plant Capacity

def plant_capacity(crop_type, grow_system, no_of_racks):   # Excluding propagation and only those within the vertical farming systems

   if crop_type == "lettuce" and grow_system == 'ziprack_8':
      no_of_towers = no_of_racks*30  # Tight spacing with lettuce (30 towers per rack)
      yield_capacity = no_of_towers*3.3  # 3.3kg of greens per tower
      farm_plant_capacity = yield_capacity/harvest_weight # Potential yield divided by harvest weight of each product
   elif grow_system != 'ziprack_8' or crop_type != 'lettuce':
      print("unknown system or crop variety. Please insert another.")
      yield_capacity = "unknown"
      farm_plant_capacity = "unknown"
   else:
      print("unknown")
      yield_capacity = "unknown"
      farm_plant_capacity = "unknown"
   return farm_plant_capacity, yield_capacity


# Lights

def displayspec(light_type):
    if light_type == "intraspectra_spectrablade_8":
      light_wattage = 75
      light_efficiency = 0.4
      print('The' + light_type + 'light is' + light_wattage, "Watts with an efficiency of:" + light_efficiency)
    else:
      light_wattage = 'unknown'
      light_efficiency = 'unknown'
    return light_wattage, light_efficiency

def qty_lights(grow_system, no_of_racks):

   if grow_system == 'ziprack_8':
   no_of_lights == no_of_racks*24  # Assumption that 24 lighting units are require to cover crop area of 1 Ziprack (30 towers)
   else:
   no_of_lights == "unknown"
   return no_of_lights

def lights_energy(light_type, qty_lights):

   lights_watts, efficiency = displayspec(light_type)
   lighting_kw_usage = lights_watts*qty_lights/1000
   kwh_per_day = lighting_kw_usage*12  # Assuming 12 hours of light for plants
   return kwh_per_day

lights_daily_energy = lights_energy(light_type=input_scenario.iLights, qty_lights(input_scenario.iSystem, no_of_racks))

# HVAC

def temp_crop_reqs(crop_type):
   if crop_type == 'lettuce':
      Tin = 23.9  # Temperature optimal for lettuce growth
   else:
      Tin = 22  'general temperature'
   return Tin

def HVAC_energy(surface_area, building_type, Tin, Tout):
   if building_type == 'basement':
      U = 0.5
   else:
      U= 24
   Q = U*surface_area*(Tin-Tout)
   HVAC_kwh = Q*0.00666667*24  # Conversion factor of kJ/h to kWh x 24 hours

   """" Heat Transfer Equation

   Notes
      -----
          Q = U x SA x (Tin - Tout)
          Q - ﻿Heat lost or gained due to outside temperature (kJ·h−1)
          U - Overall heat transfer coefficient (kJ·h−1·m−2·°C−1)
          SA - Surface Area of the space
          Tin - ﻿Inside air set point temperature (°C)
          Tout - ﻿Outside air temperature (°C)
      """

   return HVAC_kwh

HVAC_daily_energy = HVAC_energy(surface_area=input_scenario.iSurface, building_type=input_scenario.iBuilding,
                                 Tin=temp_crop_reqs(input_scenario.iCrop, Tout=input_scenario.Toutdoors))

# Labour

# OPEX

# Energy
def daily_energy_consumption(HVAC_daily_energy, lights_daily_energy):
   kwh_per_day = HVAC_daily_energy + lights_daily_energy
   return kwh_per_day

farm_kwh_per_day = daily_energy_consumption(HVAC_daily_energy, lights_daily_energy)

def monthly_energy_consumption(farm_kwh_per_day):
   m_energy_consumption = farm_kwh_per_day * 28  # 4 weeks, 28 days a month
   return mec

monthly_energy_consumption_farm = monthly_energy_consumption(farm_kwh_per_day)

# Yield

"""" Adjusted Plant Yield Equation

Notes
   -----
   Ya = Ys x PA x PARf x CO2f x Tf x (1 - Fr)
   Adjusted Plant Yield = Standard Yield x Plant Area x PAR factor
   PARf = ratio of actual PAR delivered to plant canopy compared to theoretical plant requirements. In artificial lighting
       VF the value was 1 as controlled at optimal level. Sun-fed plant level from EcoTect simulation.) x 
   CO2f = Increment by CO2 enrichment
   Tf = Temperature factor (reflects reduction of yield caused by overheating or freezing of the growing area
       if indoor temperature is uncontrolled by HVAC or other systems, value can be set for 0.9 for preliminary estimation)
   Fr = Failure rate, by default set at 5%
   """

# Sales

# REVENUE

# PROFIT