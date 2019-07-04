import math
from scipy.stats import truncnorm

def market(System=None, Crop = Lettuce):  # REQUIRES CHANGING FOR SCALABILITY

    crop1_split = input("Please enter the % of your farm that is {}:").format(Crop[0])
    r_crop1 = input("Please enter the % of {} that you are selling to retail:").format(Crop[0])
    crop1_retail = int(rmarket_crop1)/100
    rcost_crop1 = input("Please enter the price you would charge retail for this produce per kg:")
    w_crop1 = input("Please enter the % of {} that you are selling to wholesale:").format(Crop[0])
    crop1_wholesale = int(w_crop1)/100
    wcost_crop1 = input("Please enter the price you would charge wholesale for this produce per kg:")

    crop2_split = input("Please enter the % of your farm that is {}:").format(Crop[1])
    r_crop2 = input("Please enter the % of {} that you are selling to retail:").format(Crop[1])
    crop2_retail = int(rmarket_crop2) / 100
    rcost_crop2 = input("Please enter the price you would charge retail for this produce per kg:")
    w_crop2 = input("Please enter the % of {} that you are selling to wholesale:").format(Crop[1])
    crop2_wholesale = int(w_crop2) / 100
    wcost_crop2 = input("Please enter the price you would charge wholesale for this produce per kg:")

    if System[0] == "Ziptower":
        crop1_towers = int(crop1_split) / 100 * System[3]
        crop2_towers = int(crop2_split) / 100 * System[3]
    else:

    return


   """" Adjusted Plant Yield Equation

   Notes
   -----
       Adjusted Plant Yield = Standard Yield x Plant Area x PAR factor
       (ratio of actual PAR delivered to plant canopy compared to theoretical plant requirements. In artificial lighting
       VF the value was 1 as controlled at optimal level. Sun-fed plant level from EcoTect simulation.) x Increment by CO2
       enrichment x Temperature factor (reflects reduction of yield caused by overheating or freezing of the growing area
       if indoor temperature is uncontrolled by HVAC or other systems, value can be set for 0.9 for preliminary estimation)
       Failure rate was set at 5%
   """

a, b = 0.05, 0.15
Fr = truncnorm.rvs(a, b, size=1)

def adjusted_yield(System=none, Crop=none):
    Ya = Ys * Ap * PARf * CO2f * (1-Fr) * Tf

    if System ==

    """" Income per Plant
    
    Notes
    -----
    Plant income = Plant price x Plant index x Adjusted plant yield x plant share rate
    Plant price index is the ratio that the price of products from a VF to the average retail price from the current 
    market was set at 1 if not specified by user. The price share rate is the ratio that the revenue is shared between
    the farm and other marketing process. Introduced to reflect potential cost savings of transporting produce to
    market and from reduction in food supply chain that are significant cost savings but not directly included at this stage.
    If not specified, the price share rate is set at 0.6 approx 3x as high as rural farms, assuming 60% is shared by farm.
    """

def income
    PI = Pp * Pi * Ya * Psr



    # Plant income = Plant price x Plant index x Adjusted plant yield x plant share rate
    # Plant price index is the ratio that the price of products from a VF to the average retail price from the current
    # market was set at 1 if not specified by user. The price share rate is the ratio that the revenue is shared between
    # the farm and other marketing process. Introducted to reflect potential cost savings of transporting produce to
    # market and from reduction in food supply chain that are significant cost savings but not directly included at this stage.
    # If not specified, the price share rate is set at 0.6 approx 3x as high as rural farms, assuming 60% is shared by farm.


def market(input_data):
    my_market = market(System=input_data.iSystem, Crop=input_data.iCrop)

revenue = sales()
