import time
from numpy import random
import numpy as np

from numpy.random import default_rng

iteration_count = 10000

a = np.full((10,10), 1)
b = np.arange(0, 10, 1)

c = np.multiply(a, b[:, np.newaxis])

a = np.ones((20,20))
b = np.zeros((20,20))


print(a[1:6][:])