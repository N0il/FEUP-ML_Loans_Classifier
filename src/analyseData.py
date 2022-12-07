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

print("% OF ZERO SALARIES: ", (zeros / total) * 100)"""

# loanExpenses = createLoanExpenses(loans)

#print(loans['account_id'].value_counts())

# createAllExpenses(transactions)





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