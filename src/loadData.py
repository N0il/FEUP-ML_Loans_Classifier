import datetime
import pandas as pd

from utils import convertIntDate


def loadData(path):
    accounts = pd.read_csv(path+'account.csv', sep=";")
    cards = pd.read_csv(path+'card_dev.csv', sep=";")
    clients = pd.read_csv(path+'client.csv', sep=";")
    dispositions = pd.read_csv(path+'disp.csv', sep=";")
    districts = pd.read_csv(path+'district.csv', sep=";")
    loans = pd.read_csv(path+'loan_dev.csv', sep=";")
    transactions = pd.read_csv(path+'trans_dev.csv', sep=";", dtype={'trans_id': 'int', 'account_id': 'int', 'date':'int', 'type':'str', 'operation':'str', 'amount':'float', 'balance':'float', 'k_symbol':'str', 'bank':'str', 'account':'str'})

    return (accounts, cards, clients, dispositions, districts, loans, transactions)
