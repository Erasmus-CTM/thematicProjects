import numpy
import numpy.linalg as la
import matplotlib.pyplot as plt

def plotPca(X):
    """
    Plot data points along with their principal components.

    Args:
    	X: Matrix (nx2 or nx3) with one observation per row

    Returns:
    	D: List of eigenvalues
    	V: Corresponding eigenvectors with length equal to the square
    	   root of its eigenvalue.
    """
    D, V = la.eig(numpy.cov(X, rowvar=False))

    # Scale eigenvectors to have length equal to the square of the
    # corresponding eigenvalue
    for i in range(V.shape[1]):
        V[:,i] = V[:,i]/la.norm(V[:,i])*numpy.sqrt(D[i])

    # Plot data depending on the dimension
    fig = plt.figure()
    if X.shape[1]==2:
        ax=fig.add_subplot()
        ax.scatter(X[:,0], X[:, 1])
        ax.quiver(
            [0,0], [0,0],       # Startin points
            V[0,:], V[1,:])     # End points
    elif X.shape[1]==3:
        ax = fig.add_subplot(projection="3d")
        ax.scatter(X[:,0], X[:,1], X[:,2])
        ax.quiver(
            [0,0,0], [0,0,0], [0,0,0], # Starting points
            V[0,:], V[1,:], V[2,:],    # End points
            colors = (0,0,0,1)
        )
    else:
        raise ValueError("Input matrix must have 2 or 3 columns!")

    fig.gca().set_aspect("equal")
    fig.show()

    return D, V


