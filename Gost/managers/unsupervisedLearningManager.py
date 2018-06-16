import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA 
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score

from managers.csvManager import csv_run


def uLM_run():

    df, df_full, dfauthor, dfauthor_set, dfgenre_set, dfhashes, dfhashes_set, dfname_set, dfstyle = csv_run()

    #pca = PCA().fit(dfhashes)
    #plt.plot(np.cumsum(pca.explained_variance_ratio_))
    #plt.xlabel('number of components')
    #plt.ylabel('cumulative variance');
    #plt.show()
    dfhashes=dfhashes.fillna(0)
    dataframe_std = pd.DataFrame(StandardScaler().fit_transform(dfhashes))
    cov_std = dataframe_std.corr()
    cov_std=cov_std.fillna(0)

    eig_vals, eig_vect = np.linalg.eig(cov_std)
    eig_pairs = [(np.abs(eig_vals[i]), eig_vect[:,i]) for i in range(len(eig_vals))]
    
    sum_ev = sum(eig_vals)
    pve = [(i / sum_ev)*100 for i in sorted(eig_vals, reverse=True)]
    cum_var_pve = np.cumsum(pve)
    
    #fig = plt.figure(figsize=[10,5])
    #plt.scatter([i for i in range(len(dataset_std.columns))], pve, s=80)
    #plt.scatter([i for i in range(len(dataset_std.columns))], cum_var_pve, marker='+')
    #plt.legend(['Variance', 'Cumulative variance'])
    #plt.show()

    dataframe_pca = PCA(n_components=2).fit_transform(dataframe_std)

    dfhashes=dfhashes.fillna(0)
    dataframe_std = pd.DataFrame(StandardScaler().fit_transform(dfhashes))
    cov_std = dataframe_std.corr()
    cov_std=cov_std.fillna(0)

    plt.scatter(dataframe_pca[:,0],dataframe_pca[:,1])

    plt.xlabel('x')
    plt.ylabel('y')
    plt.xlim(min(dataframe_pca[:,0]),max(dataframe_pca[:,0]))
    plt.ylim(min(dataframe_pca[:,1]),max(dataframe_pca[:,1]))
    
    plt.show()

    k = range(2,20)
    silhouette = [0.0]*20
    for n_clusters in k:
        clusterer = KMeans(n_clusters=n_clusters, random_state=10)
        cluster_labels = clusterer.fit_predict(dataframe_pca)
        silhouette_avg = silhouette_score(dataframe_pca, cluster_labels)
        silhouette[n_clusters] = silhouette_avg
        
    # We compute the score for each cluster and take the closest to 1
    best_nb_clust = silhouette.index(max(silhouette)) 
    print("The best number of cluster is : " + str(best_nb_clust))

    X = dataframe_pca
    range_n_clusters = range(2,8)
    
    for n_clusters in range_n_clusters:
        fig, (ax1, ax2) = plt.subplots(1, 2)
        fig.set_size_inches(18, 7)
        
        # Limit of the figure for the silhouette -1, 1 
        ax1.set_xlim([-0.2, 1])
        ax1.set_ylim([0, len(X) + (n_clusters + 1) * 10])
    
        # Initialize the clusterer with n_clusters value and a random generator with speed = 10
        clusterer = KMeans(n_clusters=n_clusters, random_state=10)
        cluster_labels = clusterer.fit_predict(X)
        
        # Silhouette score between -1 (worse) and 1 (better) 
        silhouette_avg = silhouette_score(X, cluster_labels)  
        print("For n_clusters =", n_clusters,
              "The average silhouette_score is :", silhouette_avg)
    
        # Compute the silhouette scores for each sample
        sample_silhouette_values = silhouette_samples(X, cluster_labels)
    
        y_lower = 10
        for i in range(n_clusters):
            # Aggregate the silhouette scores for samples belonging to
            # cluster i, and sort them
            ith_cluster_silhouette_values = \
                sample_silhouette_values[cluster_labels == i]
    
            ith_cluster_silhouette_values.sort()
    
            size_cluster_i = ith_cluster_silhouette_values.shape[0]
            y_upper = y_lower + size_cluster_i
    
            color = plt.cm.inferno(float(i) / n_clusters)
            ax1.fill_betweenx(np.arange(y_lower, y_upper),
                              0, ith_cluster_silhouette_values,
                              facecolor=color, edgecolor=color, alpha=0.7)
    
            # Label the silhouette plots with their cluster numbers at the middle
            ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))
    
            # Compute the new y_lower for next plot
            y_lower = y_upper + 10  # 10 for the 0 samples
    
        ax1.set_title("The silhouette plot for the various clusters.")
        ax1.set_xlabel("The silhouette coefficient values")
        ax1.set_ylabel("Cluster label")
    
        # The vertical line for average silhouette score of all the values
        ax1.axvline(x=silhouette_avg, color="red", linestyle="--")
    
        ax1.set_yticks([])  # Clear the yaxis labels / ticks
        ax1.set_xticks([-0.2, -0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])
    
        # 2nd Plot showing the actual clusters formed
        colors = plt.cm.inferno(cluster_labels.astype(float) / n_clusters)
        ax2.scatter(X[:, 0], X[:, 1], marker='.', s=30, lw=0, alpha=0.7,
                    c= cluster_labels , edgecolor='k')
    
        # Labeling the clusters
        centers = clusterer.cluster_centers_
        # Draw white circles at cluster centers
        ax2.scatter(centers[:, 0], centers[:, 1], marker='o',
                    c="white", alpha=1, s=200, edgecolor='k')
    
        for i, c in enumerate(centers):
            ax2.scatter(c[0], c[1], marker='$%d$' % i, alpha=1,
                        s=50, edgecolor='k')
    
        ax2.set_title("The visualization of the clustered data.")
        ax2.set_xlabel("Feature space for the 1st feature")
        ax2.set_ylabel("Feature space for the 2nd feature")
    
        plt.suptitle(("#clusters = %d" % n_clusters),
                     fontsize=14, fontweight='bold')
    
        plt.show()