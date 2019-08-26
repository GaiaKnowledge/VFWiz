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
    saturated_vapour_pressure = 3130.38
    assert abs(calc_saturated_vapour_pressure_air(temp_air) - saturated_vapour_pressure) < 0.01

    
def test_saturated_vapour_pressure_air_FAO():
    temp_air = 25.0
    saturated_vapour_pressure = 3168.81
    assert abs(calc_saturated_vapour_pressure_air_FAO(temp_air) - saturated_vapour_pressure) < 0.01
    

def test_stomatal_resistance():
    ppfd = 140
    ref_stomatal_resistance = 289
    assert abs(calc_stomatal_resistance(ppfd) - ref_stomatal_resistance) < 0.1


def test_stomatal_resistance_null():
    ppfd = 0
    ref_stomatal_resistance = 450
    assert abs(calc_stomatal_resistance(ppfd) - ref_stomatal_resistance) < 0.1





if __name__ == '__main__':
    import sys
    import pytest
    pytest.main([__file__] + sys.argv[1:])