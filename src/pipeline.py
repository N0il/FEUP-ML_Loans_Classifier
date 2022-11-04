from loadData import loadData
from createData import createAgeGroup, createClientGender, createDistrictAvgSalary, createDistrictCriminalityRate, createEffortRate, createSavingsRate
from utils import convertIntDate, createAllExpenses, createClientAge, createLoanExpenses, createSalary, processFeatures
from analyseData import statFunc
import pandas as pd
from progress.bar import IncrementalBar

progressBar = IncrementalBar('Data Processing', max=6) #, suffix='%(percent)d%%')

from functools import partial
q_25 = partial(pd.Series.quantile, q=0.25)
q_25.__name__ = "25%"
q_75 = partial(pd.Series.quantile, q=0.75)
q_75.__name__ = "75%"

# loading all the csv tables
(accounts, cards, clients, dispositions, districts, loans, transactions) = loadData()

# =============== Feature Creation ===============

# client's gender
genders = createClientGender(clients)
progressBar.next()

# client's age group
ages = createClientAge(clients)
ageGroups = createAgeGroup(ages)
progressBar.next()

# client's effort rate result (above 40 -> yes, below 40% -> no)
loans['date'] = loans['date'].apply(convertIntDate)
districtAvgSalary = createDistrictAvgSalary(accounts, districts)
salaries = createSalary(transactions, 0.8)
loanExpenses = createLoanExpenses(loans)
effortRates = createEffortRate(loans, salaries, loanExpenses, districtAvgSalary)
progressBar.next()

# client's savings rate
allExpenses = createAllExpenses(transactions)
savingsRates = createSavingsRate(allExpenses, loanExpenses, loans, districtAvgSalary)
progressBar.next()

# client's district criminality
districtCrimeRates = createDistrictCriminalityRate(accounts, districts)
progressBar.next()

# ========== Combining and Cleaning Data ==========

(gendersByLoan, ageGroupByLoan, effortRateByLoan, savingsRateByLoan, distCrimeByLoan) = processFeatures(loans, clients, dispositions, genders, ageGroups, effortRates, savingsRates, districtCrimeRates)
createdFeatures = pd.DataFrame({'loan_id': loans['loan_id'], 'Gender': gendersByLoan, 'AgeGroup': ageGroupByLoan, 'EffortRate': effortRateByLoan, 'SavingsRate': savingsRateByLoan, 'DistCrime': distCrimeByLoan})
progressBar.next()

loansDataFrame = pd.merge(createdFeatures, loans, on="loan_id")

# ================ Model Creation =================
# TODO

# ================ Model Testing ==================
# TODO

loansDataFrame.head()

""" # debugging
for key in effortRates:
    print(effortRates[key])

effortPdFormat = {}

effortPdFormat['effortRate'] = []

for key in effortRates:
    effortPdFormat['effortRate'].append(effortRates[key])
    print(effortRates[key])

df = pd.DataFrame(effortPdFormat)

print(df.value_counts())

print(statFunc(df)) """