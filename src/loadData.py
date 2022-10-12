import pandas as pd
import numpy as np
import datetime

CURRENT_EPOCH = 1997

# load data
def loadData():
    accounts = pd.read_csv('data/account.csv', sep=";")
    cards = pd.read_csv('data/card_dev.csv', sep=";")
    clients = pd.read_csv('data/client.csv', sep=";")
    dispositions = pd.read_csv('data/disp.csv', sep=";")
    districts = pd.read_csv('data/district.csv', sep=";")
    loans = pd.read_csv('data/loan_dev.csv', sep=";")
    transactions = pd.read_csv('data/trans_dev.csv', sep=";")

    return (accounts, cards, clients, dispositions, districts, loans, transactions)

# attribute creation
def createClientGender(clients):
    gender = np.where(clients['birth_number'] % 10000>5000, 'Female', 'Male')
    return gender

# attribute creation
def createClientAge(clients):
    ages = (CURRENT_EPOCH % 100) - clients['birth_number'] // 10000
    return ages

# util
def convertDate(date):
    year = '19' + date[:2]
    month = date[2:4]
    day = date[4:]

    result = datetime.datetime(int(year), int(month), int(day))
    return result

# attribute creation
def createClientBirthdate(clients):
    birthdatesRaw = np.where(clients['birth_number'] % 10000>5000, clients['birth_number']-5000, clients['birth_number'])
    birthdates = map(convertDate, birthdatesRaw)
    return birthdates

