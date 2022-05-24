import matplotlib.pyplot as plt
import numpy as np
from numpy.random import default_rng
rng = default_rng()


plt.style.use('ggplot')

for i in range(10):
    mean = 0
    normal = rng.normal(mean, 0.1, 50)
    laplace = rng.laplace(mean, 0.1, 50)
    specialNormal = rng.laplace(mean, i / 20, 50)

    nScore = 0
    lScore = 0
    snScore = 0

    nDrama = 0
    lDrama = 0
    snDrama = 0

    for n, l, sn in zip(normal, laplace, specialNormal):
        nScore += abs(n)
        lScore += abs(l)
        snScore += abs(sn)
        if abs(n) > nDrama:
            nDrama = abs(n)
        if (abs(l) > lDrama):
            lDrama = abs(l)
        if (abs(sn)> snDrama):
            snDrama = abs(sn)

    print('Normal score:', nScore, 'Normal drama', nDrama)
    print('Laplace score', lScore, 'Laplace drama', lDrama)

    if nScore < lScore:
        print("Best score: normal")
    else:
        print("Best score: laplace")
    if nDrama > lDrama:
        print("Best drama: normal")
    else:
        print("Best drama: laplace")

# plot
fig, ax = plt.subplots()
ax.set_title('Normal Distribution')
ax.plot(normal, linewidth=2.0)
ax.set(xlim=(0, 50), xticks=np.arange(5, 50, 5),
       ylim=(-10, 10), yticks=np.arange(-9, 10, 2))

fig, ax = plt.subplots()
ax.set_title('Laplace Distribution')
ax.plot(laplace, linewidth=2.0)
ax.set(xlim=(0, 50), xticks=np.arange(5, 50, 5),
       ylim=(-10, 10), yticks=np.arange(-9, 10, 2))

fig, ax = plt.subplots()
ax.set_title('Special Normal Distribution')
ax.plot(specialNormal, linewidth=2.0)
ax.set(xlim=(0, 50), xticks=np.arange(5, 50, 5),
       ylim=(-10, 10), yticks=np.arange(-9, 10, 2))

plt.show()