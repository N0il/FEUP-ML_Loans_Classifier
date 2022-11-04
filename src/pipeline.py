from loadData import loadData
from createData import createAgeGroup, createClientGender, createDistrictAvgSalary, createDistrictCriminalityRate, createEffortRate, createSavingsRate
from utils import cleanData, convertIntDate, createAllExpenses, createClientAge, createLoanExpenses, createSalary, processFeatures
from analyseData import statFunc
import pandas as pd
import numpy as np
from progress.bar import IncrementalBar
import sys
from scipy import stats

from functools import partial
q_25 = partial(pd.Series.quantile, q=0.25)
q_25.__name__ = "25%"
q_75 = partial(pd.Series.quantile, q=0.75)
q_75.__name__ = "75%"

def runPipeline(dataFromFile=False):

    progressBar = IncrementalBar('Data Processing...     ', max=6) #, suffix='%(percent)d%%')

    # loading all the csv tables
    (accounts, cards, clients, dispositions, districts, loans, transactions) = loadData()

    if not dataFromFile:

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
        createdFeatures = pd.DataFrame({'loan_id': loans['loan_id'], 'gender': gendersByLoan, 'ageGroup': ageGroupByLoan, 'effortRate': effortRateByLoan, 'savingsRate': savingsRateByLoan, 'distCrime': distCrimeByLoan})
        progressBar.next()

        loansDataFrame = pd.merge(createdFeatures, loans, on="loan_id")
        loansDataFrame = cleanData(loansDataFrame)

        loansDataFrame.to_csv('./../data/our/finalData.csv', index=False)
        print("\nFinish Processing Data...:\n")

    else:
        loansDataFrame = pd.read_csv('./../data/our/finalData.csv', sep=",")

    print("Model Input Data:\n")
    print(loansDataFrame.head())
    n= np.abs(stats.zscore(loansDataFrame['amount'])) > 3  # TODO: continue here, only amount outliers where found, still create a proof of concept

    unique, counts = np.unique(n, return_counts=True)
    d= dict(zip(unique, counts))
    print(d)

    # ================ Model Creation =================
    # TODO

    # ================ Model Testing ==================
    # TODO

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

def main(args):
    if len(args) == 1:
        if args[0] == 'True' or args[0] == 'False':
            runPipeline(args[0])
    else:
        print('Usage: pipeline.py [True | False(Default)]\nStates if it runs with data file or generates it in runtime\n')
        runPipeline()

if __name__ == "__main__":
    main(args=sys.argv[1:])
