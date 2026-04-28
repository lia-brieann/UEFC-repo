####################################
#######  16.004 Jet Joe D #########
####################################

import numpy as np
import matplotlib.pyplot as plt
import math as math
from scipy.optimize import fsolve

# Breguet range equation
LHV = 44.5 * 10**6      # [J/kg] fuel heating value
g = 9.81 # m/s
L_over_D = 10 # cruise L/D
W0 = 32 # empty aircraft weight (lbs)
fmax = 1.0 # fuel capacity (gal)
rho_f = 6.843 # fuel density (lbs/gal)
Wf = fmax * rho_f # fuel weight (lbs)
Wtotal = (W0 + Wf)*0.453592 # total takeoff weight (kg)

# need to calculate overall efficeincy based on flight speed
alt = 2000 #ft
c = 100 * 0.51444 #m/s

eff_0 = np.nan # overall efficiency
R = (LHV/g)*eff_0*(L_over_D)*np.log(W0/Wtotal)
print(f'Range = {R} (m)\n      = {R/1000} (km)\n      = {R*0.000621371} (mi)')
