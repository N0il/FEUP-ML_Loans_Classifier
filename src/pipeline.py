import datetime
from loadData import loadData
from createData import createAgeGroup, createClientGender
from utils import convertIntDate, createClientAge, createLoanExpenses, createSalary

# loading all the csv tables
(accounts, cards, clients, dispositions, districts, loans, transactions) = loadData()

# =============== Feature Creation ===============

# client's gender
#genders = createClientGender(clients)

# client's age group
#ages = createClientAge(clients)
#ageGroups = createAgeGroup(ages)

# client's effort rate result (above 40 -> yes, below 40% -> no)
salaries = createSalary(transactions, 0.8)


loanExpenses = createLoanExpenses(loans)

effortRates = {}

for loanId in loanExpenses:
    accountId = loans['account_id'][1]

    if accountId in salaries:
        if salaries[accountId] == 0:
            effortRates[loanId] = 204
        else:
            effortRates[loanId] = (loanExpenses[loanId][0] / salaries[accountId]) * 100
    else:
        effortRates[loanId] = 404

# debugging
for key in effortRates:
    print(effortRates[key])

# client's savings rate
# TODO

# client's district average salary
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
