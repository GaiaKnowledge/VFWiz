
import vf_labour_
import vf_energy
import vf_revenue
import vf_input



input_data = vf_input.inputContainer()

operational_costs = vf_energy.energy(input_data) - water

OpEx: int = 0
# def OpEx(days,Labour,Shipping,Utilities,Rent,Inputs,Packaging,Misc)
days = 365
for i in range(days):
    if i % 30 == 0:
        OpEx += labour(iSize, iStaff)
        OpEx += rent(iAnnual_rent, iSize, iLocation, iLocation_type)
        OpEx += utilitiesM(energy(), water(), internet)
        OpEx += consumables(nutrients, seeds, grow_media)
        OpEx +=
    else:
        i % 365 == 0
    OpEx += annualcosts(ienergystandingcharge, iwaterstandingcharge, itax)

print(OpEx)

# Operations = Bill Growth Lights + Bill Environmental Control + Bill Misc Energy + Water Bill + Seed Cost
# + Nutrient Cost + Personnel Cost + Maintenance Cost + CO2 Cost - Reduction from Renewable Energy
# Inputs = Seeds + Nutrients + Grow Media



print("GOT costs ", costs)