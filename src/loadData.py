import datetime
import pandas as pd

from utils import convertIntDate

INPUT_DATA_PATH = './../data/input/'


def loadData():
    accounts = pd.read_csv(INPUT_DATA_PATH+'account.csv', sep=";")
    cards = pd.read_csv(INPUT_DATA_PATH+'card_dev.csv', sep=";")
    clients = pd.read_csv(INPUT_DATA_PATH+'client.csv', sep=";")
    dispositions = pd.read_csv(INPUT_DATA_PATH+'disp.csv', sep=";")
    districts = pd.read_csv(INPUT_DATA_PATH+'district.csv', sep=";")
    loans = pd.read_csv(INPUT_DATA_PATH+'loan_dev.csv', sep=";")
    transactions = pd.read_csv(INPUT_DATA_PATH+'trans_dev.csv', sep=";", dtype={'trans_id': 'int', 'account_id': 'int', 'date':'int', 'type':'str', 'operation':'str', 'amount':'float', 'balance':'float', 'k_symbol':'str', 'bank':'str', 'account':'str'})

    return (accounts, cards, clients, dispositions, districts, loans, transactions)
