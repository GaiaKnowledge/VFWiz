import math


def energy_lights(System = None, Lights = None, ienergy_price = None):  # Daily cost of energy 
    
    if Lights[0] != "unknown" and Lights[2] != 0:
     
        light_wattage = Lights[2]*Lights[3]/1000  # Lighting kW farm usage *qty x wattage
        kWh_daily_lights = light_wattage*Lights[4]  # kWh consumption from lights per day
        lights_daily_cost = kWh_daily_lights * ienergy_price
        return lights_daily_cost
    
    elif System[0] == 'unknown' and Lights[0] == 'unknown':
        return 'unknown'
        
    else:
        System[0] == 'ZipTower' and Lights[0] == "unknown"
        
        if Lights[1] == "air":
            Lights[2] = System[1]*26  # Number of racks x 26
            Lights[3] = 48  # 48W for air-cooled
            light_wattage = Lights[2]*Lights[3]/1000  # Lighting kW farm usage qty x wattage
            kWh_daily_lights = light_wattage*Lights[4]  # light wattage and hours on per day
            lights_daily_costs = kWh_daily_lights * ienergy_price  # daily kWh x price

        else:
            Lights[1] == 'water'
            Lights[2] = System[1]*10  # Number of racks x 10
            Lights[3] = 200  # 200W for water-cooled
            light_wattage = Lights[2]*Lights[3]/1000  # Lighting kW farm usage qty x wattage
            kWh_daily_lights = light_wattage*Lights[4]  # light wattage and hours on per day
            lights_daily_costs = kWh_daily_lights * ienergy_price  # daily kWh x price
            
    return lights_daily_costs

def energy_climate(Climate=None, energy_price=None):
    
    Control_kWh_daily = float(Climate[1, 1])*float(Climate[2, 1])*float(Climate[3, 1])/1000  # System control: Quantity x Watts x Hours /1000
    Injector_kWh_daily = float(Climate[1, 2])*float(Climate[2, 2])*float(Climate[3, 2])/1000  # CO2 Injector: Quantity x Watts x Hours /1000
    Dehumidifier_kWh_daily = float(Climate[1, 3])*float(Climate[2, 3])*float(Climate[3, 3])/1000  # Dehumidifier: Quantity*Watts*Hours /1000
    Fans_kWh_daily = float(Climate[1, 4])*float(Climate[2, 4])*float(Climate[3, 4])/1000  # Inline Fans: Quantity x Watts x Hours /1000
    
    Climate_energy = Control_kWh_daily + Injector_kWh_daily + Dehumidifier_kWh_daily + Fans_kWh_daily
    
    daily_cost_climate = Climate_energy * energy_price
    return daily_cost_climate

def energy_plumbing(System=None, Plumbing_kit=None, energy_price=None):
    
    if System[0] == 'ZipTower':
        if float(System[1]) < float(Plumbing_kit[2]):  # If System rack units is less than Plumbing system capacity
            nPlumbing_kits = 1  # number of plumbing kits
        
        else:
            float(System[1]) >= float(Plumbing_kit[2])  # If system rack units is more than or equal to plumbing capacity
            nPlumbing_kits = math.ceil(float(System[1])/float(Plumbing_kit[2]))  # Round number System units / plumbing capacity
        
        Pumps_farm_usage = nPlumbing_kits*float(Plumbing_kit[1])/1000  # kW of Pumps
        Pumps_kWh_daily = Pumps_farm_usage*24
        Pumps_daily_cost = Pumps_kWh_daily*energy_price
        
    else:
        System[0] != 'unknown'
        Pumps_daily_cost = 'unknown'
    
    return Pumps_daily_cost



def energy_HVAC(energy_price = None, HVAC = None):  # system design parameters will vary according to location, building and design
    
    Heating = float(HVAC[1, 1])  # power requirements
    Heating_time = float(HVAC[2, 1])
    Heating_consumption = Heating*Heating_time/1000  # kWh per day for heating
    Ventilation = float(HVAC[1, 2])
    Ventilation_time = float(HVAC[2, 2])  # ventilation requirements
    Ventilation_consumption = Ventilation*Ventilation_time/1000  # kWh per day for ventilation
    AC = float(HVAC[1, 3])  # Air-conditioning power requirements
    AC_time = float(HVAC[2,3])
    AC_consumption = AC*AC_time/1000  # kWh per day for air-conditioning
    
    Energy_consumption = Heating_consumption + Ventilation_consumption
    Energy_consumption += AC_consumption  # adding on Air-conditioning
    costs = Energy_consumption*energy_price  # cost per day
    
    return costs


def energy_seedling(Seedling_kit=None, energy_price=None):  # Should be split up into Pump. Lights and hours.
    
    Pumps_kWh_daily = float(Seedling_kit[1, 1])*float(Seedling_kit[2, 1])*float(Seedling_kit[3, 1])/1000 # Quantity*Watts*Hours/1000
    Lights_kWh_daily = float(Seedling_kit[1, 2])*float(Seedling_kit[2, 2])*float(Seedling_kit[3, 2])/1000  # Quantity x Watts x Hours /1000
    
    Seedling_total_kWh = Pumps_kWh_daily + Lights_kWh_daily
    
    daily_cost_seedling = Seedling_total_kWh * energy_price
    
    return daily_cost_seedling


def energy(input_data):
    my_energy_lights = energy_lights(System=input_data.iSystem, Lights=input_data.iLights, ienergy_price=input_data.ienergy_price)
    my_energy_plumbing = energy_plumbing()
    my_energy_climate = energy_climate()
    my_energy_HVAC = energy_HVAC()
    my_energy_seedling = energy_seedling()
    my_energy_pricing = ienergy_price
    size = iSize

    if energy_lights != "unknown": 
        consumption = my_energy_lights + my_energy_plumbing + my_energy_climate + my_energy_HVAC + my_energy_seedling  
        # Daily consumption of energy
    else:
        Energy_Lights = "unknown"
        energy_demand = size*15  # 14-17 kWh per square-metre average energy for hydroponic factory (Xydis et al, 2017)
        consumption = energy_demand * 20  # ASSUME: demand x 20 hours (lights on 18h, climate control & irrigation 24h)
    
    costs = consumption * my_energy_pricing  # daily
    return costs