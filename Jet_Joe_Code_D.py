####################################
#######  16.004 Jet Joe D #########
####################################

import numpy as np
import matplotlib.pyplot as plt
import math as math
from scipy.optimize import fsolve

r_outer = 55.24/2*10**(-3)   # [m]
r_inner = 37.2/2*10**(-3)    # [m]
rm = (r_outer+r_inner)/2      # [m]
A = math.pi*(2*rm)/12*.00548      # [m^2]

LHV = 44.5 * 10**6      # [J/kg] fuel heating value
g = -9.81 # m/s
LoD = 10 # cruise L/D
ToW_TO = 0.34 # takeoff T/W
ToW_C = 0.1 # cruise T/W
W0 = 32 # empty aircraft weight (lbs)
fmax = 1.0 # fuel capacity (gal)
rho_f = 6.843 # fuel density (lbs/gal)
Wf0 = fmax * rho_f # fuel weight (lbs)
Wtotal = (W0 + Wf0)*0.453592 # total takeoff weight (kg)
W_TO = Wtotal
alt = 2000*0.3048 #ft --> m

def drone_range(mdot_f, t, SFC, mdot_1):

    # use breguet range equation to evaluate range in cruise
    c = 100 * 0.51444 # knots --> m/s
    T = t*mdot_1
    mu_0 = (T*c)/(mdot_f*LHV) # overall efficiency
    R = -(LHV/g)*mu_0*(LoD)*np.log(W0/Wtotal) # m
    print(f'Range = {R} (m)\n      = {R/1000} (km)\n      = {R*0.000621371} (mi)')

    return R

drone_range(0.000225182, 2.296, 1.93e-05, 0.03215) # values from intermediate speed


def static_thrust():

    h = np.linspace(0, 15000 * 0.3048, 50)    # altitudes from sea level to 15000 ft (expressed in m)

    Tamb = 15.04 - .00649*h
    Pamb = 101.29 * ((Tamb + 273.1)/288.08)**5.256
    R = 273 # J/kg*K
    rho0 = Pamb/(.2869 * (Tamb+273.1)) # static air density

    # assume pe and p0 are equal
    T = Pamb**(2/3) * (2*rho0*A)**(1/3)
    s_alt = 1/(rho0*T/Wtotal)
    s_SL = 1/(rho0[0]*T[0]/Wtotal)
    s_ratio = s_alt/s_SL

    plt.figure()
    plt.plot(h, s_ratio)
    plt.xlabel('h')
    plt.ylabel('s_alt/s_SL')
    plt.title(f's_alt/s_SL as a function of altitude')
    plt.show()

    return

static_thrust() # max RPM
