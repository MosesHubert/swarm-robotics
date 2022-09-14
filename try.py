from random import uniform
import numpy as np
import pandas as pd

n_state = 5
Q_values = []
for i in range(0, n_state * 7, 7):
    row = []
    for j in range(i, i + 7, 1):
        row.append(float(uniform(-2,2)))
    Q_values.append(row)

Q_values = np.array(Q_values ,dtype=float).reshape(n_state, 7)
a = pd.DataFrame(Q_values[0]).transpose()
print(a)