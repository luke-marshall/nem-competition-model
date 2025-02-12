# Feature selection trial
# Using forests
# Adapted from sklearn tutorials. 
# Original code here http://scikit-learn.org/stable/auto_examples/ensemble/plot_forest_importances.html#sphx-glr-auto-examples-ensemble-plot-forest-importances-py


import numpy as np
import matplotlib.pyplot as plt

from sklearn.datasets import make_classification
from sklearn.ensemble import ExtraTreesClassifier

import marketUtils
import random



nem = marketUtils.getNem()
interconnectors = marketUtils.getInterconnectorFlows()
(hhi, maxShareRetailers) = marketUtils.getHHI()

X = []
y = []


# Prepare the data for the classifier.
times = list(nem)
times.sort()
xLabels = list(interconnectors.itervalues().next())
xLabels.sort()



for time in times:
	
	# Add the classifications:
	if float(hhi[time]['Cumulative_HHI']) >= 2500:
		classification = 1
	else: 
		classification = 0
	y.append(classification)

	
	row = []
	for attribute in xLabels:
		row.append(interconnectors[time][attribute])
	# for category in sorted(list(hhi[time])):
	# 	row.append(hhi[time][category])
	row.append(nem[time]['nsw']['demand'])
	row.append(nem[time]['vic']['demand'])
	row.append(nem[time]['qld']['demand'])
	row.append(nem[time]['sa']['demand'])
	row.append(nem[time]['tas']['demand'])
	row.append(random.randint(1,2))
	X.append(row)

# for category in sorted(list(hhi[time])):
# 	xLabels.append('nsw '+category)

xLabels.append('nsw demand')
xLabels.append('vic demand')
xLabels.append('qld demand')
xLabels.append('sa demand')
xLabels.append('tas demand')
xLabels.append('DUMMY VARIABLE')


X = np.array(X)
y = np.array(y)

print X
print np.sum(y)




# Build a classification task using 3 informative features
# X, y = make_classification(n_samples=1000,
# 							n_features=10,
# 							n_informative=3,
# 							n_redundant=0,
# 							n_repeated=0,
# 							n_classes=2,
# 							random_state=0,
# 							shuffle=False)

# print X

# Build a forest and compute the feature importances
forest = ExtraTreesClassifier(n_estimators=250,random_state=0)



forest.fit(X, y)
importances = forest.feature_importances_
std = np.std([tree.feature_importances_ for tree in forest.estimators_], axis=0)
indices = np.argsort(importances)[::-1]

# Print the feature ranking
print("Feature ranking:")

for f in range(X.shape[1]):
	
	print("%d. feature %d (%f) %s" % (f + 1, indices[f], importances[indices[f]], str(xLabels[indices[f]])))

# Plot the feature importances of the forest
plt.figure()
plt.title("Feature importances")
plt.bar(range(X.shape[1]), importances[indices], color="r", yerr=std[indices], align="center")
plt.xticks(range(X.shape[1]), indices)
plt.xlim([-1, X.shape[1]])
plt.show()