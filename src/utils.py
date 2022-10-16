import datetime

CURRENT_EPOCH = 1997

def createClientAge(clients):
    ages = (CURRENT_EPOCH % 100) - clients['birth_number'] // 10000
    return ages

def convertDate(date):
    year = '19' + date[:2]
    month = date[2:4]
    day = date[4:]

    result = datetime.datetime(int(year), int(month), int(day))
    return result

# (creating clients salary)
def createSalary():
    # check only monthly recurrent income:

        # 1 - convert all transactions table dates
        # 2 - create a map for each client with an entry for each month
        # 3 - create an array of values for each map entry
        # 4 - check values that are recurrent in each array
        # 5 - the sum of the values of the previous step are the salary
        # 6 - also record the period of months to match with the other periods
    pass

# (creating clients total of monthly loans)
def createLoansExpenses():
    # 1 - see loan init and end date
    # 2 - sum all of the loans per month
    # 3 - make an average of the months
    pass

# (creating clients total of monthly expenses, including loans)
def createAllExpenses():
    # 1 - sum all negative transactions (withdraws and debits) per month
    # 2 - make and average of the months
    pass
