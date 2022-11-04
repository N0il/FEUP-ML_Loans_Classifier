import pandas as pd

def loadData():
    accounts = pd.read_csv('./../data/account.csv', sep=";")
    cards = pd.read_csv('./../data/card_dev.csv', sep=";")
    clients = pd.read_csv('./../data/client.csv', sep=";")
    dispositions = pd.read_csv('./../data/disp.csv', sep=";")
    districts = pd.read_csv('./../data/district.csv', sep=";")
    loans = pd.read_csv('./../data/loan_dev.csv', sep=";")
    transactions = pd.read_csv('./../data/trans_dev.csv', sep=";", dtype={'trans_id': 'int', 'account_id': 'int', 'date':'int', 'type':'str', 'operation':'str', 'amount':'float', 'balance':'float', 'k_symbol':'str', 'bank':'str', 'account':'str'})

    return (accounts, cards, clients, dispositions, districts, loans, transactions)

(accounts, cards, clients, dispositions, districts, loans, transactions) = loadData()
