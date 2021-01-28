import time
from numpy import random

from numpy.random import default_rng

iteration_count = 10000

start = time.thread_time_ns()
rng = default_rng()
for i in range(0, iteration_count):
    vals = rng.standard_normal(10)
    more_vals = rng.standard_normal(10)

fast = time.thread_time_ns()-start
# instead of this

for i in range(0, iteration_count):
    vals = random.standard_normal(10)
    more_vals = random.normal(0, 2.5, size=(60,4))
slow = time.thread_time_ns()-start - fast

for i in range(0, iteration_count):
    vals = random.normal(10)
    random.default_rng().normal(0, 2.5, size=(60, 4))
mine = time.thread_time_ns()-start - fast - slow

print(fast, slow, mine)