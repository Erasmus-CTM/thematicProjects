import numpy
from numpy.linalg import inv
import matplotlib.pyplot as plt

def fit(X, v):
    """
    Find mindste kvadraters løsning u til Xu=vHat, sådan
    at ||v-vHat||^2 minimeres. Fungerer kun på andengrads-
    polynomier som i workshoppen.

    Args:
    	X: Designmatrix
    	v: Datavektor

    Returns:
    	(u, vHat)
    """
    u = ???                     # Fyld selv ind. Bemærk, at matrixproduktet
    vHat = ???                  # A*B er A.dot(B) i numpy

    # Evaluer modellen på et x/y-gitter
    x = numpy.arange(-10, 10, 0.1)
    y = numpy.arange(-10, 10, 0.1)
    xg, yg = numpy.meshgrid(x, y)
    zg = (
        numpy.ones(numpy.shape(xg)) * u[0] +
        xg * u[1] +
        yg * u[2] +
        xg**2 * u[3] +
        xg*yg * u[4] +
        yg**2 * u[5]
    )

    # Plot datapunkterne v sammen med modellen
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    ax.plot_surface(xg, yg, zg, alpha=0.7)
    ax.scatter(X[:,1], X[:,2], v, s=20, color='k')

    plt.show(block=False)

    return(u, vHat)
