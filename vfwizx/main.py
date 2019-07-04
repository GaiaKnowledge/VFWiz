


# import vf_labour_
from vf_energy import energy
#import vf_revenue
from vf_input import inputContainer
import matplotlib.pyplot as plt
import numpy as np
from vf_crops import Crop

input_data = inputContainer()


# LEAFY GREENS
Lettuce = Crop("Lettuce", 3.6 * 7, 5 * 7, 0.453592 * 6.4, 0)  # Harvest times from ZipGrow calculator, Harvest weight per Ziptower
Chard = Crop("Chard", 4.3 * 7, 6 * 7, 0.453592 * 8.8, 0)
Bok_Choy = Crop("Bok Choy", 4.3 * 7, 6 * 7, 0.453592 * 12.8, 0)
Pak_Choi = Crop("Pak Choi", 4.3 * 7, 6 * 7, 0.453592 * 6.4, 0)
Mustard_Greens = Crop("Mustard Greens", 4.3 * 7, 6 * 7, 0.453592 * 6.4, 0)
Kale = Crop("Kale", 4.3 * 7, 6 * 7, 0.453592 * 6.4, 0)
Collards = Crop("Collards", 4.3 * 7, 6 * 7, 0.453592 * 8, 0)

# HERBS
Basil = Crop("Basil", 3.6 * 7, 5 * 7, 0.0283495 * 102.4, 0)
Cilantro = Crop("Cilantro", 4.3 * 7, 6 * 7, 0.0283495 * 76.8, 0)
Oregano = Crop("Oregano", 7.2 * 7, 10 * 7, 0.0283495 * 64, 0)
Fennel = Crop("Fennel", 5.8 * 7, 8 * 7, 0.0283495 * 153.6, 0)
Mint = Crop("Mint", 4.3 * 7, 6 * 7, 0.0283495 * 76.8, 0)
Parsley = Crop("Parsley", 4.3 * 7, 6 * 7, 0.0283495 * 76.8, 0)
Chives = Crop("Chives", 5.8 * 7, 8 * 7, 0.0283495 * 102.4, 0)
Thyme = Crop("Thyme", 5.8 * 7, 8 * 7, 0.0283495 * 51.2, 0)
Lemongrass = Crop("Lemongrass", 4.3 * 7, 6 * 7, 0.0283495 * 64, 0)
Nasturtiums = Crop("Nasturtiums", 2.9 * 7, 4 * 7, 0.0283495 * 19.2, 0)
Tarragon = Crop("Tarragon", 7.2 * 7, 10 * 7, 0.0283495 * 38.4, 0)
Chervil = Crop("Chervil", 3.6 * 7, 5 * 7, 0.0283495 * 108.8, 0)

#operational_costs = vf_energy.energy(input_data)

OpEx: int = 0
OpEx_array = []

# def OpEx(days,Labour,Shipping,Utilities,Rent,Inputs,Packaging,Misc)
days = 366
print("Days",days-1)

for i in range(days):
    if i % 30 == 0:
       # OpEx += labour(iSize, iStaff)  # Fixed costs
       # OpEx += rent(iAnnual_rent, iSize, iLocation, iLocation_type)  # Fixed costs
       OpEx += energy(input_data)
       # OpEx += utilitiesM(energy(), water(), internet)  # Variable costs
       # OpEx += consumables(nutrients, seeds, grow_media)  # Variable costs
       # OpEx += 0
    elif i % 365 == 0:
        OpEx += 2 # annualcosts(ienergystandingcharge, iwaterstandingcharge, iinsurance)  # Fixed costs
    OpEx_array.append(OpEx)

# Operations = Bill Growth Lights + Bill Environmental Control + Bill Misc Energy + Water Bill + Seed Cost
# + Nutrient Cost + Personnel Cost + Maintenance Cost + CO2 Cost - Reduction from Renewable Energy
# Inputs = Seeds + Nutrients + Grow Media


sales: int = 0
# def OpEx(days,Labour,Shipping,Utilities,Rent,Inputs,Packaging,Misc)
sales_array = []

for i in range(days):
    if i % 30 == 0:
        sales += 5 # revenue(input_data.iSystem)
        #Revenue += rent(iAnnual_rent, iSize, iLocation, iLocation_type)
        #Revenue += utilitiesM(energy(), water(), internet)
        #Revenue += consumables(nutrients, seeds, grow_media)
        #Revenue +=
    elif i % 365 == 0:
        sales += 50
    sales_array.append(sales)

sales_array = np.asarray(sales_array)
OpEx_array = np.asarray(OpEx_array)

print("Operational Expenditure: £", OpEx)
print("Sales: £", sales)

profit_array = sales_array - OpEx_array

print("Profit £:",profit_array[-1])

plt.plot(profit_array)
plt.xlabel('Days')
plt.ylabel('Gross Profit')
plt.show()

gross_profit_margin = profit_array / sales_array

plt.figure()
plt.plot(gross_profit_margin)
plt.xlabel('Days')
plt.ylabel('Gross Profit Margin')
plt.show()

print("Gross Profit Margin:",gross_profit_margin[-1])

# print("GOT costs ", costs)