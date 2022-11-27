import numpy as np

from utils import *


# ?possible attribute creation (birthdates)
def createClientBirthdate(clients):
    """_summary_

    Args:
        clients (_type_): _description_

    Returns:
        _type_: _description_
    """
    birthdatesRaw = np.where(clients['birth_number'] % 10000>5000, clients['birth_number']-5000, clients['birth_number'])
    birthdates = map(convertIntDate, birthdatesRaw)
    return birthdates


def createClientBirthdateRaw(clients):
    """_summary_

    Args:
        clients (_type_): _description_

    Returns:
        _type_: _description_
    """
    birthdatesRaw = np.where(clients['birth_number'] % 10000>5000, clients['birth_number']-5000, clients['birth_number'])
    return birthdatesRaw


def createClientGender(clients):
    """_summary_

    Args:
        clients (_type_): _description_

    Returns:
        _type_: _description_
    """
    gender = np.where(clients['birth_number'] % 10000>5000, 'female', 'male')
    return gender


def createAgeGroup(ages):
    """_summary_

    Args:
        ages (_type_): _description_

    Returns:
        _type_: _description_
    """
    ageGroups = list(map(lambda age: 'kid' if age < 18 else ('adult' if age < 60 else 'elderly'), ages))
    return ageGroups


# attribute creation (effort rate)
def createEffortRate(loans, salaries, loanExpenses, districtAvgSalary):
    """_summary_

    Args:
        loans (_type_): _description_
        salaries (_type_): _description_
        loanExpenses (_type_): _description_
        districtAvgSalary (_type_): _description_

    Returns:
        _type_: _description_
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


# attribute creation (savings rate)
def createSavingsRate(allExpenses, loanExpenses, loans, salaries):
    """_summary_

    Args:
        allExpenses (_type_): _description_
        loanExpenses (_type_): _description_
        loans (_type_): _description_
        salaries (_type_): _description_

    Returns:
        _type_: _description_
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


# attribute creation (district average salary) -> or just used as an util
def createDistrictAvgSalary(accounts, districts):
    """_summary_

    Args:
        accounts (_type_): _description_
        districts (_type_): _description_

    Returns:
        _type_: _description_
    """
    avgSalaries = {}

    for _, row in accounts.iterrows():
        for _, distRow in districts.iterrows():
           if(row["district_id"] == distRow["code "]):
                avgSalaries[row["account_id"]] = float(distRow["average salary "])
    return avgSalaries


# attribute creation (district criminality rate)
def createDistrictCriminalityRate(accounts, districts):
    """_summary_

    Args:
        accounts (_type_): _description_
        districts (_type_): _description_

    Returns:
        _type_: _description_
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
