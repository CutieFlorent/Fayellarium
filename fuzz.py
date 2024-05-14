import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.colors import Normalize
from mpl_toolkits.mplot3d import Axes3D

def sharpen(func):
    def AND(A, B):
        return np.minimum(A, B)

    def OR(A, B):
        return np.maximum(A, B)

    if func.__name__ == 'AND': return AND
    if func.__name__ == 'OR': return OR

def cubic(func):
    f = lambda x: -2 * x ** 3 + 3 * x ** 2

    def AND(A, B):
        A, B = f(A), f(B)
        return np.minimum(A, B)

    def OR(A, B):
        A, B = f(A), f(B)
        return np.maximum(A, B)

    if func.__name__ == 'AND': return AND
    if func.__name__ == 'OR': return OR

def rounded(func):
    def f(A):
        return np.where(A<0.5,
                        -np.sqrt(1/4-A**2)+1/2,
                        np.sqrt(1/4-(A-1)**2)+1/2,)

    def AND(A, B):
        A, B = f(A), f(B)
        return np.minimum(A, B)

    def OR(A, B):
        A, B = f(A), f(B)
        return np.maximum(A, B)

    if func.__name__ == 'AND': return AND
    if func.__name__ == 'OR': return OR

def NOT(A):
    return 1 - A

def AVG(A, B):
    return (A+B)/2

# @sharpen
# @cubic
# @rounded
def AND(A, B):
    return A * B  #np.sqrt(A * B)

def NAND(A, B):
    return NOT(AND(A, B))

# @sharpen
# @cubic
# @rounded
def OR(A, B):
    return NOT(AND(NOT(A), NOT(B)))

def NOR(A, B):
    return AND(NOT(A), NOT(B))

def TEST_AND(A, B):
    ruler = np.linspace(0,1,3)

    table = np.array([[0,0,0],
                      [0,0.5,0.5],
                      [0,0.5,1],
                      ])
    # interp.RBFInterpolator(np.stack((ruler,ruler)),table,smoothing=0,kernel='cubic')

def XOR(A, B):
    # f = lambda x: -2 * x ** 3 + 3 * x ** 2
    # xor1 = OR(AND(A, NOT(B)), AND(NOT(A), B))
    # xor2 = AND(NAND(A, B), OR(A, B))
    # res = AVG(xor1, xor2)
    # for i in range(2):
    #     res = f(res)
    # return res

    return AND(A, NOT(B)) + AND(NOT(A), B)




def NXOR(A, B):
    return NOT(XOR(A, B))

def DIFF(A, B):

    return AND(XOR(A, B), NXOR(A, B))
    # return OR(AND(A, NOT(B)), AND(B, NOT(A)))

def ZERO(A, B):
    return AND(XOR(A, B), NXOR(A, B))

def ONE(A, B):
    return OR(XOR(A, B), NXOR(A, B))


if __name__ == '__main__':
    DIM = 3
    STEP = 32

    X = np.linspace(0, 1, 129)
    A, B = np.meshgrid(X, X)

    fig, axes = plt.subplots(2, 3)
    plt.subplots_adjust(wspace=0.2, hspace=0.5)
    norm = Normalize(vmin=0, vmax=1)

    for i, ax, func in zip(
            range(1, 7),
            axes.flat,
            [AND, OR, ONE, XOR, NXOR, ZERO],
    ):
        if DIM == 2:
            if STEP:
                digi = np.digitize(func(A, B), bins=np.linspace(0, 1, STEP+1))
                digi = (digi - 0.5) / STEP
            else:
                digi = func(A, B)

            ax.set_title(func.__name__)
            ax.imshow(digi, cmap='twilight_shifted', origin='lower', extent=[0, 1, 0, 1], norm=norm)
            ax.xaxis.set_major_locator(ticker.MultipleLocator(1 / 4))
            ax.yaxis.set_major_locator(ticker.MultipleLocator(1 / 4))

        if DIM == 3:
            digi = func(A, B)

            ax.axis('off')
            ax.set_title(func.__name__)
            ax = fig.add_subplot(2, 3, i, projection='3d')
            for func in [ax.set_xlim, ax.set_ylim, ax.set_zlim]:
                func(0, 1)
            im = ax.plot_surface(A, B, digi, cmap='viridis', norm=norm)

    plt.show()
