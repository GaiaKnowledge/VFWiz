#  Main Code for VF Wiz - Francis Baumont De Oliveira

import json
import math
import numpy as np

from vf_inputs import Scenario


def get_scenario(input_file):
    with open(input_file) as f:
        inputs = json.load(f)
    scenario = Scenario()
    scenario.lights = inputs['lights']
    scenario.crop = inputs['crop']
    scenario.area = inputs['grow_area']
    scenario.surface = inputs['surface_area']
    scenario.volume = inputs['farm_volume']
    scenario.building = inputs['building_type']
    scenario.system = inputs['grow_system']
    scenario.CO2 = inputs['co2_enrichment']
    scenario.energy = inputs['energy_price']
    scenario.toutdoors = inputs['average_outdoor_temperature']
    scenario.crop_price = inputs['crop_price_per_kilo']
    scenario.wages = inputs['minimum_wage']
    return scenario

# System
def calc_no_of_racks(grow_system, grow_area):
   if grow_system == 'ziprack_8':
      no_of_racks = math.floor(grow_area/4.62963)  # 54 Zipracks per 250 sq-m (including aisles, work bench and plumbing kit)
   else:
      raise RuntimeError("Unknown grow_system: {}".format(grow_system))
   return no_of_racks

# Harvest weight

def calc_harvest_weight(crop):

   if crop == "lettuce":
      harvest_weight = 0.5  # kg
   else:
      raise RuntimeError("Unknown crop {}".format(crop))

   return harvest_weight

def get_gross_yield(crop):
   if crop == 'lettuce':
      ys = 78.5  # kg / m2 / year
   else:
      raise RuntimeError("Unknown crop {}".format(crop))
   return ys


# Plant Capacity

def calc_plant_capacity(crop, grow_system, no_of_racks):   # Excluding propagation and only those within the vertical farming systems
   if crop == "lettuce" and grow_system == 'ziprack_8':
      no_of_towers = no_of_racks*30  # Tight spacing with lettuce (30 towers per rack)
      yield_capacity = no_of_towers*3.3  # 3.3kg of greens per tower
      harvest_weight = calc_harvest_weight(crop)
      farm_plant_capacity = yield_capacity / harvest_weight # Potential yield divided by harvest weight of each product
   else:
      raise RuntimeError("Unknown crop {}".format(crop))

   return farm_plant_capacity, yield_capacity


# Lights

def get_spec(lights):
    if lights == "intraspectra_spectrablade_8":
      light_wattage = 75
      light_efficiency = 0.4
      print("The {} light is {} watts with an efficiency of: {}".format(lights, light_wattage, light_efficiency))
    else:
         raise RuntimeError("Unknown lights {}".format(lights))
    return light_wattage, light_efficiency

def calc_no_of_lights(grow_system, no_of_racks):
   if grow_system == 'ziprack_8':
      no_of_lights = no_of_racks*24  # Assumption that 24 lighting units are require to cover crop area of 1 Ziprack (30 towers)
   else:
      raise RuntimeError("Unknown grow system {}".format(grow_system))  
   return no_of_lights

def calc_lights_energy(lights, no_of_lights):
   lights_watts, efficiency = get_spec(lights)
   lighting_kw_usage = lights_watts*no_of_lights/1000
   kwh_per_day = lighting_kw_usage*12  # Assuming 12 hours of light for plants
   return kwh_per_day



# HVAC

def get_temp_crop_reqs(crop):
   if crop == 'lettuce':
      Tin = 23.9  # Temperature optimal for lettuce growth
   else:
      Tin = 22  # 'general temperature'
   return Tin

def calc_HVAC_energy(surface_area, building_type, Tin, Tout):
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



# Labour

# Energy
def calc_daily_energy_consumption(HVAC_daily_energy, lights_daily_energy):
   kwh_per_day = HVAC_daily_energy + lights_daily_energy
   return kwh_per_day

def calc_monthly_energy_consumption(farm_kwh_per_day):
   monthly_energy_consumption_farm = farm_kwh_per_day * 28  # 4 weeks, 28 days a month
   return monthly_energy_consumption_farm


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



def calc_crop_ppfd_reqs(crop):
   if crop == 'lettuce':
      crop_ppfd_reqs = 295
   else:
      raise RuntimeError("Unknown crop: {}".format(crop))
   return crop_ppfd_reqs


