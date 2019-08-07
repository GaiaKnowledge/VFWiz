class Crop(object):

    def __init__(self,crop,iharvest,gharvest,kilos_tower, harvest_weight): # Time to harvest in days, harvest weight at end of cycle
        self.name = crop
        self.iharvest = gharvest # Time to harvest in days for greenhouse
        self.gharvest = iharvest # Time to harvest in days for indoors
        self.zipharvest = zipharvest # Time to harvest based off Zipgrow calculations
        self.standard_yield
        self.kilo_tower = kilos_tower # kilos harvested per zip tower
        self.harvest_weight = harvest_weight # typical weight per crop for harvest
        self.crop_failure_rate = crop_failure_rate # the crop specific percentage or failure of the growing
        self.plant_price = plant_price

        #  AS PER ECONOMIC ESTIMATION SYSTEM FOR VFS - source according to various publications and databases from Shao, Heath and Zhu (2016)

        self.PAR_requirements = PAR_req  # Theoretical PAR requirements
        self.temperature_requirements = temp_req  # Theoretical temperature requirements
        self.seed_cost = seed_cost
        self.PPFD = PPFD  # umol/m2/s
        self.photoperiod_hours = photoperiod_hours
        self.eharvest = days_before_harvest  # as per economic estimation tool
        self.dry_mass = dry_mass_per_plant  # dry mass per plant
        self.dm_fm = dm_fm  # dry mass to fresh mass ratio DM:FM
        self.plants_per_sq_fm = plants_per_sq_m  # Plants/m^2
        self.gross_yield = gross_yield  # kg per sq-m per year
        self.water = water_req  # water requirements Litre per dry-mass kg of plant
        self.fm_per_plant = fm_plant  # fresh mass per plant in kq
        self.water_per_space = water_space  # water use in litres per square metre per year
        self.plant_spacing = plant_spacing  # Plant spacing in m
        self.height = shoot_height  # Height of shoot in metres
        self.root_depth = root_depth  # depth of root
        self.light_use_efficiency = light_efficiency  # Light use efficiency in kg per mol per sq-m
        self.harvest_index = harvest_index  #  Index is the ratio of edible weight to the gross harvest weight


c, d = 0.05, 0.1
herbs_split = 0.5  # percentage of crops that are herbs
herbs_Ys = 2  # kg per ziptower harvest
herbs_harvest_cycle = 31.5

gyield_array = []
cg_yield_array = [0]
cg_yield = 0

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