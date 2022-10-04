
import numpy as np
import matplotlib.pyplot as plt

def lerp(v0, v1, t):
    return (1 - t) * v0 + t * v1

size = 1000
image = np.zeros((size, size, 3), dtype="uint8")
assert image.shape[0] == image.shape[1]

color1 = [255, 128, 0]
color2 = [0, 128, 255]

for i, v in enumerate(np.linspace(0, 1, 2 * size - 1)):
    r = lerp(color1[0], color2[0], v)
    g = lerp(color1[1], color2[1], v)
    b = lerp(color1[2], color2[2], v)
    j = 0
    if(i==0):
        image[i, j, :] = [r, g, b]
    elif(i>=size):
        j = i - size
        for k in range(2*size-i-1):
            j += 1
            image[size-k-1, j] = [r, g, b]
    else:
        for k in range(i+1):
            image[i, j] = [r, g, b]
            j+=1
            i-=1

plt.figure(1)
plt.imshow(image)
plt.show()