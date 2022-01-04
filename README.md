# bixreader
Quickly hacked library to read CST binary files into NumPy arrays. Please report any problematic input file.

Clone into working directory.

Example code, you may need to adjust depending on your data file:
```python
import bixreader
import matplotlib.pyplot as plt

header, data = bixreader.read('a.bix')
print(header)
print(data['Points'].shape)

ax = plt.subplot(projection='3d')
ax.quiver(*data['Points'], *data['Result'], length=0.5, normalize=True)
ax.set(xlim=(-500, 500), ylim=(-500, 500), zlim=(-500, 500))
plt.show()
```