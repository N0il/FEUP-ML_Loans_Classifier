from loadData import loadData
from createData import createAgeGroup, createClientGender, createDistrictAvgSalary, createDistrictCriminalityRate, createEffortRate, createSavingsRate
from utils import convertIntDate, createAllExpenses, createClientAge, createLoanExpenses, createSalary, log
from prePocessData import combineFeatures, cleanData, labelEncoding, processZeroSalaries, removeOutliers
from progress.bar import IncrementalBar
import sklearn
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
import numpy as np
"""This file has some exploratory data analysis,
   it is not actually part of our loan classifier module
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from createData import createClientBirthdateRaw, createDistrictAvgSalary
from loadData import loadData
from prePocessData import processZeroSalaries
from utils import convertIntDate, createSalary


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


(accounts, cards, clients, dispositions, districts, loans, transactions) = loadData('./../data/input/')
inputData = [accounts, cards, clients, dispositions, districts, loans, transactions]
inputDataNames = ['accounts', 'cards', 'clients', 'dispositions', 'districts', 'loans', 'transactions']
data = pd.read_csv('../data/output/createdData.csv', sep=",")


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

(accounts, cards, clients, dispositions, districts, loans, transactions) = loadData("../data/input/")
processed_data = pd.read_csv("../data/output/createdData.csv", sep=",")

"""
salaries = createSalary(transactions, 0.8)
# plotData(salaries, 50, 'hist')

fig, ax = plt.subplots()
plt.hist(salaries, 30, rwidth=0.9, color='green')
ax.set_title('Salaries distribution')
ax.set_xlabel("Salaries")
ax.set_ylabel("Number of accounts")
plt.show()
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


def checkBirthVSLoanPeriod(data):
    birthdates = createClientBirthdateRaw(clients)
    loanDates = data['date']

    oldestClient = min(birthdates) # 1911-8-20
    youngerClient = max(birthdates) # 1987-9-27

    minLoan = min(loanDates) # 1993-07-05
    maxLoan = max(loanDates) # 1996-12-27

