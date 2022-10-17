import numpy as np

from utils import *

# ?possible attribute creation (birthdates)
def createClientBirthdate(clients):
    birthdatesRaw = np.where(clients['birth_number'] % 10000>5000, clients['birth_number']-5000, clients['birth_number'])
    birthdates = map(convertDate, birthdatesRaw)
    return birthdates

def createClientGender(clients):
    gender = np.where(clients['birth_number'] % 10000>5000, 'female', 'male')
    return gender

def createAgeGroup(ages):
    ageGroups = map(lambda age: 'kid' if age < 18 else ('adult' if age < 65 else 'elderly'), ages)
    return ageGroups

# attribute creation (effort rate)
def createEffortRate():
    pass
    # TODO

# attribute creation (savings rate)
def createSavingsRate():
    pass
    # TODO

# attribute creation (district average salary) -> or just used as an util
def createDistrictAvgSalary():
    pass
    # TODO

# attribute creation (district criminality rate)
def createDistrictCriminalityRate():
    pass
    # TODO
