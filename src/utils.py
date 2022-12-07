import numpy as np
import datetime
from dateutil.relativedelta import relativedelta
from progress.bar import Bar
from colored import fg, attr

CURRENT_EPOCH = 1997


def createClientAge(clients):
    """Creates client age

    Args:
        clients (DataFrame): clients table

    Returns:
        array: ages
    """
    ages = (CURRENT_EPOCH % 100) - clients['birth_number'] // 10000
    return ages


def convertDate(date):
    """Converts partial string date to date object

    Args:
        date (str): date

    Returns:
        Date: date
    """
    year = '19' + date[:2]
    month = date[2:4]
    day = date[4:]

    convertedDate = datetime.datetime(int(year), int(month), int(day))
    return convertedDate


def convertFullDate(date):
    """Converts full date string to Date object

    Args:
        date (str): date

    Returns:
        Date: date
    """
    splitted = date.split("-")

    day = splitted[2]
    if len(day) > 2:
        day = day[0:2]

    convertedDate = datetime.datetime(int(splitted[0]), int(splitted[1]), int(day))
    return convertedDate


def convertIntDate(date):
    """Converts partial date as an integer to Date object

    Args:
        date (int): date

    Returns:
        Date: date
    """
    year = '19' + str(date // 10000)
    month = str((date % 10000) // 100)
    day = str(date % 100)

    convertedDate = datetime.datetime(int(year), int(month), int(day))
    return convertedDate


def calculateEndDate(startDate, duration):
    """Calculates loan end date

    Args:
        startDate (Date): loan start date
        duration (int): loan duration

    Returns:
        Date: loan end date
    """
    return startDate + relativedelta(months=+duration)


def createSalary(transactions, occurrencesThreshold=0.8):
    """Creates clients' salary

    Args:
        transactions (DataFrame): transactions table
        occurrencesThreshold (float, optional): percentage of months on which the same value as to appear to be considered. Defaults to 0.8.

    Returns:
        dict: clients' salaries
    """
    progressBar = Bar('Creating Salaries', max=transactions.shape[0], suffix='%(percent)d%%               ')
    # check only monthly recurrent income:
        # 1 - convert all transactions table dates
        # 2 - create a map for each client with an entry for each month
        # (starting in the smallest one found until the furthest one)
        # 3 - create an array of values for each map entry
        # 4 - check values that are recurrent in each array
        # 5 - the sum of the values of the previous step are the salary

    # 1
    transactions['date'] = transactions['date'].apply(convertIntDate)

    # 2 & 3
    clientsIncome = {}

    for _, row in transactions.iterrows():
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
        progressBar.next()

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
    return salaries


def createLoanExpenses(loans):
    """Creates clients' monthly loan expenses

    Args:
        loans (DataFrame): loans table

    Returns:
        dict: loan monthly expenses by account id
    """
    # 1 - calculate end date
    # 2 - for each loan calculate the total of loans being payed
    # (loans with concurrent periods -> main loan start is before loan being iterated)

    endDates = {}

    # 1
    for index, row in loans.iterrows():
        endDate = calculateEndDate(row['date'], row['duration'])
        endDates[row['loan_id']] = endDate

    loansExpenses = {}

    # 2
    for index, row in loans.iterrows():
        concurrentLoansAmount = row['payments']

        for insideIndex, insideRow in loans.iterrows():
             if index != insideIndex:
                if row['account_id'] == insideRow['account_id']:
                    if endDates[insideRow['loan_id']] < endDates[row['loan_id']]:
                        concurrentLoansAmount += insideRow['payments']

        loansExpenses[row['loan_id']] = (concurrentLoansAmount, row['account_id'])
    return loansExpenses


def createAllExpenses(transactions):
    """Creates clients' monthly expenses, excluding loans

    Args:
        transactions (DataFrame): The transactions table

    Returns:
        dict: expenses by client id
    """
    progressBar = Bar('Creating Expenses', max=transactions.shape[0], suffix='%(percent)d%%               ')
    # 1 - sum all negative transactions (withdraws) per month
    # 2 - make an average of the months

    clientsExpenses = {}

    # 1
    for _, row in transactions.iterrows():
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
        progressBar.next()

    # 2
    for accountId in clientsExpenses:
        totalAmount = 0
        nMonths = len(clientsExpenses[accountId])

        for monthId in clientsExpenses[accountId]:
            totalAmount += clientsExpenses[accountId][monthId]

        averageAmount = totalAmount / nMonths
        clientsExpenses[accountId] = round(averageAmount)
    return clientsExpenses


def log(text, verbose, colored=False):
    """Logs a message to console

    Args:
        text (str): The text to print
        verbose (bool): Controls wether the it should print or not
        colored (bool, optional): Color of the text. Defaults to False.
    """
    if not verbose:
        return
    if colored:
        print(text % (fg(2), attr(1)))
        print('%s %s' % (fg(0), attr(0)))
    else:
        print(text)
