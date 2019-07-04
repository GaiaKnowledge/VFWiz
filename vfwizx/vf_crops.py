class Crop(object):

    def __init__(self,crop,iharvest,gharvest,kilos_tower, harvest_weight): # Time to harvest in days, harvest weight at end of cycle
        self.name = crop
        self.gharvest = gharvest # Time to harvest in days for greenhouse
        self.iharvest = iharvest # Time to harvest in days for indoors
        self.kilo_tower = kilos_tower # kilos harvested per zip tower
        self.harvest_weight = harvest_weight # typical weight for harvest