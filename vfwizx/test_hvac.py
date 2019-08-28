#!/usr/bin/env python3
'''
Created on 25 Aug 2019

@author: jmht
'''


from vf_hvac import calc_saturated_vapour_pressure_air
from vf_hvac import calc_saturated_vapour_pressure_air_FAO
from vf_hvac import calc_stomatal_resistance


def test_saturated_vapour_pressure_air1():
    temp_air = 25.0
    saturated_vapour_pressure = 3158
    assert abs(calc_saturated_vapour_pressure_air(temp_air) - saturated_vapour_pressure) < 1

    
def test_saturated_vapour_pressure_air_FAO():
    temp_air = 25.0
    saturated_vapour_pressure = 3168.81
    assert abs(calc_saturated_vapour_pressure_air_FAO(temp_air) - saturated_vapour_pressure) < 1
    

def test_stomatal_resistance():
    ppfd = 140
    ref_stomatal_resistance = 289
    assert abs(calc_stomatal_resistance(ppfd) - ref_stomatal_resistance) < 1


def test_stomatal_resistance_null():
    ppfd = 0
    ref_stomatal_resistance = 450
    assert abs(calc_stomatal_resistance(ppfd) - ref_stomatal_resistance) < 1





if __name__ == '__main__':
    import sys
    import pytest
    #pytest.main([__file__] + sys.argv[1:])
    
    ppfd = 600
    reflection_coefficient = 0.05
    cultivation_area_coverage = 1.0
    net_radiation = 118.8
    #net_radiation = (1 - reflection_coefficient) * ppfd * ppfd2lr * cultivation_area_coverage
    
    ppfd2lr = net_radiation / ((1 - reflection_coefficient) * ppfd * cultivation_area_coverage)
    print(ppfd2lr) # 4155.789