import numpy as np
#import matplotlib.pyplot as plt
#import pickle
#matplotlib inline

N = 1000
x = np.random.rand(N) * 4 - 2
y = np.multiply(np.sqrt(2 - np.power(x,2)),(np.random.rand(N) * 2 - 1))

x2 = np.random.rand(2*N) * 6 - 3
y2 = np.multiply(np.sqrt(9 - np.power(x2,2)),(np.random.rand(2*N) * 2 - 1))

positives = np.zeros((1000,3))
positives[:,0] = x
positives[:,1] = y
positives[:,2] = 1

negatives = np.zeros((2000,3))
negatives[:,0] = x2
negatives[:,1] = y2
negatives[:,2] = 0

#Hollowing out larger ball
newnegatives = negatives[(np.power(negatives[:,0],2) + np.power(negatives[:,1],2)) > 5]
#Checking number of negatives and positives are roughly equal

#Plotting the figure
#fig = plt.figure(figsize=(6,6))
#ax1 = fig.add_subplot(111)

#ax1.scatter(positives[:,0], positives[:,1], s=20, alpha=0.5, c='r', marker="o", label='positive')
#ax1.scatter(newnegatives[:,0], newnegatives[:,1], s=20, alpha=0.5, c='b', marker="o", label='negative')
#plt.legend(loc='upper left')
np.savetxt('t1.out', positives, delimiter=',')
np.savetxt('t2.out', newnegatives, delimiter=',')
#plt.show()
