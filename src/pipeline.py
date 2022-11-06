from loadData import loadData
from createData import createAgeGroup, createClientGender, createDistrictAvgSalary, createDistrictCriminalityRate, createEffortRate, createSavingsRate
from utils import convertIntDate, createAllExpenses, createClientAge, createLoanExpenses, createSalary, log
from prePocessData import combineFeatures, cleanData, labelEncoding, processZeroSalaries, removeOutliers
import pandas as pd
import numpy as np
from progress.bar import IncrementalBar
import sys
from scipy import stats
from colored import fg, bg, attr
import time
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder

OUTPUT_DATA_PATH = './../data/output/'


def createFeatures(verbose):
    progressBar = IncrementalBar('Creating data...', max=6, suffix='[%(index)d / %(max)d]               ') #, suffix='%(percent)d%%')

    # ================= Loading Data =================

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
    salaries = processZeroSalaries(salaries, districtAvgSalary, True)
    loanExpenses = createLoanExpenses(loans)
    effortRates = createEffortRate(loans, salaries, loanExpenses, districtAvgSalary)
    progressBar.next()

    # client's savings rate
    allExpenses = createAllExpenses(transactions)
    savingsRates = createSavingsRate(allExpenses, loanExpenses, loans, salaries)
    progressBar.next()

    # client's district criminality
    districtCrimeRates = createDistrictCriminalityRate(accounts, districts)
    progressBar.next()

    # =============== Combining Data ===============

    (gendersByLoan, ageGroupByLoan, effortRateByLoan, savingsRateByLoan, distCrimeByLoan, expensesByLoan) = combineFeatures(loans, clients, dispositions, genders, ageGroups, effortRates, savingsRates, districtCrimeRates, allExpenses)
    createdFeatures = pd.DataFrame({'loan_id': loans['loan_id'], 'gender': gendersByLoan, 'ageGroup': ageGroupByLoan, 'effortRate': effortRateByLoan, 'savingsRate': savingsRateByLoan, 'distCrime': distCrimeByLoan, 'expenses': expensesByLoan})
    progressBar.next()

    loansDataFrame = pd.merge(createdFeatures, loans, on="loan_id")

    log('%s \nFinish Creating Data... %s', verbose, True)
    return loansDataFrame


def processFeatures(loansDataFrame, verbose):
    log("Input Data BEFORE Cleaning:\n", verbose)
    log(loansDataFrame.head(), verbose)

    newLoansDataFrame = cleanData(loansDataFrame)
    newLoansDataFrame = labelEncoding(newLoansDataFrame)
    newLoansDataFrame = removeOutliers(newLoansDataFrame)

    log("\nInput Data AFTER Cleaning:\n", verbose)
    log(newLoansDataFrame.head(), verbose)

    log('%s \nFinish Cleaning Data... %s', verbose, True)
    return newLoansDataFrame


def createModel(loansDataFrame, testSize, modelType, verbose):
    # Labels are the values to predict
    labels = np.array(loansDataFrame['status'])

    # Remove the labels from the features
    features = loansDataFrame.drop('status', axis = 1)

    # Saving feature names for later use
    featuresList = list(features.columns)

    # Convert to numpy array
    features = np.array(features)

    # Split the data into training and testing sets
    train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size=testSize, random_state=42)

    log('Training Features Shape:' + str(train_features.shape), verbose)
    log('Training Labels Shape:' + str(train_labels.shape), verbose)
    log('Testing Features Shape:' + str(test_features.shape), verbose)
    log('Testing Labels Shape:' + str(test_labels.shape), verbose)

    if modelType == 'rf':
        # Instantiate model with 1000 decision trees
        model = RandomForestRegressor(n_estimators = 1000, random_state = 42)

    # Train the model on training data
    model.fit(train_features, train_labels)

    log('%s \nFinish Creating and Training Model... %s', verbose, True)
    return (model, test_features, test_labels)


# TODO: incomplete!!
def testModel(model, test_features, test_labels, verbose):
    # Use the model to predict status using the test data
    predictions = model.predict(test_features)

    log('%sFinish Testing Model... %s', verbose, True)

    errors = abs(predictions - test_labels)
    mape = 100 * (errors / test_labels)
    # Calculate and display accuracy
    accuracy = 100 - np.mean(mape)
    log('Accuracy:' + str(round(accuracy, 2)) + '%.', verbose)


def runPipeline(dataFromFile, saveCleanData, testSize, modelType, verbose):
    # =============== Creating Features ===============

    if not dataFromFile:
        loansDataFrame = createFeatures(verbose)
        loansDataFrame.to_csv(OUTPUT_DATA_PATH+'createdData.csv', index=False)
    else:
        loansDataFrame = pd.read_csv(OUTPUT_DATA_PATH+'createdData.csv', sep=",")

    # ================ Cleaning Data ==================

    loansDataFrame = processFeatures(loansDataFrame, verbose)

    if saveCleanData:
        loansDataFrame.to_csv(OUTPUT_DATA_PATH+'createdData_CLEAN.csv', index=False)

    # ================ Creating Model =================

    (model, test_features, test_labels) = createModel(loansDataFrame, testSize, modelType, verbose)

    # ================ Testing Model ==================

    testModel(model, test_features, test_labels, verbose)
