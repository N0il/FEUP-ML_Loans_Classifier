import pandas as pd
import numpy as np
import sys
from scipy import stats
from progress.bar import Bar
from sklearn.preprocessing import LabelEncoder
from utils import log

from utils import convertFullDate


def checkForDuplicates(accounts, cards, clients, dispositions, districts, loans, transactions, verbose):
    # Selecting duplicate rows based
    # on 'account_id' column
    accounts_duplicates = accounts[accounts.duplicated('account_id')].shape[0]
    cards_duplicates = cards[cards.duplicated('card_id')].shape[0]
    clients_duplicates = clients[clients.duplicated('client_id')].shape[0]
    dispositions_duplicates = dispositions[dispositions.duplicated('disp_id')].shape[0]
    districts_duplicates = districts[districts.duplicated('code ')].shape[0]
    loans_duplicates = loans[loans.duplicated('loan_id')].shape[0]
    transactions_duplicates = transactions[transactions.duplicated('trans_id')].shape[0]

    logMessage = "Dataset Duplicates:\nAccounts: "+ str(accounts_duplicates) + "\nCards: " + str(cards_duplicates) + "\nClients: " + str(clients_duplicates) + "\nDispositions: " + str(dispositions_duplicates) + "\nDistricts: " + str(districts_duplicates) + "\nLoans: " + str(loans_duplicates) + "\nTransactions: " + str(transactions_duplicates) + "\n"
    log(logMessage, verbose)
    return


def printDatasetSizes(accounts, cards, clients, dispositions, districts, loans, transactions, verbose):
    accounts_size = accounts.shape[0]
    cards_size = cards.shape[0]
    clients_size = clients.shape[0]
    dispositions_size = dispositions.shape[0]
    districts_size = districts.shape[0]
    loans_size = loans.shape[0]
    transactions_size = transactions.shape[0]

    logMessage = "Dataset Sizes:\nAccounts: "+ str(accounts_size) + "\nCards: " + str(cards_size) + "\nClients: " + str(clients_size) + "\nDispositions: " + str(dispositions_size) + "\nDistricts: " + str(districts_size) + "\nLoans: " + str(loans_size) + "\nTransactions: " + str(transactions_size) + "\n"
    log(logMessage, verbose)
    return


# process all data to correspond to a loan row,
# in order to combine all data with loans table
def combineFeatures(loans, clients, dispositions, genders, ageGroups, effortRates, savingsRates, districtCrimeRates, expenses, ages):
    progressBar = Bar('Features Processing', max=loans.shape[0], suffix='%(percent)d%% - %(eta)ds               ')
    gendersByLoan = []
    ageGroupByLoan = []
    effortRateByLoan = []
    savingsRateByLoan = []
    distCrimeByLoan = []
    expensesByLoan =  []
    agesByLoan = []

    for _, row in loans.iterrows():
        accountId = row['account_id']
        loanId = row['loan_id']
        clientId = None

        # treating genders and ageGroups
        for _, rowDisp in dispositions.iterrows():
            if rowDisp['account_id'] == accountId:
                clientId = rowDisp['client_id']

        if clientId != None:
            indexes = clients.index
            indexesBool = clients['client_id'] == clientId
            clientIndex = indexes[indexesBool][0]

            gendersByLoan.append(genders[clientIndex])
            ageGroupByLoan.append(ageGroups[clientIndex])
            agesByLoan.append(ages[clientIndex])
        else:
            print('ClientId None')

        # treating the rest of the features
        effortRateByLoan.append(effortRates[loanId])
        savingsRateByLoan.append(savingsRates[loanId])
        distCrimeByLoan.append(districtCrimeRates[accountId])
        try:
            expensesByLoan.append(expenses[accountId])
        except KeyError:
            expensesByLoan.append(0)
        progressBar.next()

    return (gendersByLoan, ageGroupByLoan, effortRateByLoan, savingsRateByLoan, distCrimeByLoan, expensesByLoan, agesByLoan)


def cleanData(loansDataFrame):
    print('\nRemoving Redundant Information...')
    columnsToRemove =  ['loan_id', 'account_id']

    noRedundantData = loansDataFrame

    for col in columnsToRemove:
        noRedundantData = noRedundantData.drop(col, axis=1)

    return noRedundantData


# TODO: do the same thing to the categorical data
def removeOutliers(loansDataFrame):
    print('Removing Outliers...\n')
    nonCategoricalColumns = ['savingsRate', 'distCrime', 'amount', 'duration', 'payments', 'expenses']
    totalOutliers = 0

    result = loansDataFrame

    for col in nonCategoricalColumns:
        prevSize = result.shape[0]
        result = result[(np.abs(stats.zscore(result[col])) < 3)]
        size = result.shape[0]
        print('Column  ', col, ' had ', prevSize-size, ' outliers')
        totalOutliers += prevSize-size

    print('Removed a total of  ', totalOutliers, ' outliers')
    return result


def labelEncoding(loansDataFrame):
    print('Encoding data...')
    # gender and ageGroup encoding
    le = LabelEncoder()

    encodedGender = le.fit_transform(loansDataFrame['gender'])
    encodedAgeGroup = le.fit_transform(loansDataFrame['ageGroup'])

    encodedDataFrame = loansDataFrame.drop("gender", axis=1)
    encodedDataFrame = encodedDataFrame.drop("ageGroup", axis=1)

    encodedDataFrame["gender"] = encodedGender
    encodedDataFrame["ageGroup"] = encodedAgeGroup

    # splitting date into year, month, day
    years = []
    months = []
    days = []

    for _, row in encodedDataFrame.iterrows():
        date = convertFullDate(str(row['date']))

        years.append(date.year)
        months.append(date.month)
        days.append(date.day)

    encodedDataFrame = encodedDataFrame.drop("date", axis=1)

    # encodedDataFrame['year'] = years # Year doesn't make sense, because the model is going to be used in future years
    encodedDataFrame['month'] = months
    encodedDataFrame['day'] = days

    return encodedDataFrame


def processZeroSalaries(salaries, districtAvgSalary, substituteWithAvg):
    processedSalaries = {}
    nSalaries = len(salaries)
    nZeroSalaries = 0

    for accountId in salaries:
        if salaries[accountId] == 0:
            nZeroSalaries+=1
            if substituteWithAvg:
                processedSalaries[accountId] = districtAvgSalary[accountId]
            else:
                processedSalaries[accountId] = 1
        else:
            processedSalaries[accountId] = salaries[accountId]

    print("\nNumber of zero salaries: ", nZeroSalaries, " of a total of ", nSalaries)

    return processedSalaries
