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
    print(loans.head())
    effortRates = {}

    for loanId in loanExpenses:
        for index, row in loans.iterrows():
            if row['loan_id'] == loanId:
                accountId = row['account_id']

        if accountId in salaries:
            if salaries[accountId] == 0:
                print("203")
                effortRates[loanId] = (loanExpenses[loanId][0] / districtAvgSalary[accountId]) * 100
            else:
                print("200")
                effortRates[loanId] = (loanExpenses[loanId][0] / salaries[accountId]) * 100
        else:
            print("404")
            effortRates[loanId] = (loanExpenses[loanId][0] / districtAvgSalary[accountId]) * 100
        # effortRates[loanId] = 1 if effortRates[loanId] <= 40 else 0

    return effortRates


# attribute creation (savings rate)
def createSavingsRate(allExpenses, loanExpenses, loans, salaries):
    savingsRates = {}

    for loanId in loanExpenses:
        for index, row in loans.iterrows():
            if row['loan_id'] == loanId:
                accountId = row['account_id']

        print("AC: ", accountId)

        if accountId in allExpenses:
            savingsRates[loanId] = ((salaries[accountId]-(loanExpenses[loanId][0] + allExpenses[accountId])) / salaries[accountId]) * 100
        else:
            savingsRates[loanId] = ((salaries[accountId]-loanExpenses[loanId][0]) / salaries[accountId]) * 100

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
    progressBar = Bar('Creating Crime Rate', max=accounts.shape[0], suffix='%(percent)d%% - %(eta)ds')
    districtCrimeRates = {}

    for index, row in accounts.iterrows():
        for innerIndex, innerow in districts.iterrows():
            if innerow["no. of commited crimes '95 "] == '?':
                innerow["no. of commited crimes '95 "] = 0
            if innerow["no. of commited crimes '96 "] == '?':
                innerow["no. of commited crimes '96 "] = 0
            if(row["district_id"] == innerow["code "]):
                districtCrimeRates[row["account_id"]] = ((int(innerow["no. of commited crimes '95 "]) + int(innerow["no. of commited crimes '96 "])) / int(innerow["no. of inhabitants"])) * 100
        progressBar.next()
    return districtCrimeRates
