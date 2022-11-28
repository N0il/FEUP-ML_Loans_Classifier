from loadData import loadData
from createData import createAgeGroup, createClientGender, createDistrictAvgSalary, createDistrictCriminalityRate, createEffortRate, createSavingsRate
from utils import convertIntDate, createAllExpenses, createClientAge, createLoanExpenses, createSalary, log
from prePocessData import checkForDuplicates, combineFeatures, cleanData, labelEncoding, printDatasetSizes, processZeroSalaries, removeOutliers

import pandas as pd
import numpy as np
from progress.bar import IncrementalBar
from progress.bar import Bar
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn import svm
from sklearn.naive_bayes import GaussianNB
from sklearn.feature_selection import RFE
from sklearn.linear_model import Perceptron
from imblearn.over_sampling import SMOTE
from collections import Counter
import csv
import re

OUTPUT_DATA_PATH = './../data/output/'


def createFeatures(verbose, path):
    """Wrapper function for all the feature engineering

    Args:
        verbose (bool): control console logs
        path (str): path of the original input data

    Returns:
        DataFrame: features created merged with the loans table
    """
    progressBar = IncrementalBar('Creating data...', max=6, suffix='[%(index)d / %(max)d]               ') #, suffix='%(percent)d%%')

    # ================= Loading Data =================

    (accounts, cards, clients, dispositions, districts, loans, transactions) = loadData(path)
    checkForDuplicates(accounts, cards, clients, dispositions, districts, loans, transactions, verbose)
    printDatasetSizes(accounts, cards, clients, dispositions, districts, loans, transactions, verbose)

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

    (gendersByLoan, ageGroupByLoan, effortRateByLoan, savingsRateByLoan, distCrimeByLoan, expensesByLoan, agesByLoan) = combineFeatures(loans, clients, dispositions, genders, ageGroups, effortRates, savingsRates, districtCrimeRates, allExpenses, ages)
    createdFeatures = pd.DataFrame({'loan_id': loans['loan_id'], 'gender': gendersByLoan, 'ageGroup': ageGroupByLoan, 'effortRate': effortRateByLoan, 'savingsRate': savingsRateByLoan, 'distCrime': distCrimeByLoan, 'expenses': expensesByLoan, 'age': agesByLoan})
    progressBar.next()

    loansDataFrame = pd.merge(createdFeatures, loans, on="loan_id")

    log('%s \nFinish Creating Data... %s', verbose, True)
    return loansDataFrame


def processFeatures(loansDataFrame, verbose, sampleByAge, sampleByYear, removeOutliersOn=True):
    """Wrapper function for all the data pre processing

    Args:
        loansDataFrame (DatFrame): the DataFrame created in createFeatures function
        verbose (bool): control console logs
        sampleByAge (str): controls sampling by age
        sampleByYear (str): controls sampling by year
        removeOutliersOn (bool, optional): controls outliers removal. Defaults to True.

    Returns:
        DataFrame: clean data frame
    """
    log("Input Data BEFORE Cleaning:\n", verbose)
    log(loansDataFrame.head(), verbose)

    newLoansDataFrame = cleanData(loansDataFrame)

    if sampleByYear != 'none':
        year = sampleByYear + '01-01'
        log("Sampling over year: " + sampleByYear, verbose)
        indexYear1 = newLoansDataFrame[(newLoansDataFrame['date'] > year)].index
        newLoansDataFrame = newLoansDataFrame.drop(indexYear1)

    newLoansDataFrame = labelEncoding(newLoansDataFrame)
    if removeOutliersOn:
        newLoansDataFrame = removeOutliers(newLoansDataFrame)

    if sampleByAge != 'none':
        ages = sampleByAge.split("-")
        lowAge = int(ages[0])
        highAge = int(ages[1])

        log("\nSampling over age: " + sampleByAge, verbose)

        indexAge1 = newLoansDataFrame[(newLoansDataFrame['age'] > highAge) ].index
        indexAge2 = newLoansDataFrame[(newLoansDataFrame['age'] < lowAge) ].index
        newLoansDataFrame = newLoansDataFrame.drop(indexAge1)
        newLoansDataFrame = newLoansDataFrame.drop(indexAge2)

    log("\nInput Data AFTER Cleaning:\n", verbose)
    log(newLoansDataFrame.head(), verbose)

    log('%s \nFinish Cleaning Data... %s', verbose, True)
    return newLoansDataFrame


def featureSelectionRank(model, labels, features, verbose):
    """Outputs the features ranking

    Args:
        model (model): model to be used with RFE
        labels (array): labels
        features (array): features
        verbose (bool): control console logs

    Returns:
        array: features ranking
    """
    selector = RFE(model, n_features_to_select=1)
    selector = selector.fit(features, labels)
    log('\nFeature Ranking: {rank}\n'.format(rank=selector.ranking_), verbose)

    return selector.ranking_


