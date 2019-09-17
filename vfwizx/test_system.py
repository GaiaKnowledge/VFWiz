# ============================================== SYSTEM AND EXPECTED YIELDS #================================== #


'''
Created on 17 Sep 2019
@author: fbdo
'''
from fbr_maincode import calc_no_of_racks
from fbr_maincode import calc_harvest_weight
from fbr_maincode import get_gross_yield
from fbr_maincode import calc_plant_capacity
from fbr_maincode import get_spec
from fbr_maincode import calc_no_of_lights
from fbr_maincode import get_temp_crop_reqs


def test_no_of_racks_ziprack8():
    grow_system = 'ziprack_8'
    grow_area = 251
    no_of_racks = 54
    assert abs(calc_no_of_racks(grow_system, grow_area) - no_of_racks) < 0.49


def test_harvest_weight():
    crop = 'lettuce'
    harvest_weight = 0.5
    assert abs(calc_harvest_weight(crop) - harvest_weight) == 0


def test_gross_yield():
    """Values taken from: Developing an Economic Estimation Tool for Vertical Farms (Shao et al, 2017)"""
    crop = 'lettuce'
    ref_gross_yield = 78.5  # They state 78.5 kg per m^2 per year is possible in a vertical farm
    assert abs(get_gross_yield(crop) - ref_gross_yield) == 0


def test_plant_capacity():
    """Values taken from: https://www.engineeringtoolbox.com/relative-humidity-air-d_687.html"""
    crop = 'lettuce'
    grow_system = 'ziprack_8'
    no_of_racks = 54

    plant_capacity_yield, plant_capacity_number = calc_plant_capacity(crop, grow_system, no_of_racks)
    ref_plant_capacity_yield = 5346
    ref_plant_capacity_number = xxxx
    assert abs(plant_capacity_yield - ref_plant_capacity_yield) < 0.1


def test_get_spec():
    """Data from experiment 3 from table 1 of paper"""
    temp_air = 21
    relative_humidity = 76
    vapour_concentration_deficit = 4.4
    assert abs(calc_vapour_concentration_deficit(temp_air, relative_humidity) - vapour_concentration_deficit) < 0.1


def test_no_of_lights():
    """Data from experiment 1(A) from table 1 of paper """
    ppfd = 140
    ref_stomatal_resistance = 289
    assert abs(calc_stomatal_resistance(ppfd) - ref_stomatal_resistance) < 1


def test_stomatal_resistance_null():
    ppfd = 0
    ref_stomatal_resistance = 450
    assert abs(calc_stomatal_resistance(ppfd) - ref_stomatal_resistance) < 1


def test_temp_crop_reqs():
    """Data from set A from table 2 of paper"""
    ppfd = 600
    reflection_coefficient = 0.05
    cultivation_area_coverage = 0.95
    net_radiation = calc_net_radiation(ppfd, reflection_coefficient, cultivation_area_coverage)
    assert abs(net_radiation - 108.3) < 0.1