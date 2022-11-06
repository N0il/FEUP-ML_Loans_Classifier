from loadData import loadData
from createData import createAgeGroup, createClientGender, createDistrictAvgSalary, createDistrictCriminalityRate, createEffortRate, createSavingsRate
from utils import convertIntDate, createAllExpenses, createClientAge, createLoanExpenses, createSalary
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


def createFeatures():
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

    print ('%s \nFinish Creating Data...\n %s' % (fg(2), attr(1)))
    print ('%s %s' % (fg(0), attr(0)))
    return loansDataFrame


def processFeatures(loansDataFrame):
    print("Input Data BEFORE Cleaning:\n")
    print(loansDataFrame.head())

    newLoansDataFrame = cleanData(loansDataFrame)
    newLoansDataFrame = labelEncoding(newLoansDataFrame)
    newLoansDataFrame = removeOutliers(newLoansDataFrame)

    print("\nInput Data AFTER Cleaning:\n")
    print(newLoansDataFrame.head())

    print ('%s \nFinish Cleaning Data...\n %s' % (fg(2), attr(1)))
    print ('%s %s' % (fg(0), attr(0)))

    return newLoansDataFrame


def createModel(loansDataFrame, testSize, modelType):
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

    print('Training Features Shape:', train_features.shape)
    print('Training Labels Shape:', train_labels.shape)
    print('Testing Features Shape:', test_features.shape)
    print('Testing Labels Shape:', test_labels.shape)

    if modelType == 'rf':
        # Instantiate model with 1000 decision trees
        model = RandomForestRegressor(n_estimators = 1000, random_state = 42)

    # Train the model on training data
    model.fit(train_features, train_labels)

    print ('%s \nFinish Creating and Training Model...\n %s' % (fg(2), attr(1)))
    print ('%s %s' % (fg(0), attr(0)))
    return (model, test_features, test_labels)


# TODO: untested and incomplete!!
def testModel(model, test_features, test_labels):
    # Use the model to predict status using the test data
    predictions = model.predict(test_features)

    print ('%s \nFinish Testing Model...\n %s' % (fg(2), attr(1)))
    print ('%s %s' % (fg(0), attr(0)))

    errors = abs(predictions - test_labels)
    mape = 100 * (errors / test_labels)
    # Calculate and display accuracy
    accuracy = 100 - np.mean(mape)
    print('Accuracy:', round(accuracy, 2), '%.')


def runPipeline(dataFromFile=True, saveCleanData=True, testSize=0.25, modelType='rf'):
    # =============== Creating Features ===============

    if not dataFromFile:
        loansDataFrame = createFeatures()
        loansDataFrame.to_csv(OUTPUT_DATA_PATH+'createdData.csv', index=False)
    else:
        loansDataFrame = pd.read_csv(OUTPUT_DATA_PATH+'createdData.csv', sep=",")

    # ================ Cleaning Data ==================

    loansDataFrame = processFeatures(loansDataFrame)

    if saveCleanData:
        loansDataFrame.to_csv(OUTPUT_DATA_PATH+'createdData_CLEAN.csv', index=False)

    # ================ Creating Model =================

    (model, test_features, test_labels) = createModel(loansDataFrame, testSize, modelType)

    # ================ Testing Model ==================

    testModel(model, test_features, test_labels)
