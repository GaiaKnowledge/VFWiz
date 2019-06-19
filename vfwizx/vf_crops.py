class Crop(object):

    def __init__(self,crop,iharvest,gharvest,kilos_tower): # Time to harvest in days, harvest weight at end of cycle
        self.crop = crop
        self.gharvest = gharvest # Time to harvest in days for greenhouse
        self.iharvest = iharvest # Time to harvest in days for indoors
        self.kilo_tower = kilos_tower # kilos harvested per zip tower

        v1 = Crop("Lettuce", 3.6*7, 5*7, 0.453592*6.4) # Harvest times from ZipGrow calculator, Harvest weight per Ziptower
        v2 = Crop("Chard", 4.3*7, 6*7, 0.453592*8.8)
        v3 = Crop("Bok Choy", 4.3*7, 6*7, 0.453592*12.8)
        v4 = Crop("Pak Choi", 4.3*7, 6*7, 0.453592*6.4)
        v5 = Crop("Mustard Greens", 4.3*7, 6*7, 0.453592*6.4)
        v6 = Crop("Kale", 4.3*7, 6*7, 0.453592*6.4)
        v7 = Crop("Collards", 4.3*7, 6*7, 0.453592*8)


        h1 = Crop("Basil", 3.6*7, 5*7, 0.0283495*102.4)
        h2 = Crop("Cilantro", 4.3*7, 6*7, 0.0283495*76.8)
        h3 = Crop("Oregano", 7.2*7, 10*7, 0.0283495*64)
        h4 = Crop("Fennel", 5.8*7, 8*7, 0.0283495*153.6)
        h5 =  Crop("Mint", 4.3*7, 6*7, 0.0283495*76.8)
        h6 =  Crop("Parsley", 4.3*7, 6*7, 0.0283495*76.8)
        h7 =  Crop("Chives", 5.8*7, 8*7, 0.0283495*102.4)
        h8 =  Crop("Thyme", 5.8*7, 8*7, 0.0283495*51.2)
        h9 =  Crop("Lemongrass", 4.3*7, 6*7, 0.0283495*64)
        h10 =  Crop("Nasturtiums", 2.9*7, 4*7, 0.0283495*19.2)
        h11 = Crop("Tarragon", 7.2*7, 10*7, 0.0283495*38.4)
        h12 = Crop("Chervil", 3.6*7, 5*7, 0.0283495*108.8)