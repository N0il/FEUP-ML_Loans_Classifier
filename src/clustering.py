"""This module is used to execute the clustering data mining task"""


import matplotlib.pyplot as plt
from pipeline import processFeatures
import seaborn as sns; sns.set()
import numpy as np
from sklearn.cluster import KMeans
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors 
scaler = StandardScaler()

OUTPUT_DATA_PATH = './../data/output/'

loansDataFrame = pd.read_csv(OUTPUT_DATA_PATH+'createdData.csv', sep=",")
loansDataFrame = processFeatures(loansDataFrame, False, 'none', 'none')

loansDataFrame = scaler.fit_transform(loansDataFrame[['amount', 'effortRate']])
loansDataFrame = pd.DataFrame(loansDataFrame, columns = ['amount', 'effortRate'])

print(loansDataFrame.head())

# ploting the elbow curve for k-means to find the point of diminishing returns of the k variable
inertia = {}
for k in range(1, 10):
    kmeans = KMeans(n_clusters=k ,init="k-means++")
    kmeans = kmeans.fit(loansDataFrame[['amount', 'effortRate']])
    inertia[k] = kmeans.inertia_
plt.plot(inertia.keys(), inertia.values(), 'gs-')
plt.show()

# best k-means plot
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


# Generate elbow plot of distance to neighbours to find the point of diminishing returns for the dbscan max distance
neighbors = NearestNeighbors(n_neighbors=20)
neighbors_fit = neighbors.fit(loansDataFrame2)
distances, indices = neighbors_fit.kneighbors(loansDataFrame2)

distances = np.sort(distances, axis=0)
distances = distances[:,1]
plt.plot(distances)
plt.show()
    

# We looped through some values of min_samples and eps close to the found point of diminishing returns to find the best clusterings 
"""
for m in range(6,8):
    print(m)
    eps_range=[x/100.0 for x in range(20,23)]
    for e in eps_range:
        dbscan = DBSCAN(eps = e, min_samples = m).fit(loansDataFrame2[['amount', 'effortRate']]) # fitting the model
        loansDataFrame2['Clusters'] = dbscan.labels_
        plt.title(f"min_samples={m} and eps={e}")
        sns.scatterplot(x="amount", y="effortRate",hue = 'Clusters',  data=loansDataFrame2)
        plt.show()
"""

# Here is one of the dbscan clusterings with the best separation
dbscan = DBSCAN(eps = 0.21, min_samples = 6).fit(loansDataFrame2[['amount', 'effortRate']]) # fitting the model
loansDataFrame2['Clusters'] = dbscan.labels_

sns.scatterplot(x="amount", y="effortRate",hue = 'Clusters',  data=loansDataFrame2)
plt.show()
