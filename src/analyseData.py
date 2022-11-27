from createData import createClientBirthdate, createClientBirthdateRaw, createDistrictAvgSalary
from loadData import loadData
from prePocessData import processZeroSalaries
from utils import convertIntDate, createAllExpenses, createLoanExpenses, createSalary
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import seaborn as sns
import numpy as np


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

def printTable(df, name):
    df.to_csv('../plots/'+name+".csv")

def plotData(dfX, dfY, plotType, name=""):
    if plotType=="bar":
        plt.rcdefaults()
        fig, ax = plt.subplots()

        bars = ax.barh(range(dfX.size), dfX, align='center')
        ax.set_yticks(range(dfY.size), labels=dfY)
        # ax.invert_yaxis()  # labels read top-to-bottom
        # ax.set_title('Top publishers by number of publications')
        # ax.set_xlabel("Number of publications")
        ax.bar_label(bars,label_type="center",color="white")
    elif plotType == "hist":
        plt.hist(dfX, dfY, rwidth=0.9, color='green')
    else:
        print("plotType not available")
        return
    if name == '':
        plt.show()
    else:
        plt.savefig("../plots/"+name+".png", bbox_inches='tight')


""" salaries = createSalary(transactions, 0.8)
plotData(salaries, 50, 'hist');

salariesPdFormat = {}

salariesPdFormat['salary'] = []

for key in salaries:
    salariesPdFormat['salary'].append(salaries[key])

df = pd.DataFrame(salariesPdFormat)

print(df.head())

print(statFunc(df))

total = (df['salary'] == df['salary']).sum()
total = df.count()[0]

zeros = (df['salary'] == 0).sum()

print("NUMBER OF SALARIES: ", total)

print("NUMBER OF ZERO SALARIES: ", zeros)

print("% OF ZERO SALARIES: ", (zeros / total) * 100) """

# loanExpenses = createLoanExpenses(loans)

#print(loans['account_id'].value_counts())

# createAllExpenses(transactions)


#

(accounts, cards, clients, dispositions, districts, loans, transactions) = loadData('./../data/input/')
inputData = [accounts, cards, clients, dispositions, districts, loans, transactions]
inputDataNames = ['accounts', 'cards', 'clients', 'dispositions', 'districts', 'loans', 'transactions']


def checkRegionsRepresentedAccounts(accounts, districts):
    regionsUsed = {}
    numberOfRegions = 77

    for _, row in accounts.iterrows():
        for _, distRow in districts.iterrows():
            if(row["district_id"] == distRow["code "]):
                try:
                    regionsUsed[distRow["code "]] += 1
                except:
                    regionsUsed[distRow["code "]] = 0

    representedRegions = set()

    for key in regionsUsed:
        print(key, " : ", regionsUsed[key])
        if regionsUsed[key] > 50:
            representedRegions.add(key)

    return (len(representedRegions) / numberOfRegions) * 100


def checkRegionsRepresentedLoans(loans, accounts, districts):
    regionsUsed = {}
    numberOfRegions = 77

    for _, row in accounts.iterrows():
        for _, lRow in loans.iterrows():
            if lRow['account_id'] == row['account_id']:
                for _, distRow in districts.iterrows():
                    if(row["district_id"] == distRow["code "]):
                        try:
                            regionsUsed[distRow["code "]] += 1
                        except:
                            regionsUsed[distRow["code "]] = 0

    representedRegions = set()
    notRepresentedRegions = set()

    for key in regionsUsed:
        print(key, " : ", regionsUsed[key])
        if regionsUsed[key] > 10:
            representedRegions.add(key)

    for key in regionsUsed:
        print(key, " : ", regionsUsed[key])
        if regionsUsed[key] == 0:
            notRepresentedRegions.add(key)

    return ((len(representedRegions) / numberOfRegions) * 100, (len(notRepresentedRegions) / numberOfRegions) * 100)

data = pd.read_csv('../data/output/createdData.csv', sep=",")


def checkBirthVSLoanPeriod(data):
    birthdates = createClientBirthdateRaw(clients)
    loanDates = data['date']

    oldestClient = min(birthdates) # 1911-8-20
    youngerClient = max(birthdates) # 1987-9-27

    minLoan = min(loanDates) # 1993-07-05
    maxLoan = max(loanDates) # 1996-12-27

    print("Min loan: ", minLoan, " Max loan: ", maxLoan)
    print("Min client: ", oldestClient, " Max client: ", youngerClient)



# print(checkRegionsRepresentedAccounts(accounts, districts), " of the Czech regions are represented by the accounts data (> 50 samples)\n")
# loanRegions = checkRegionsRepresentedLoans(loans, accounts, districts)
#print(loanRegions[0], " of the Czech regions are represented by the loans data (> 10 samples)\n")
#print(loanRegions[1], " of the Czech regions are not represented by the loans data\n")

# checkBirthVSLoanPeriod(data)

""" sns.set(rc={'figure.figsize':(12, 7.5)})
sns.set_context('talk')

sns.distplot(data['expenses'], color="maroon")
plt.xlabel("koruna", labelpad=14)
plt.ylabel("probability of occurence", labelpad=14)
plt.title("Distribution of Clients' Expenses", y=1.015, fontsize=20)
plt.show()

sns.distplot(data['amount'], color="maroon")
plt.xlabel("koruna", labelpad=14)
plt.ylabel("probability of occurence", labelpad=14)
plt.title("Distribution of Loans' amount", y=1.015, fontsize=20)
plt.show()


sns.distplot(data['savingsRate'], color="maroon")
plt.xlabel("%", labelpad=14)
plt.ylabel("probability of occurence", labelpad=14)
plt.title("Distribution of Clients' savings rate", y=1.015, fontsize=20)
plt.show() """

""" for i in range(len(inputData)):
    print("\n",inputDataNames[i] , ":")
    print("Empty values: ", np.where(inputData[i].applymap(lambda x: x == '?')))
    print("Null values: ", np.where(pd.isnull(inputData[i])))
    print("Number of Null values: ", len(np.where(pd.isnull(inputData[i]))[0]))
    print("Total values: ", len(np.where(inputData[i].applymap(lambda x: x))[0])) """

""" plt.hist(data['ageGroup'], bins=3)
# adding labels
plt.xlabel('age group')
plt.ylabel('absolute frequency')
plt.show() """

""" plt.hist(data['effortRate'], bins=20, color='orange')
# adding labels
plt.xlabel('effort rate')
plt.ylabel('absolute frequency')
plt.show()

plt.hist(data['status'], bins=2)
# adding labels
plt.xlabel('status')
plt.ylabel('absolute frequency')
plt.show() """

""" loans['date'] = loans['date'].apply(convertIntDate)

districtAvgSalary = createDistrictAvgSalary(accounts, districts)
salaries = createSalary(transactions, 0.8)
salaries = processZeroSalaries(salaries, districtAvgSalary, True)

plt.hist(salaries, bins=10)
# adding labels
plt.xlabel('salaries')
plt.ylabel('absolute frequency')
plt.show() """

plt.hist(data['expenses'], bins=10, color='orange')
# adding labels
plt.xlabel('expenses')
plt.ylabel('absolute frequency')
plt.show()