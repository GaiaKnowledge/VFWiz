class Lights(object):

    def __init__(self, light_name, light_height, unit, light_type, light_watts, max_watts, light_spectrum,
                 light_configuration, light_control, light_dimmable, light_cooling, light_efficiency, light_life,
                 light_maintenance_schedule, light_pixels, light_source, light_price, light_currency, light_usage_currency, light_cost_daily,
                 ):

        self.name = light_name
        self.height = light_height  # What is the length of light? what dimensions is it
        self.dimension = unit  # What is the unit of the length?
        self.type = light_type  # LED, HID, etc.
        self.watts = light_watts  # Wattage of lights typically
        self.max_watts = max_watts  # What is the maximum wattage if the light is programmable
        self.spectrum = light_spectrum  # The spectrum selection of the lights
        self.configuration = light_configuration  # Is the spectrum fixed or multiple channels? if so, how many channels?
        self.control = light_control  # Individual side control or multiple for double sided lights?
        self.dimmable = light_dimmable  # Is the lights dimmable from 10-100%?
        self.cooling = light_cooling  # Are they "water" or "air" cooled?
        self.efficiency = light_efficiency  # What is the efficiency of the light? (give a percentage)
        self.life_span = light_life  # What is the life span of the light in hours?
        self.maintenance = light_maintenance_schedule # How often must the lights be serviced?
        self.pixels = light_pixels
        self.source = light_source  # Who is the supplier of the light?
        self.pricing = light_price  # How much do the lights cost?
        self.capital_currency = light_currency  # What currency are you paying for the lights in?
        self.currency = light_usage_currency # What currency is the cost in for usage?
        self.daily_cost = light_cost_daily  # How much does it cost to use the light per day? "(energy_price/1000)*self.watts*time_on
        self.yearly_cost = light_cost_daily*365  # How much does it cost to use the lights per year?
        self.BTU = self.watts*(1-self.efficiency)*3.41  # How much british thermal units (BTUs) of heat does it produce?

    def displayspec(self):
        print('The' + self.type + 'light is' + self.name, "and is" + self.cooling + self.dimmable, "and" +self.configuration, "spectrum"
              "\nIt's height is" + self.height + self.dimension,
              "\nThe power requirement for the light is:" + self.watts, "but can reach a maximum requirement of:" +self.max_watts,
              '\nYou can buy the lights from' + self.source, 'for' + self.currency + self.pricing, "each."
              '\nThe daily cost of using the light, based on your energy pricing, is: £' + self.currency + self.daily_cost
              )
# Intravision

intravision_single_spectra_blade_8ft = Lights("Intravision Single Sided Spectra Blades", 2.4, "metres", "LED", 75, 100,
                                                "UVA 365nm, Purple 410nm, Royal blue 445nm, Green 530nm, "
                                                "Red 630 mn, Deep red 660nm, Fare red 730nm, Cool White,"
                                                "Daylight and Warm White", "2-channel or fixed", "One-side", "Dimmable", "air", 0.40,  #% typical for LEDs
                                                "25000 hours at 25 degrees", 12, "unknown", "Intravision/Zipgrow", 2000, "$", "£", 0.2,
                                                )
intravision_double_spectra_blade_8ft = Lights("Intravision Double Sided Spectra Blades", 2.4, "metres", "LED", 130, 180,
                                                "UVA 365nm nm, Purple 410nm, Royal blue 445nm, Green 530nm, "
                                                "Red 630 mn, Deep red 660nm, Fare red 730nm, Cool White,"
                                                "Daylight and Warm White", "2-channel or fixed", "Individual side-control", "Dimmable", "air", 0.40,  #% typical for LEDs",
                                                "25000 hours at 25 degrees", 12, "unknown", "Intravision/Zipgrow", 3000, "$", "£", 0.4,
                                                )
intravision_double_spectra_blade_5ft2 = Lights("Intravision Double Sided Spectra Blades", 1.6, "metres", "LED", 90, 90,
                                                "UVA 365nm nm, Purple 410nm, Royal blue 445nm, Green 530nm, "
                                                "Red 630 mn, Deep red 660nm, Fare red 730nm, Cool White,"
                                                "Daylight and Warm White", "1-channel fixed", "No control", "Dimmable", "air", 0.40,  #% typical for LEDs"
                                                "25000 hours at 25 degrees", 6, "unknown", "Intravision/Zipgrow", 2000, "$", "£", 0.4,
                                               )

# Liberty Produce Lights

# Valoya  def displayspec(self):

# VARIPAR - PFL Water-Cooled
#
# Colasse VegeLED
