from calendar import month
import numpy as np
import datetime
from dateutil.relativedelta import relativedelta

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

def calculateEndDate(startDate, duration):
    return startDate + relativedelta(months=+duration)

# (creating clients salary) -> maybe use samples (year by year instead of the whole table)
def createSalary(transactions, occurrencesThreshold=0.8):
    # check only monthly recurrent income:
        # 1 - convert all transactions table dates
        # 2 - create a map for each client with an entry for each month (starting in the smallest one found until the furthest one)
        # 3 - create an array of values for each map entry
        # 4 - check values that are recurrent in each array
        # 5 - the sum of the values of the previous step are the salary
        # 6 - also record the period of months to match with the other periods

    # Calculus modes:
        # A -

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

    # 6 TODO: only need the end date (or maybe ignore) if not ignore -> check if loan start date is before the salary end date
    #                                                                -> if it is not consider the district average salary

    values_view = salaries.values()
    value_iterator = iter(values_view)
    first_value = next(value_iterator)

    print(first_value)

    return salaries


# (creating clients total of monthly loans)
def createLoanExpenses(loans):
    # 1 - convert all loan dates
    # 2 - calculate end date
    # 3 - for each loan calculate the total of loans being payed (loans with concurrent periods -> main loan start is before loan being iterated)

    # 1
    loans['date'] = loans['date'].apply(convertIntDate)
    print(loans['date'][0])

    endDates = {}
    # 2
    for index, row in loans.iterrows():
        endDate = calculateEndDate(row['date'], row['duration'])
        endDates[row['loan_id']] = endDate

    loansExpenses = {}

    # 3
    for index, row in loans.iterrows():

        concurrentLoansAmount = row['payments']

        for insideIndex, insideRow in loans.iterrows():
             if index != insideIndex:
                if row['account_id'] == insideRow['account_id']:
                    if endDates[insideRow['loan_id']] < endDates[row['loan_id']]:
                        concurrentLoansAmount += insideRow['payments']


        loansExpenses[row['loan_id']] = (concurrentLoansAmount, row['account_id'])

    # DEBUGGING
    for index, row in loans.iterrows():
        if loansExpenses[row['loan_id']][0] != row['payments']:
            print("HERE: " + str(row['payments']))

    return loansExpenses

# (creating clients total of monthly expenses, excluding loans)
def createAllExpenses(transactions):
    # 1 - convert all dates
    # 2 - sum all negative transactions (withdraws) per month
    # 3 - sum all debits per month (table missing)
    # 4 - make an average of the months

    # 1
    transactions['date'] = transactions['date'].apply(convertIntDate)
    print(transactions['date'][0])

    clientsExpenses = {}

    # 2
    for index, row in transactions.iterrows():
         if row['type'] == 'withdrawal':
            monthYearId = str(row['date'].year) + str(row['date'].month)

            if row['account_id'] not in clientsExpenses:
                months = {}
                months[monthYearId] = row['amount']
                clientsExpenses[row['account_id']] = months
            else:
                if monthYearId not in clientsExpenses[row['account_id']]:
                    clientsExpenses[row['account_id']][monthYearId] = row['amount']
                else:
                    clientsExpenses[row['account_id']][monthYearId] += row['amount']

    values_view = clientsExpenses.values()
    value_iterator = iter(values_view)
    first_value = next(value_iterator)
    print(first_value)

    # 4
    for accountId in clientsExpenses:
        totalAmount = 0
        nMonths = len(clientsExpenses[accountId])

        for monthId in clientsExpenses[accountId]:
            totalAmount += clientsExpenses[accountId][monthId]

        averageAmount = totalAmount / nMonths

        clientsExpenses[accountId] = averageAmount

    values_view = clientsExpenses.values()
    value_iterator = iter(values_view)
    first_value = next(value_iterator)
    print(first_value)

    return clientsExpenses


