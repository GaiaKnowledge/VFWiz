#!/usr/bin/env python3
'''
Created on 25 Aug 2019

@author: jmht
'''


from vf_hvac import calc_saturated_vapour_pressure_air
from vf_hvac import calc_saturated_vapour_pressure_air_FAO

def test_saturated_vapour_pressure_air1():
    temp_air = 25.0
    saturated_vapour_pressure = 3130.38
    assert abs(calc_saturated_vapour_pressure_air(temp_air) - saturated_vapour_pressure) < 0.01
    
def test_saturated_vapour_pressure_air_FAO():
    temp_air = 25.0
    saturated_vapour_pressure = 3168.81
    assert abs(calc_saturated_vapour_pressure_air_FAO(temp_air) - saturated_vapour_pressure) < 0.01


if __name__ == '__main__':
    import sys
    import pytest
    pytest.main([__file__] + sys.argv[1:])