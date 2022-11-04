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
    ageGroups = list(map(lambda age: 'kid' if age < 18 else ('adult' if age < 65 else 'elderly'), ages))
    return ageGroups

# attribute creation (effort rate)
def createEffortRate(loans, salaries, loanExpenses, districtAvgSalary):
    effortRates = {}

    for loanId in loanExpenses:
        accountId = loans['account_id'][1]

        if accountId in salaries:
            if salaries[accountId] == 0:
                effortRates[loanId] = (loanExpenses[loanId][0] / districtAvgSalary[accountId]) * 100
            else:
                effortRates[loanId] = (loanExpenses[loanId][0] / salaries[accountId]) * 100
        else:
            effortRates[loanId] = (loanExpenses[loanId][0] / districtAvgSalary[accountId]) * 100
        effortRates[loanId] = 1 if effortRates[loanId] <= 40 else 0

    return effortRates


# attribute creation (savings rate)
def createSavingsRate(allExpenses, loanExpenses, loans, districtAvgSalary):
    savingsRates = {}

    for loanId in loanExpenses:
        accountId = loans['account_id'][1]

        if accountId in allExpenses:
            savingsRates[loanId] = (1-((loanExpenses[loanId][0] + allExpenses[accountId]) / districtAvgSalary[accountId])) * 100
        else:
            savingsRates[loanId] = (1-(loanExpenses[loanId][0] / districtAvgSalary[accountId])) * 100

    return savingsRates

# attribute creation (district average salary) -> or just used as an util
def createDistrictAvgSalary(accounts, districts):
    avgSalaries = {}

    for index, row in accounts.iterrows():
        for innerIndex, innerow in districts.iterrows():
           if(row["district_id"] == innerow["code "]):
                avgSalaries[row["account_id"]] = float(innerow["average salary "])
    return avgSalaries

# attribute creation (district criminality rate)
def createDistrictCriminalityRate(accounts, districts):
    districtCrimeRates = {}

    for index, row in accounts.iterrows():
        for innerIndex, innerow in districts.iterrows():
            if innerow["no. of commited crimes '95 "] == '?':
                innerow["no. of commited crimes '95 "] = 0
            if innerow["no. of commited crimes '96 "] == '?':
                innerow["no. of commited crimes '96 "] = 0
            if(row["district_id"] == innerow["code "]):
                districtCrimeRates[row["account_id"]] = (int(innerow["no. of commited crimes '95 "]) + int(innerow["no. of commited crimes '96 "])) / int(innerow["no. of inhabitants"])
    return districtCrimeRates
