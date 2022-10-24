import datetime
from loadData import loadData
from createData import createAgeGroup, createClientGender, createDistrictAvgSalary
from utils import convertIntDate, createClientAge, createLoanExpenses, createSalary
from analyseData import statFunc
import pandas as pd

from functools import partial
q_25 = partial(pd.Series.quantile, q=0.25)
q_25.__name__ = "25%"
q_75 = partial(pd.Series.quantile, q=0.75)
q_75.__name__ = "75%"

# loading all the csv tables
(accounts, cards, clients, dispositions, districts, loans, transactions) = loadData()

# =============== Feature Creation ===============

# client's gender
#genders = createClientGender(clients)

# client's age group
#ages = createClientAge(clients)
#ageGroups = createAgeGroup(ages)

# client's district average salary
# TODO
districtAvgSalary = createDistrictAvgSalary(accounts, districts)

for id in districtAvgSalary:
    print(districtAvgSalary[id])

# client's effort rate result (above 40 -> yes, below 40% -> no)
salaries = createSalary(transactions, 0.8)
loanExpenses = createLoanExpenses(loans)

effortRates = {}

for loanId in loanExpenses:
    accountId = loans['account_id'][1]

    if accountId in salaries:
        if salaries[accountId] == 0:
            effortRates[loanId] = 204
            effortRates[loanId] = (loanExpenses[loanId][0] / districtAvgSalary[accountId]) * 100
            effortRates[loanId] = 1 if effortRates[loanId] <= 40 else 0
        else:
            effortRates[loanId] = (loanExpenses[loanId][0] / salaries[accountId]) * 100
    else:
        effortRates[loanId] = 404


# debugging
for key in effortRates:
    print(effortRates[key])

effortPdFormat = {}

effortPdFormat['effortRate'] = []

for key in effortRates:
    effortPdFormat['effortRate'].append(effortRates[key])
    print(effortRates[key])

df = pd.DataFrame(effortPdFormat)

print(df.value_counts())

print(statFunc(df))

# client's savings rate
# TODO

# client's district criminality
# TODO

# ================ Combining Data =================
# TODO

# ================ Model Creation =================
# TODO

# ================ Model Testing ==================
# TODO


# DEBUGGING TESTS
# createSalary(transactions)

# createLoanExpenses(loans)
