import matplotlib.pyplot as plt 
import numpy as np 


def samplemat(dims):
    """Make a matrix with all zeroes and increasing elements on the diagonal"""
    aa = np.zeros(dims)
    print(aa)
    for i in range(min(dims)):
        aa[i, i] = i
    print(aa)
    return aa



plt.matshow(samplemat((15,11)))

plt.show()