def trainModel(model, train_features_imbalanced, train_labels_imbalanced, verbose, balance, testFeatures, selectNFeatures, modelType):
    """_summary_

    Args:
        model (model): the model object
        train_features_imbalanced (array): train features
        train_labels_imbalanced (array): train labels
        verbose (bool): control console logs
        balance (bool): control balancing
        testFeatures (array): test features to trim
        selectNFeatures (int): number of features to select
        modelType (str): model to use

    Returns:
        tuple: model object and trimmed test features
    """
    # Data balancing
    if balance:
        smote = SMOTE(random_state = 14)
        train_features, train_labels = smote.fit_resample(train_features_imbalanced, train_labels_imbalanced)
        log('%sFinish balancing data... %s', verbose, True)
        log('Balanced dataset shape: {count}\n'.format(count=Counter(train_labels)), verbose)
    else:
        train_features = train_features_imbalanced
        train_labels = train_labels_imbalanced
        log('Imbalanced dataset shape: {count}\n'.format(count=Counter(train_labels)), verbose)

    if not (modelType== 'svm' or modelType=='naive'):
        progressBar = Bar('Selecting Features', max=len(train_features[0]), suffix='%(percent)d%% - %(eta)ds               ')

        bestAuc = 0
        bestMask = []
        intermediaryAUCs = []

        if selectNFeatures == 99: # never used value
            # Test model against multiple features groups
            for i in range(len(train_features[0])):
                selector = RFE(model, n_features_to_select=(len(train_features[0])-i))
                selector = selector.fit(train_features, train_labels)
                mask = selector.support_

                features = []
                for r in range(len(train_features)):
                    row = []
                    for c in range(len(train_features[r])):
                        if mask[c]:
                            row.append(train_features[r][c])
                    features.append(row)

                # Train the model on training data
                model.fit(features, train_labels)
                if modelType == 'pr':
                    predictions = model._predict_proba_lr(features)
                else:
                    predictions = model.predict_proba(features)
                aucScore = roc_auc_score(train_labels, predictions[:, 1]) * 100
                intermediaryAUCs.append(aucScore)

                # update best score and mask
                if aucScore > bestAuc:
                    bestAuc = aucScore
                    bestMask = mask

                progressBar.next()
        else:
            selector = RFE(model, n_features_to_select=selectNFeatures)
            selector = selector.fit(train_features, train_labels)
            bestMask = selector.support_

        if intermediaryAUCs != []:
            interAUCsString = ' | '.join([str(elem) for elem in intermediaryAUCs])
            log("\n\nIntermediary AUC's: \n" + interAUCsString + "\n", verbose)

        # Train with the selected features
        features = []

        for r in range(len(train_features)):
            row = []
            for c in range(len(bestMask)):
                if bestMask[c]:
                    row.append(train_features[r][c])
            features.append(row)

        # Trim the test features accordingly
        trimmedTestFeatures = []

        for r in range(len(testFeatures)):
            testRow = []
            for c in range(len(bestMask)):
                if bestMask[c]:
                    testRow.append(testFeatures[r][c])
            trimmedTestFeatures.append(testRow)

        # Train the model on training data
        model.fit(features, train_labels)
    else:
        model.fit(train_features, train_labels)
        return (model, testFeatures)

    featuresMaskString = ' | '.join([str(elem) for elem in bestMask])
    log('Features after selection:\n' + featuresMaskString, verbose)
    return (model, trimmedTestFeatures)


def createModel(loansDataFrame, trainSize, modelType, verbose, balance, selectNFeatures, randomState, testMode, parameters):
    """_summary_

    Args:
        loansDataFrame (_type_): _description_
        trainSize (_type_): _description_
        modelType (_type_): _description_
        verbose (_type_): _description_
        balance (_type_): _description_
        selectNFeatures (_type_): _description_
        randomState (_type_): _description_
        testMode (_type_): _description_
        parameters (_type_): _description_

    Returns:
        _type_: _description_
    """
    # Labels are the values to predict
    labels = np.array(loansDataFrame['status'])

    # Remove the labels from the features
    features = loansDataFrame.drop('status', axis = 1)

    # Saving feature names for later use
    featuresList = list(features.columns)

    featuresString = ' | '.join([str(elem) for elem in featuresList])
    log('Features before selection:\n' + featuresString, verbose)

    # Convert to numpy array
    features = np.array(features)

    if randomState == 0:
        randomState = None

    # Split the data into training and testing sets
    if testMode == 'none':
        train_features, test_features, train_labels, test_labels = train_test_split(features, labels, train_size=trainSize, random_state=randomState)
    else:
        # train data
        train_features = features
        train_labels = labels

        # test data
        dataFrame = pd.read_csv(testMode, sep=",")
        processedDataFrame = processFeatures(dataFrame, False, 'none', 'none', False)
        test_features = processedDataFrame.drop('status', axis = 1).to_numpy()
        test_labels = []

    log('\nTraining Features Shape:' + str(train_features.shape), verbose)
    log('Training Labels Shape:' + str(train_labels.shape), verbose)
    log('Testing Features Shape:' + str(test_features.shape), verbose)
    if test_labels != []:
        log('Testing Labels Shape:' + str(test_labels.shape), verbose)

    # Handle inputted parameters
    if parameters ==  None or len(parameters) < 3:
        log('\nUsing default parameters', verbose)
        nEstimators = 100
        randomState = None
        maxDepth = None
        Solver = 'lbfgs'
        c = 1.0
        Penalty = 'l2'
    else:
        if modelType == 'rf' or modelType == 'gb':
            nEstimators = int(parameters[0])
            if parameters[1] == 'None':
                randomState = None
            else:
                randomState = int(parameters[1])
            if parameters[2] == 'None':
                maxDepth = None
            else:
                maxDepth = int(parameters[2])
        elif modelType == 'lr':
            Solver = parameters[0]
            c = float(parameters[0])
            Penalty = parameters[0]

    if modelType == 'rf':
        model = RandomForestClassifier(n_estimators=nEstimators, random_state=randomState, max_depth=maxDepth)
    elif modelType == 'lr':
        model = LogisticRegression(solver=Solver, C=c, penalty=Penalty, max_iter=1000)
    elif modelType == 'gb':
        model = GradientBoostingClassifier(n_estimators=nEstimators, learning_rate=1.0, max_depth=maxDepth, random_state=randomState)
    elif modelType == 'dt':
        model = DecisionTreeClassifier()
    elif modelType == 'pr':
        model = Perceptron(tol=1e-3, random_state=0)
    elif modelType == 'svm': # doesn't support RFE
        model = svm.SVC(probability=True, kernel='poly')
    elif modelType == 'naive': # doesn't support RFE
        model = GaussianNB()
    else:
         print("\nModel Not Detected!\n")
         exit()

    # Show features ranking
    if not (modelType== 'svm' or modelType=='nn' or modelType=='naive'):
        featureSelectionRank(model, labels, features, verbose)

    # Feature selection and training model
    (model, trimmed_test_features) = trainModel(model, train_features, train_labels, verbose, balance, test_features, selectNFeatures, modelType)

    log('%s \nFinish Creating and Training Model... %s', verbose, True)
    return (model, trimmed_test_features, test_labels)


