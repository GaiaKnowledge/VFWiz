class Employee:

    def __init__(self, title, name, pay):
        self.title = title
        self.name = name
        self.pay = pay  # Hourly rate £ per hour

emp_1 = Employee('Farm Hand', 'Nick', 8.21)
emp_2 = Employee('Sales/Account Manager', 'Jayne', 12)
emp_3 = Employee('Business Manager', 'Paul', 18)
emp_4 = Employee('Master Grower', 'Sam', 15)

print(emp_1)
print(emp_2)
print(emp_3)
print(emp_4)

def  emp


def labour(size=iSize, staff=iStaff):  # Very BASIC assumptions based on size from Agrilyst survey 2017

    if staff == 0:
        staff = 0.0155004 * size
        # 0.00144/sq-ft or 0.00007sq-ft for greenhouses
    else:
        staff = staff
    if size < 930:  # square-meters
        wages = 10229.63 * staff  # $13348.60 per person
    else:
        size > 930  # square-metres
        wages = 19866.07 * staff  # $25923.14 per person
    monthly_wages = wages / 12

    return monthly_wages


hourly

labour_wages = labour(iSize, iStaff)
print(labour_wages)
