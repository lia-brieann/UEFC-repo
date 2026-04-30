####################################
#######  16.004 Jet Joe D #########
####################################

import numpy as np
import matplotlib.pyplot as plt
import math as math
from scipy.optimize import fsolve

LHV = 44.5 * 10**6      # [J/kg] fuel heating value
g = 9.81 # m/s
LoD = 10 # cruise L/D
ToW_TO = 0.34 # takeoff T/W
ToW__C = 0.1 # cruise T/W
W0 = 32 # empty aircraft weight (lbs)
fmax = 1.0 # fuel capacity (gal)
rho_f = 6.843 # fuel density (lbs/gal)
Wf = fmax * rho_f # fuel weight (lbs)
Wtotal = (W0 + Wf)*0.453592 # total takeoff weight (kg)

def drone_range(mdot_f):
    # Breguet range equation
    alt = 2000 #ft

    # need to calculate overall efficiency based on flight speed

    c = 100 * 0.51444 #m/s

    mdot_f = np.nan # assume a constant fuel flow rate
    mu_0 = (T*c)/(mdot_f*LHV) # overall efficiency
    R = (LHV/g)*mu_0*(LoD)*np.log(W0/Wtotal)

    print(f'Range = {R} (m)\n      = {R/1000} (km)\n      = {R*0.000621371} (mi)')

    return