# Annual yield
def calc_adjusted_yield(building_type, ys, crop, pa, lights, co2_enrichment, tf, crop_ppfd_reqs, ppfd_lights, grow_area):

   #PAR factor
   if lights == "intraspectra_spectrablade_8":
      PARf = 1
   else:
      PARf = ppfd_lights/crop_ppfd_reqs  # ratio of PAR delivered to canopy to theoretical PAR reqs
   # CO2 factor
   if co2_enrichment == 'yes':
      CO2f = 1
   else:
      CO2f = 0.9

   # standard yield
   if isinstance(ys, int):
      ys = ys
   else:
      ys = get_gross_yield(crop)
      pa = grow_area

   #Temperature

   #Failure rate
   fr = 0.05

   ya = ys*pa*PARf*CO2f*tf*(1-fr)
   return ya

# Sales

def sales(ya, crop_price):
   crop_sales = ya*crop_price
   return crop_sales


def OpEx(days,labour, farm_kwh_per_day, energy_price):
   for i in range(days):
      if i % 30 == 0:
       # OpEx += labour()  # Fixed costs
       OpEx += (energy(farm_kwh_per_day, energy_price)*30)

      elif i % 365 == 0:
        OpEx += 2 # annualcosts(ienergystandingcharge, iwaterstandingcharge, iinsurance)  # Fixed costs


# Operations = Bill Growth Lights + Bill Environmental Control + Bill Misc Energy + Water Bill + Seed Cost
# + Nutrient Cost + Personnel Cost + Maintenance Cost + CO2 Cost - Reduction from Renewable Energy
# Inputs = Seeds + Nutrients + Grow Media

# REVENUE




def revenue(days, ya, crop_price):
   sales = 0.0
   for i in range(days):
      if i % 30 == 0:
        sales += sales(ya, crop_price) # revenue(input_data.system)
        #Revenue += rent(iAnnual_rent, iSize, iLocation, iLocation_type)
        #Revenue += utilitiesM(energy(), water(), internet)
        #Revenue += consumables(nutrients, seeds, grow_media)
        #Revenue +=
      elif i % 365 == 0:
        sales += 50

# PROFIT
def profit(sales_array, OpEx_array):
   profit_array = sales_array - OpEx_array  # Profit = revenue from sales - running costs
   return profit_array


def gross_profit_margin(sales_array,
                        cogs):  # Profit and Cost of Goods Sold - i.e. cost of materials and director labour costs
   gross_profit_margin = (sales_array - cogs) / sales_array  # Total revenue - Cost of goods sold (COGS) / revenue
   return gross_profit_margin

# OPEX

OpEx: int = 0
days = 366
OpEx_array = []
sales: int = 0
sales_array = []

print("Days",days-1)
input_file = 'input_file.json'
scenario = get_scenario(input_file)

no_of_racks = calc_no_of_racks(scenario.system, scenario.area)
no_of_lights = calc_no_of_lights(scenario.system, no_of_racks)
lights_daily_energy = calc_lights_energy(scenario.lights, no_of_lights)

HVAC_daily_energy = calc_HVAC_energy(surface_area=scenario.surface, building_type=scenario.building,
                                Tin=get_temp_crop_reqs(scenario.crop), Tout=scenario.toutdoors)
farm_kwh_per_day = calc_daily_energy_consumption(HVAC_daily_energy, lights_daily_energy)
monthly_energy_consumption_farm = calc_monthly_energy_consumption(farm_kwh_per_day)
farm_plant_capacity, standard_yield = calc_plant_capacity(scenario.crop, scenario.system, no_of_racks)
ys = standard_yield
crop_ppfd_reqs = calc_crop_ppfd_reqs(scenario.crop)
ppfd_lights = 295  # placeholder

tf = 1
OpEx_array.append(OpEx)
# ARRAY conversion
sales_array.append(sales)
sales_array = np.asarray(sales_array) # Sales as an array
OpEx_array = np.asarray(OpEx_array)  # OpEx as an array
profit_array = profit(sales_array, OpEx_array)


# gross_profit_margin(sales_array, cogs)

print("Profit £:", profit_array[-1])

# plt.plot(profit_array)
# plt.xlabel('Days')
# plt.ylabel('Gross Profit')
# plt.show()

# plt.figure()
# plt.plot(gross_profit_margin)
# plt.xlabel('Days')
# plt.ylabel('Gross Profit Margin')
# plt.show()
#
# print("Gross Profit Margin:",gross_profit_margin[-1])

# print("GOT costs ", costs)