import numpy as np
from scipy.spatial import distance
import matplotlib.pyplot as plt
# Given lat, long, h for a track (all gt and all segments)

N_regions = 512
N_height = 64

# L = 1000000
# lon = np.linspace(30, 80, L)[:, np.newaxis]
# lat = np.linspace(-50, 50, L)[:, np.newaxis]
# h = np.random.random(L)

filename = "data_0530_03_09.npy"
data = np.load(filename, allow_pickle=True).item()

lon = data["lon"][:, np.newaxis]
lat = data["lat"][:, np.newaxis]
h = data["lz"]

pos = np.concatenate((lon, lat), axis=1)

pos_i_idx = np.argmin(pos[:, 0])
pos_f_idx = np.argmax(pos[:, 0])

pos_i = np.transpose(np.array([pos[pos_i_idx, 0], pos[pos_i_idx, 1]])[:, np.newaxis])
pos_f = np.transpose(np.array([pos[pos_f_idx, 0], pos[pos_f_idx, 1]])[:, np.newaxis])

dist = distance.cdist(pos, pos_i, 'euclidean')
bins_regions = np.digitize(dist, np.linspace(np.min(dist), np.max(dist), N_regions))

lon_moy = []
lat_moy =[]
hist = []
h_min = []
h_max = []
for n in np.arange(1, N_regions):
    idx = np.where(bins_regions == n)[0]

    H = h[idx]
    if len(H) > 5:
        H = H[H > np.percentile(H, 1)]
        H = H[H < np.percentile(H, 99)]

        h_min.append(np.min(H))
        h_max.append(np.max(H))

        lon_moy.append(np.mean(lon[idx]))
        lat_moy.append(np.mean(lat[idx]))

        hist.append(np.histogram(H, bins=N_height)[0])


pos = [lon_moy, lat_moy]

np.save("hist" + filename[4:], {"pos": [lon_moy, lat_moy],
                       "hist": hist,
                       "h": [h_min, h_max]})

# plt.plot(hist[0][0])
# plt.show()
