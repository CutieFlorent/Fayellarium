import numpy as np
import matplotlib.pyplot as plt
from fuzz import AND, OR, XOR


def cross(func, x, y):
    f = lambda t: 4*np.exp(-t)/(1+np.exp(-t))**2
    x, y = f(x), f(y)
    # return f(y)
    return func(x,y)



def plt3D(i, ax, func, cmap):
    ax = figs.add_subplot(1,3,i, projection='3d')
    ax.plot_surface(X, Y, cross(func, X, Y), cmap=cmap, rstride=2, cstride=2)
    ax.view_init(elev=30, azim=45)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel(func.__name__)


EXPAND = 16
ACCURACY = 2 ** 7
ruler = np.linspace(-EXPAND, EXPAND, ACCURACY + 1)
X, Y = np.meshgrid(ruler, ruler)

# plt.figure()
figs, axs = plt.subplots(1, 3)
plt.subplots_adjust(wspace=0.2, hspace=0.5)

for i, ax, func in zip(range(1,4), axs.flat, [OR, XOR, AND]):
    ax.axis('off')
    plt3D(i, ax, func, 'viridis')

# plt.imshow(Z, extent=[-10, 10, -10, 10], origin='lower', cmap='viridis')
# plt.xlabel('x')
# plt.ylabel('y')
# # plt.show()


plt.show()
