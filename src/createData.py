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
def createDistrictAvgSalary(accounts, districts):
    avgsalaries = {}
    for index, row in accounts.iterrows():
        for innerIndex, innerow in districts.iterrows():
           if(row["district_id"] == innerow["code "]):
                avgsalaries[row["account_id"]] = innerow["average salary "]
    return avgsalaries

# attribute creation (district criminality rate)
def createDistrictCriminalityRate(accounts, districts):
    distCrimeRate = {}
    for index, row in accounts.iterrows():
        for innerIndex, innerow in districts.iterrows():
           if(row["district_id"] == innerow["code"]):
                distCrimeRate[row["account_id"]] = (innerow["no. of commited crimes '95 "] + innerow["no. of commited crimes '96 "]) / innerow["no. of inhabitants "]
    return distCrimeRate