print("% OF ZERO SALARIES: ", (zeros / total) * 100)"""
print("Min loan: ", minLoan, " Max loan: ", maxLoan)
print("Min client: ", oldestClient, " Max client: ", youngerClient)


print(checkRegionsRepresentedAccounts(accounts, districts), " of the Czech regions are represented by the accounts data (> 50 samples)\n")
loanRegions = checkRegionsRepresentedLoans(loans, accounts, districts)
print(loanRegions[0], " of the Czech regions are represented by the loans data (> 10 samples)\n")
print(loanRegions[1], " of the Czech regions are not represented by the loans data\n")

checkBirthVSLoanPeriod(data)

sns.set(rc={'figure.figsize':(12, 7.5)})
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


# # loan status distribution plot
# fig, ax = plt.subplots()
# ax.bar_label(ax.barh(["1","-1"],loans.status.value_counts()))
# plt.title("Loans' status distribution")
# plt.xlabel("Number of loans")
# plt.ylabel("Status",)
# plt.show()

# progressBar = IncrementalBar('Creating data...', max=6, suffix='[%(index)d / %(max)d]               ') #, suffix='%(percent)d%%')

#     # client's gender
# genders = createClientGender(clients)
# progressBar.next()

# # client's age group
# ages = 1900+(clients['birth_number'] // 10000)
# ageGroups = createAgeGroup(ages)
# progressBar.next()

# # client's effort rate result (above 40 -> yes, below 40% -> no)
# loans['date'] = 1900+(loans['date'] // 10000)
# fig, ax = plt.subplots()
# bins = np.linspace(1900, 2000, 50)
# plt.hist(ages, bins, rwidth=0.9, alpha=0.5, color='red', label="BirthDate")
# plt.hist(loans.date, bins, rwidth=0.9, alpha=0.5, color='green', label="LoanDate")
# plt.legend(loc='upper right')
# ax.set_xlabel('Year')
# ax.set_title('Number of Births and Loans issued over the years')
# ax.legend()

# plt.show()

# print(ages)
# print(loans.date)


# fig, ax = plt.subplots( sharey=True, figsize=(7, 4))
# # fig.subplots_adjust(hspace=0.5, left=0.07, right=0.93)
# hb = ax.hexbin(processed_data.amount, processed_data.payments, gridsize=50, mincnt=1)
# ax.set_title("Frequency Relation of Effort Rate and Loan Value")
# cb = fig.colorbar(hb)
# cb.set_label('counts')
# ax.set_xlabel('Loan Value')
# ax.set_ylabel('Number of payments')
# plt.show()
processed_data.date =[int(date.split("-")[0])+(int(date.split("-")[1])-1+((int(date.split("-")[2])-1)/30))/12 for date in processed_data.date]
# processed_data.date =[int(date.split("-")[0]) for date in processed_data.date]
# df = processed_data[["date","status"]].value_counts()
df1 = processed_data.loc[processed_data['status'] == -1]
df2 = processed_data.loc[processed_data['status'] == 1]
# df1 = df1[["date","status"]].value_counts()
# df2 = df2[["date","status"]].value_counts()
# print(df1, df2)
# df["ratio"] = []


# df1 = processed_data.loc[processed_data['status'] == -1]
# df2 = processed_data.loc[processed_data['status'] == 1]

# fig, ax = plt.subplots( sharey=True, figsize=(7, 4))
# ax.set_title("Loan status in relation to Value and Age")
# plt.scatter(df1.amount, df1.distCrime, alpha=0.5, s=20, linewidths=0, color="red", label="Failed")
# plt.scatter(df2.amount, df2.distCrime, alpha=0.5, s=20, linewidths=0, color="green", label="Succeded")
# # plt.xticks(range(1993,1998))
# ax.set_xlabel('Loan Value')
# ax.set_ylabel("Client's Age")
# plt.legend(loc='upper right')

# plt.show()

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
from sys import argv

# fig = plt.figure()
# ax = Axes3D(fig)
fig, ax = plt.subplots()
# ax.scatter(processed_data.duration, processed_data.amount, processed_data.payments, marker="o")
# ax.scatter(processed_data)
# ax.boxplot(processed_data.amount)
sns.boxplot(data=processed_data.amount, width=.6, palette="vlag")
sns.stripplot(data=processed_data.amount,size=4, palette='dark:.3', linewidth=0)
ax.set_title("Loan value distribution")
# ax.text2D(0.05, 0.95, "Relation between loans's total duration, value and payments", transform=ax.transAxes)
# ax.set_xlabel('Duration')
# ax.set_ylabel('Total Loan Value')
# ax.set_zlabel('Value per Payment')
# fig.colorbar(surf, shrink=0.5, aspect=5)
# plt.savefig('../plots/duration_amount_payments.png')
plt.show()

# df = statFunc(loans[["amount","duration","payments"]])
# df.to_csv("../plots/statistics.csv")

# fig, ax = plt.subplots()
# bins = np.linspace(1993, 1997, 40)
# plt.hist(df1.age, bins, rwidth=0.9, alpha=0.5, color='red', label="female")
# plt.hist(df2.age, bins, rwidth=0.9, alpha=0.5, color='green', label="male")
# plt.legend(loc='upper right')
# ax.set_xlabel('Year')
# ax.set_title('Number of Successful and failed loans over the years')
# ax.legend()

# plt.show()
# print(processed_data.distCrime.value_counts())
sns.distplot(data['savingsRate'], color="maroon")
plt.xlabel("%", labelpad=14)
plt.ylabel("probability of occurence", labelpad=14)
plt.title("Distribution of Clients' savings rate", y=1.015, fontsize=20)
plt.show()

for i in range(len(inputData)):
    print("\n",inputDataNames[i] , ":")
    print("Empty values: ", np.where(inputData[i].applymap(lambda x: x == '?')))
    print("Null values: ", np.where(pd.isnull(inputData[i])))
    print("Number of Null values: ", len(np.where(pd.isnull(inputData[i]))[0]))
    print("Total values: ", len(np.where(inputData[i].applymap(lambda x: x))[0]))

plt.hist(data['ageGroup'], bins=3)
plt.xlabel('age group')
plt.ylabel('absolute frequency')
plt.show()

plt.hist(data['effortRate'], bins=20, color='orange')
plt.xlabel('effort rate')
plt.ylabel('absolute frequency')
plt.show()

plt.hist(data['status'], bins=2)
plt.xlabel('status')
plt.ylabel('absolute frequency')
plt.show()

loans['date'] = loans['date'].apply(convertIntDate)
districtAvgSalary = createDistrictAvgSalary(accounts, districts)
salaries = createSalary(transactions, 0.8)
salaries = processZeroSalaries(salaries, districtAvgSalary, True)

plt.hist(salaries, bins=10)
plt.xlabel('salaries')
plt.ylabel('absolute frequency')
plt.show()

plt.hist(data['expenses'], bins=10, color='orange')
plt.xlabel('expenses')
plt.ylabel('absolute frequency')
plt.show()
