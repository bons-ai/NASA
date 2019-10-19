import numpy as np
from sklearn.decomposition import NMF
import matplotlib.pyplot as plt
import umap
import hdbscan
import json

filename = "hist_0530_03_09.npy"
data = np.load(filename, allow_pickle=True).item()

hist = np.array(data["hist"])
h = np.array(data["h"])
pos = np.array(data["pos"])

reducer = umap.UMAP()
embedding = reducer.fit_transform(hist)

clusterer = hdbscan.HDBSCAN(algorithm='best', alpha=1.0, approx_min_span_tree=True,
    gen_min_span_tree=False, leaf_size=40,
    metric='euclidean', min_cluster_size=15, min_samples=None, p=None)
clusterer.fit(embedding)
#
# print(clusterer.labels_)
#
# plt.figure()
# plt.scatter(embedding[:, 0], embedding[:, 1], c=clusterer.labels_)
# plt.show()
#
# plt.figure(figsize=(12,12))
# plt.scatter(pos[0, :], pos[1,:], c=clusterer.labels_)
# plt.colorbar()
# plt.show()

results = []
for n in range(pos.shape[1]):
    results.append({"coordinates": list(pos[:, n]),
                    "type": float(clusterer.labels_[n])})

full_data = {"points": results,
             "minLat": np.min(pos[0, :]),
             "maxLat": np.max(pos[0, :]),
             "minLong": np.min(pos[1, :]),
             "maxLong": np.max(pos[1, :])}

with open("results.json", "w", encoding='utf-8') as f:
    json.dump(full_data, f)
