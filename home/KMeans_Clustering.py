import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import pickle
df = pd.read_csv('person_dataset.csv')

df_subset = df.iloc[:, :14]
'''
wcss = []  # List to hold the WCSS values for different number of clusters

# Range for the number of clusters (1 to 10)
for i in range(1, 20):
    kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=42)
    kmeans.fit(df_subset)
    wcss.append(kmeans.inertia_)  # Inertia: Sum of squared distances of samples to their closest cluster center

# Plotting the elbow graph
plt.figure(figsize=(10, 6))
plt.plot(range(1, 20), wcss, marker='o', linestyle='--')
plt.title('Elbow Method For Optimal Number of Clusters')
plt.xlabel('Number of Clusters')
plt.ylabel('WCSS')  # Within-cluster sum of squares
plt.show()
'''
kmeans = KMeans(n_clusters=7, init='k-means++', max_iter=300, n_init=10, random_state=42)
kmeans.fit(df_subset)

# Add the cluster labels to the DataFrame
df_subset['Cluster'] = kmeans.labels_
cluster_dict = df_subset.groupby('Cluster')['pid'].apply(list).to_dict()
cluster_sizes = {cluster: len(pids) for cluster, pids in cluster_dict.items()}
total_size = sum(cluster_sizes.values())

# Calculate the score ranges for each cluster based on its size
score_ranges = {}
lower_bound = 0.0

for cluster, size in cluster_sizes.items():
    proportion = size / total_size
    upper_bound = lower_bound + proportion
    score_ranges[cluster] = (lower_bound, upper_bound)
    lower_bound = upper_bound

# Print the cluster dictionary and the score ranges
print("Cluster Dictionary:")
print(cluster_dict)
print("\nScore Ranges:")
print(score_ranges)


with open('cluster.pkl', 'wb') as file:
    pickle.dump(kmeans, file)

print("Dictionary saved as 'cluster.pkl'")