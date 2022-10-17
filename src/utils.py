from calendar import month
import numpy as np
import datetime

CURRENT_EPOCH = 1997

def createClientAge(clients):
    ages = (CURRENT_EPOCH % 100) - clients['birth_number'] // 10000
    return ages

def convertDate(date):
    year = '19' + date[:2]
    month = date[2:4]
    day = date[4:]

    convertedDate = datetime.datetime(int(year), int(month), int(day))
    return convertedDate

def convertIntDate(date):
    year = '19' + str(date // 10000)
    month = str((date % 10000) // 100)
    day = str(date % 100)

    convertedDate = datetime.datetime(int(year), int(month), int(day))
    return convertedDate

# (creating clients salary) -> maybe use samples (year by year instead of the whole table)
def createSalary(transactions, occurrencesThreshold=0.8):
    # check only monthly recurrent income:
        # 1 - convert all transactions table dates
        # 2 - create a map for each client with an entry for each month (starting in the smallest one found until the furthest one)
        # 3 - create an array of values for each map entry
        # 4 - check values that are recurrent in each array
        # 5 - the sum of the values of the previous step are the salary
        # 6 - also record the period of months to match with the other periods

    # 1
    transactions['date'] = transactions['date'].apply(convertIntDate)
    print(transactions['date'][0])

    # 2 & 3
    clientsIncome = {}

    for index, row in transactions.iterrows():
        if row['type'] == 'credit':
            monthYearId = str(row['date'].year) + str(row['date'].month)

            if row['account_id'] not in clientsIncome:
                months = {}
                amounts = []
                amounts.append(row['amount'])
                months[monthYearId] = amounts
                clientsIncome[row['account_id']] = months
            else:
                if monthYearId not in clientsIncome[row['account_id']]:
                    amounts = []
                    amounts.append(row['amount'])
                    clientsIncome[row['account_id']][monthYearId] = amounts
                else:
                    clientsIncome[row['account_id']][monthYearId].append(row['amount'])

    values_view = clientsIncome.values()
    value_iterator = iter(values_view)
    first_value = next(value_iterator)

    print(first_value)

    # 4 & 5
    salaries = {}

    for accountId in clientsIncome:
        clientRecurrentValues = []

        nMonths = len(clientsIncome[accountId])

        requiredOccurrences = int(nMonths * occurrencesThreshold)

        for monthKey in clientsIncome[accountId]:

            month = clientsIncome[accountId][monthKey]
            clientRecurrentValues += month

        values, counts = np.unique(clientRecurrentValues, return_counts = True)

        salary = 0
        for i in range(len(values)):
            if counts[i] >= requiredOccurrences:
                salary += values[i]

        salaries[accountId] = salary

    values_view = salaries.values()
    value_iterator = iter(values_view)
    first_value = next(value_iterator)

    print(first_value)

    return salaries


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
    # 3 - sum the value from the previous step with the value from the function createLoansExpenses()
    pass
