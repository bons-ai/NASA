import numpy as np

H = np.arange(100, 200)
H = H[H>np.percentile(H, 10)]

print(H)

print(np.percentile(H, 5))