#TODO: crete this function, also check this RepeatedKFold
# evaluate a give model using cross-validation
""" def crossValidation(model, X, y):
	cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)
	scores = cross_val_score(model, X, y, scoring='accuracy', cv=cv, n_jobs=-1)
	return scores
 """


def testModel(model, test_features, test_labels, verbose, modelType):
    """_summary_

    Args:
        model (_type_): _description_
        test_features (_type_): _description_
        test_labels (_type_): _description_
        verbose (_type_): _description_
        modelType (_type_): _description_
    """
    # Use the model to predict status using the test data
    if modelType == 'pr':
        predictions = model._predict_proba_lr(test_features)
    else:
        predictions = model.predict_proba(test_features)


    classesOrderString = ' '.join([str(elem) for elem in model.classes_])

    log("Classes order: "+classesOrderString+"\n", verbose)

    with open(OUTPUT_DATA_PATH+"predictions"+"_"+type(model).__name__+".csv","w+", newline='',) as my_csv:
        csvWriter = csv.writer(my_csv, delimiter=',')
        csvWriter.writerows(predictions)

    log('%sFinish Testing Model... %s', verbose, True)

    # roc curve for models
    if test_labels !=  []:
        aucScore = roc_auc_score(test_labels, predictions[:, 1]) * 100

        log('AUC: {auc:.0f}%'.format(auc=aucScore), verbose)


def runPipeline(dataFromFile, saveCleanData, trainSize, modelType, verbose, balance, selectNFeatures, path, createdDataName, randomState, testMode, sampleByAge, sampleByYear, parameters):
    """Main module function, runs the entire ML pipeline according to the arguments given

    Args:
        dataFromFile (bool): to get data from file, instead having to create it
        saveCleanData (bool): to save data after pre processing
        trainSize (int): train data percentage
        modelType (str): states the model to be used
        verbose (bool): controls verbose mode
        balance (bool): controls data balancing
        selectNFeatures (int): number of features to select
        path (str): path of the train data
        createdDataName (str): name of the data file created
        randomState (int): split test train random state
        testMode (str): path to test data, or none
        sampleByAge (str): age to sample data with, or none
        sampleByYear (str): years to sample data with, or none
        parameters (array): list of hyper-parameters
    """
    createdDataFile = re.sub('\..*$', '', createdDataName) # used to remove file name extensions

    # =============== Creating Features ===============

    if not dataFromFile:
        loansDataFrame = createFeatures(verbose, path)
        loansDataFrame.to_csv(OUTPUT_DATA_PATH+createdDataFile+'.csv', index=False)
    else:
        loansDataFrame = pd.read_csv(OUTPUT_DATA_PATH+createdDataFile+'.csv', sep=",")

    # ================ Cleaning Data ==================

    loansDataFrame = processFeatures(loansDataFrame, verbose, sampleByAge, sampleByYear)

    if saveCleanData:
        loansDataFrame.to_csv(OUTPUT_DATA_PATH+'createdData_CLEAN.csv', index=False)

    # ================ Creating Model =================

    (model, test_features, test_labels) = createModel(loansDataFrame, trainSize, modelType, verbose, balance, selectNFeatures, randomState, testMode, parameters)

    # ================ Testing Model ==================

    testModel(model, test_features, test_labels, verbose, modelType)
