import numpy as np

from utils import *


def createClientBirthdate(clients):
    """Creates clients' birthdates (date objects)

    Args:
        clients (DataFrame): clients data frame

    Returns:
        array: clients' sorted birthdates
    """
    birthdatesRaw = np.where(clients['birth_number'] % 10000>5000, clients['birth_number']-5000, clients['birth_number'])
    birthdates = map(convertIntDate, birthdatesRaw)
    return birthdates


def createClientBirthdateRaw(clients):
    """Creates clients' birthdate (raw date numbers)

    Args:
        clients (DataFrame): clients data frame

    Returns:
        array: clients' sorted birthdates
    """
    birthdatesRaw = np.where(clients['birth_number'] % 10000>5000, clients['birth_number']-5000, clients['birth_number'])
    return birthdatesRaw


def createClientGender(clients):
    """Creates clients' genders

    Args:
        clients (DataFrame): clients data frame

    Returns:
        array: clients' sorted genders
    """
    gender = np.where(clients['birth_number'] % 10000>5000, 'female', 'male')
    return gender


def createAgeGroup(ages):
    """Creates clients' age groups

    Args:
        ages (array): sorted clients' ages

    Returns:
        array: clients' sorted age groups
    """
    ageGroups = list(map(lambda age: 'kid' if age < 18 else ('adult' if age < 60 else 'elderly'), ages))
    return ageGroups


def createEffortRate(loans, salaries, loanExpenses, districtAvgSalary):
    """Creates effort rate (installments / income)

    Args:
        loans (DataFrame): loans data frame
        salaries (dict): salaries by account id
        loanExpenses (dict): loan expenses by account id
        districtAvgSalary (dict): average district salaries by account id

    Returns:
        dict: effort rate by account id
    """
    effortRates = {}

    for loanId in loanExpenses:
        for _, row in loans.iterrows():
            if row['loan_id'] == loanId:
                accountId = row['account_id']

        if accountId in salaries:
            if salaries[accountId] == 0:
                effortRates[loanId] = (loanExpenses[loanId][0] / districtAvgSalary[accountId]) * 100
            else:
                effortRates[loanId] = (loanExpenses[loanId][0] / salaries[accountId]) * 100
        else:
            effortRates[loanId] = (loanExpenses[loanId][0] / districtAvgSalary[accountId]) * 100
        effortRates[loanId] = round(effortRates[loanId], 2)
    return effortRates


def createSavingsRate(allExpenses, loanExpenses, loans, salaries):
    """Creates savings rates ((installments + expenses) / income)

    Args:
        allExpenses (dict): expenses by account id
        loanExpenses (dict): loan installments by account id
        loans (DataFrame): loans data frame
        salaries (dict): salaries by account id

    Returns:
        dict: savings' rates by account id
    """
    savingsRates = {}

    for loanId in loanExpenses:
        for _, row in loans.iterrows():
            if row['loan_id'] == loanId:
                accountId = row['account_id']

        if accountId in allExpenses:
            savingsRates[loanId] = ((salaries[accountId]-(loanExpenses[loanId][0] + allExpenses[accountId])) / salaries[accountId]) * 100
        else:
            savingsRates[loanId] = ((salaries[accountId]-loanExpenses[loanId][0]) / salaries[accountId]) * 100
        savingsRates[loanId] = round(savingsRates[loanId], 2)
    return savingsRates


def createDistrictAvgSalary(accounts, districts):
    """Creates district average salary

    Args:
        accounts (DataFrame): accounts data frame
        districts (DataFrame): districts data frame

    Returns:
        dict: average salary by account id
    """
    avgSalaries = {}

    for _, row in accounts.iterrows():
        for _, distRow in districts.iterrows():
           if(row["district_id"] == distRow["code "]):
                avgSalaries[row["account_id"]] = float(distRow["average salary "])
    return avgSalaries


def createDistrictCriminalityRate(accounts, districts):
    """Creates district criminality rate per person

    Args:
        accounts (DataFrame): accounts data frame
        districts (DataFrame): districts data frame

    Returns:
        dict: district crime rate per person, per account
    """
    progressBar = Bar('Creating Crime Rate', max=accounts.shape[0], suffix='%(percent)d%% - %(eta)ds')
    districtCrimeRates = {}

    for _, row in accounts.iterrows():
        for _, distRow in districts.iterrows():
            if distRow["no. of commited crimes '95 "] == '?':
                distRow["no. of commited crimes '95 "] = 0
            if distRow["no. of commited crimes '96 "] == '?':
                distRow["no. of commited crimes '96 "] = 0
            if(row["district_id"] == distRow["code "]):
                districtCrimeRates[row["account_id"]] = ((int(distRow["no. of commited crimes '95 "]) + int(distRow["no. of commited crimes '96 "])) / int(distRow["no. of inhabitants"])) * 100
                districtCrimeRates[row["account_id"]] = round(districtCrimeRates[row["account_id"]], 2)
        progressBar.next()
    return districtCrimeRates
