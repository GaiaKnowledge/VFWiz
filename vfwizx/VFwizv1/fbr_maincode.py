#  Main Code for VF Wiz - Francis Baumont De Oliveira

import json
def get_input_scenario(input_file):
   with open(input_file) as f:
       inputs = json.load(f)
   input_scenario = inputContainer()
   input_scenario.iLights = inputs['light_type']
   input_scenario.iCrop = inputs['crop']
   input_scenario.iArea = inputs['farm_area']
   input_scenario.iSystem = inputs['grow_system']
   input_scenario.iEnergy = inputs['energy_price']
   input_scenario.Toutdoors = inputs['average_outdoor_temperature']
   input_scenario.iCrop_price = inputs['crop_price_per_kilo']
   input_scenario.iWages = inputs['minimum_wage']
   return input_scenario
input_file = 'input_file.json'
input_scenario = get_input_scenario(input_file)