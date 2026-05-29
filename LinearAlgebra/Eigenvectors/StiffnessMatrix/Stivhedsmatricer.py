from numpy import loadtxt
from numpy.linalg import eigvals

## Figur 4
K1 = loadtxt("StivMat1.csv", delimiter=",") # Indlæser matricen K1

# Egenværdierne for en matrix A kan i Numpy beregnes med kommandoen eigvals(A).
# Resultatet er en vektor, hvor antallet af gange, hver egenværdi optræder,
# svarer til dens multiplicitet.
eig1 = eigvals(K1)
print(eig1)

# Er nogen af egenværdierne 0 (eller tæt på 0)?

# Er K1 inverterbar?

## Figur 5
K2 = loadtxt("StivMat2.csv", delimiter=",")

eig2 = eigvals(K2)
print(eig2)

# Er nogen af egenværdierne 0 (eller tæt på 0)?

# Betyder dette, at K2 er inverterbar? Sammenhold dette med rangen af K2.
