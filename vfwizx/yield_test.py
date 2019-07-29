from scipy.stats import truncnorm
import matplotlib.pyplot as plt
import numpy as np

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
no_towers = 225
PARf = 1
CO2f = 1
Tf = 1

# LEAFY GREENS
a, b = 0.05, 0.1
greens_Ys = 3.3 #kg per ziptower harvest
greens_split = 0.5 # Percentage of crops that are leafy greens
# Ap = 162 # number of towers
g_harvest_cycle = 28 # amount of days

# HERBS
c, d = 0.05, 0.1
herbs_split = 0.5 # percentage of crops that are herbs
herbs_Ys = 2 # kg per ziptower harvest
herbs_harvest_cycle = 31.5

gyield_array = []
cg_yield_array = [0]
cg_yield = 0

food = np.array(
[['', 'Control System', 'CO2 Injector', 'Dehumidifier', 'Inline Fans'],
                             ['Quantity', 0, 1, 1, 0],
                             ['Watts', 100, 60, 1350, 198],
                             ['Hours on per day', 24,16, 18, 24]]
                            )

def percentage_of_crop(no_towers, split, harvest_cycle):
    cp = split * no_towers
    towers_per_unit_time = cp/harvest_cycle
    return(towers_per_unit_time)

def adjusted_yield(Ys, Ap, PARf, CO2f, Tf, a, b):
    Fr = truncnorm.rvs(a, b, size=1)
    Ya = Ys * Ap * PARf * CO2f * (1 - Fr) * Tf
    return(Ya)

def annual_yield(Ya):
    return(50*7*Ya)

days = 366

gyield_array = []
cg_yield_array = [0]
cg_yield = 0

hyield_array =[]
ch_yield_array =[0]
ch_yield = 0

for i in range(days):
    gtowers_per_unit_time = percentage_of_crop(no_towers,greens_split,g_harvest_cycle)
    greens_yield = adjusted_yield(greens_Ys, gtowers_per_unit_time, PARf, CO2f, Tf, a, b)
    cg_yield = cg_yield + greens_yield
    gyield_array.append(greens_yield)
    cg_yield_array.append(cg_yield)

    htowers_per_unit_time = percentage_of_crop(no_towers, herbs_split, herbs_harvest_cycle)
    herbs_yield = adjusted_yield(herbs_Ys, htowers_per_unit_time, PARf, CO2f, Tf, c, d)
    ch_yield = ch_yield + herbs_yield
    hyield_array.append(herbs_yield)
    ch_yield_array.append(ch_yield)

gyield_array = np.asarray(gyield_array)
c_ygield_array = np.asarray(cg_yield_array)

hyield_array = np.asarray(hyield_array)
c_hyield_array = np.asarray(hyield_array)

print("Annual yield of leafy greens", float(annual_yield(greens_yield)), "kg")
print("Annual yield of herbs", float(annual_yield(herbs_yield)), "kg")


#  GRAPHS FOR LEAFY GREENS
plt.figure()
plt.plot(gyield_array)
plt.xlabel('Days')
plt.ylabel('Yield (kg)')
plt.show()

plt.figure()
plt.hist(gyield_array)
plt.xlabel('Yield for Leafy Greens (kg)')
plt.ylabel('Frequency')
plt.show()

plt.figure()
plt.plot(cg_yield_array)
plt.xlabel('Days')
plt.ylabel('Cumulative Yield for Leafy Greens (kg)')
plt.show()

# GRAPHS FOR HERBS
plt.figure()
plt.plot(hyield_array)
plt.xlabel('Days')
plt.ylabel('Yield for Herbs (kg)')
plt.show()

plt.figure()
plt.hist(hyield_array)
plt.xlabel('Yield for Herbs (kg)')
plt.ylabel('Frequency')
plt.show()

plt.figure()
plt.plot(ch_yield_array)
plt.xlabel('Days')
plt.ylabel('Cumulative Yield for Herbs (kg)')
plt.show()


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


def income(Pp, Pi, Ya, Psr):
    PI = Pp * Pi * Ya * Psr
    return PI



    # Plant income = Plant price x Plant index x Adjusted plant yield x plant share rate
    # Plant price index is the ratio that the price of products from a VF to the average retail price from the current
    # market was set at 1 if not specified by user. The price share rate is the ratio that the revenue is shared between
    # the farm and other marketing process. Introducted to reflect potential cost savings of transporting produce to
    # market and from reduction in food supply chain that are significant cost savings but not directly included at this stage.
    # If not specified, the price share rate is set at 0.6 approx 3x as high as rural farms, assuming 60% is shared by farm.
