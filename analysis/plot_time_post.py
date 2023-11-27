import numpy as np
import matplotlib.pyplot as plt

S = [
	[0.64, 0.49, 0.81], 
	[0.88, 0.84, 0.92], 
	[1.7, 1.5, 2], 
	[3, 2.2, 4], 
	[0.17, 0.14, 0.2], 
	[0.92, 0.9, 0.95], 
	[0.66, 0.63, 0.69], 
	[0.59, 0.56, 0.61], 
	[1, 0.97, 1.04], 
	[1, 0.96, 1.05], 
]

I = [
	[0.41, 0.39, 0.44], 
	[0.047, 0.041, 0.053], 
	[0.047, 0.026, 0.069], 
	[0.76, 0.74, 0.79], 
	[0.35, 0.33, 0.36], 
	[0.11, 0.1, 0.114], 
	[0.066, 0.06, 0.074], 
	[0.048, 0.043, 0.053], 
	[0.0079, 0.0059, 0.01], 
	[0.028, 0.024, 0.033]
]


NARROW_BANDS = ['OE (I)', 'OE (II)', 'OE (III)', 'OE (IV)', 'ME (I)', 'ME (II)', 'ME (III)', 'ME (IV)', 'EME (I)', 'EME (II)', 'EME (III)']

def sep(nums):
	mean = []
	mn = []
	mx = []
	for s1, s2, s3 in nums:
		mean.append(s1)
		mn.append(s2)
		mx.append(s3)
	return mean, mn, mx


fig, axes = plt.subplots(2, 1, figsize=(10, 5), sharex=True)


axes[0].axhline(1, color='black', linestyle='--')

mean, mn, mx = sep(S)
axes[0].fill_between(range(1, 11), mn, mx, alpha=0.5, color='black', edgecolor='white')
axes[0].plot(range(1, 11), mean, color='black')

axes[0].set_ylim(0, 4)
axes[0].set_title('Frequency-dependent selection ($s$)')


mean, mn, mx = sep(I)
axes[1].fill_between(range(1, 11), mn, mx, alpha=0.5, color='black', edgecolor='white')
axes[1].plot(range(1, 11), mean, color='black')

axes[1].set_ylim(0, 1)
axes[1].set_title('Innovation rate ($i$)')

axes[1].set_xticks(range(0, 11))
axes[1].set_xticklabels(NARROW_BANDS)
axes[0].set_xlim(0, 11)
axes[1].set_xlim(0, 10)


plt.show()