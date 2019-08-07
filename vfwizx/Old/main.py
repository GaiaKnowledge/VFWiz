


# import vf_labour_
from vf_energy import energy
#import vf_revenue
from vf_input import inputContainer
import matplotlib.pyplot as plt
import numpy as np
from vf_crops import Crop

input_data = inputContainer()

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
       # OpEx += energy(input_data)
       # OpEx += utilitiesM(energy(), water(), internet)  # Variable costs
       # OpEx += consumables(nutrients, seeds, grow_media)  # Variable costs
        OpEx += 40

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
        sales += 9000 # revenue(input_data.iSystem)
        #Revenue += rent(iAnnual_rent, iSize, iLocation, iLocation_type)
        #Revenue += utilitiesM(energy(), water(), internet)
        #Revenue += consumables(nutrients, seeds, grow_media)
        #Revenue +=
    elif i % 365 == 0:
        sales += 50
    sales_array.append(sales)

sales_array = np.asarray(sales_array) # Sales as an array
OpEx_array = np.asarray(OpEx_array)  # OpEx as an array

print("Operational Expenditure: £", OpEx)
print("Sales: £", sales)


def profit(sales_array, OpEx_array):
    profit_array = sales_array - OpEx_array  # Profit = revenue from sales - running costs
    return profit_array

profit_array = profit(sales_array, OpEx_array)

def COGS(consumables, utilitiesM, rent, labour):
    COGS = consumables + utilitiesM + rent + labour
    return

def gross_profit_margin(sales_array, cogs):  # Profit and Cost of Goods Sold - i.e. cost of materials and director labour costs
    gross_profit_margin = (sales_array - cogs)/sales_array # Total revenue - Cost of goods sold (COGS) / revenue
    return gross_profit_margin

# gross_profit_margin(sales_array, cogs)

print("Profit £:",profit_array[-1])

plt.plot(profit_array)
plt.xlabel('Days')
plt.ylabel('Gross Profit')
plt.show()

# plt.figure()
# plt.plot(gross_profit_margin)
# plt.xlabel('Days')
# plt.ylabel('Gross Profit Margin')
# plt.show()
#
# print("Gross Profit Margin:",gross_profit_margin[-1])

# print("GOT costs ", costs)