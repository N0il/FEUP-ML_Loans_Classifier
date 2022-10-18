from loadData import loadData
from utils import createAllExpenses, createLoanExpenses, createSalary
import pandas as pd

from functools import partial
q_25 = partial(pd.Series.quantile, q=0.25)
q_25.__name__ = "25%"
q_75 = partial(pd.Series.quantile, q=0.75)
q_75.__name__ = "75%"

def statFunc(x):
    stats = x.agg(["mean", "var", "std", "min", q_25, "median", q_75, "max"])
    IQ = (stats.loc["75%"] - stats.loc["25%"])
    stats.loc["lower_limit"] = stats.loc["25%"] - 1.5*IQ
    stats.loc["upper_limit"] = stats.loc["75%"] + 1.5*IQ
    stats.loc["outliers-"] = x[x<stats.loc["lower_limit"]].count()
    stats.loc["outliers+"] = x[x>stats.loc["upper_limit"]].count()
    return stats

(accounts, cards, clients, dispositions, districts, loans, transactions) = loadData()

""" salaries = createSalary(transactions, 0.1)

salariesPdFormat = {}

salariesPdFormat['salary'] = []

for key in salaries:
    salariesPdFormat['salary'].append(salaries[key])

df = pd.DataFrame(salariesPdFormat)

# print(df.head())

print(statFunc(df))

total = (df['salary'] == df['salary']).sum()

zeros = (df['salary'] == 0).sum()

print(total)

print(zeros)

print((zeros / total) * 100)

print(df.count()) """

# loanExpenses = createLoanExpenses(loans)

#print(loans['account_id'].value_counts())

createAllExpenses(transactions)

