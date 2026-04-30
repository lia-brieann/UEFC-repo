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
alt = 2000 #ft

def drone_range(mdot_f, t, mdot_j):

    # need to calculate overall efficiency based on flight speed
    c = 100 * 0.51444 # knots --> m/s
    T = t*mdot_j
    mu_0 = (T*c)/(mdot_f*LHV) # overall efficiency
    R = (LHV/g)*mu_0*(LoD)*np.log(W0/Wtotal) # m

    print(f'Range = {R} (m)\n      = {R/1000} (km)\n      = {R*0.000621371} (mi)')

    return R

drone_range(0.001290232,4.526,0.2997)


def static_thrust():
    h = np.linspace(0, 15000 * 0.3048, 1000)    # altitudes from sea level to 15000 ft (expressed in m)
    p0 = np.nan # static air density
    return
