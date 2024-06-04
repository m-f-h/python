""" plot a 2D vector field in Python - written & (c) May 2022 by M.F.Hasler

We find that the best way to plot a 2D vector field 
U(x,y) = (u, v)  where (u,v) = a(r) (x,y) + b(r) (-y,x)
and  (a,b) are solution to some ODE, 
is to use matplotlib.pyplot.quiver together with numpy.meshgrid and .vectorize().

# assume we integrated an ODE using, e.g.:
from scipy.integrate import solve_ivp
S = solve_ivp(f, [Rmax,Rmin], y0, dense_output=True)

# then S.sol is a function of r \in [Rmin, Rmax]
"""
import numpy as np
Rmin,Rmax = 20,200
S = lambda r: np.array([1-r/R,1])*2.718281828**(-r/R)
S.sol = S

import matplotlib.pyplot as plt
def uv(x,y): a,b = S.sol( (x**2+y**2)**.5 ); return a*x-b*y, a*y+b*x
x,y = np.meshgrid(np.linspace(-Rmin, Rmax*2/3, 40), np.linspace(-2*Rmin,2*Rmin, 30), sparse = True)
u,v = np.vectorize(uv, 2)(x,y)
plt.quiver(x, y, u, v)
plt.show()
