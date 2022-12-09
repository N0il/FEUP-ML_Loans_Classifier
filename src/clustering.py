import matplotlib.pyplot as plt
from pipeline import processFeatures
import seaborn as sns; sns.set()
import numpy as np
from sklearn.cluster import KMeans
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()

OUTPUT_DATA_PATH = './../data/output/'

loansDataFrame = pd.read_csv(OUTPUT_DATA_PATH+'createdData.csv', sep=",")
loansDataFrame = processFeatures(loansDataFrame, False, 'none', 'none')

loansDataFrame = scaler.fit_transform(loansDataFrame[['amount', 'effortRate']])
loansDataFrame = pd.DataFrame(loansDataFrame, columns = ['amount', 'effortRate'])

print(loansDataFrame.head())

inertia = {}

for k in range(1, 10):
    kmeans = KMeans(n_clusters=k ,init="k-means++")
    kmeans = kmeans.fit(loansDataFrame[['amount', 'effortRate']])
    inertia[k] = kmeans.inertia_

plt.plot(inertia.keys(), inertia.values(), 'gs-')
plt.show()

kmeans = KMeans(n_clusters=4 ,init="k-means++")
kmeans = kmeans.fit(loansDataFrame[['amount', 'effortRate']])

loansDataFrame['Clusters'] = kmeans.labels_

print(loansDataFrame.head())

sns.scatterplot(x="amount", y="effortRate",hue = 'Clusters',  data=loansDataFrame)
plt.show()

loansDataFrame2 = pd.read_csv(OUTPUT_DATA_PATH+'createdData.csv', sep=",")
loansDataFrame2 = processFeatures(loansDataFrame2, False, 'none', 'none')

loansDataFrame2 = scaler.fit_transform(loansDataFrame2[['amount', 'effortRate']])
loansDataFrame2 = pd.DataFrame(loansDataFrame2, columns = ['amount', 'effortRate'])

dbscan = DBSCAN(eps = 0.1, min_samples = 5).fit(loansDataFrame2[['amount', 'effortRate']]) # fitting the model
loansDataFrame2['Clusters'] = dbscan.labels_

sns.scatterplot(x="amount", y="effortRate",hue = 'Clusters',  data=loansDataFrame2)
plt.show()
# plt.scatter(loansDataFrame2['amount'], loansDataFrame2['effortRate'], c=labels, cmap= "plasma")
# plt.show()