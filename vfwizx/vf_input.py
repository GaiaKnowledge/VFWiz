import numpy as np

class inputContainer(object):
    
    def __init__(self):
        
        self.iName = "UTC"
        self.iLocation = "Liverpool"
        self.iLocation_type = "Urban"  # Urban, Semi-urban or rural
        self.iSize = 20  # square-metres
        self.iStaff = 0  # not sure how many staff or hours
        self.iStart = "01/04/2019"
        self.iType = "Indoor"
        self.iSystem = ['ZipTowers', 21]  # System type, quantity of racks
        self.iLights = ["Example", "water", 210, 200, 18] # Type of Light, cooling type, Qty, Wattage, Hours per day
        self.iPlumbing =['Example', 1800, 45]  # Type of Plumbing kit, wattage, 1 system per X amount of rack units
        self.iClimate = np.array(
                            [['', 'Control System', 'CO2 Injector', 'Dehumidifier', 'Inline Fans'],
                             ['Quantity', 0, 1, 1, 0],
                             ['Watts', 100, 60, 1350, 198],
                             ['Hours on per day', 24,16, 18, 24]]
                            )
        self.iSeedling = np.array(
                             [['', 'Pumps', 'Lights'],
                              ['Quantity', 1, 9],
                              ['Watts', 33, 54],
                              ['Hours on per day', 1, 16]]
                            )
        
        self.iHVAC = np.array(
                         [['', 'Heating', 'Ventilation', 'AC'],
                          ['Watts', 0, 0, 0],
                          ['Hours on per day', 1, 16, 10]]
                         )
        
        self.iAnnual_rent = 23000  # outreach
        self.iRTQ = 80
        self.iwater_price = 3.20/1000  # United utilities £3.20 per 1000 UK litres
        self.iwaterstandingcharge = 63.77  # United utilities £63.77 standing charge
        self.ienergy_price = 0.125  # UK-Power 12.5p per kWH
        self.ienergystandingcharge = 85  # £85 standing charge
        self.itax = 0  # Council tax
        self.iinternet = 0  # Cost of internet per month