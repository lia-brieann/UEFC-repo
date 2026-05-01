####################################
#######  16.004 Jet Joe D #########
####################################

import numpy as np
import matplotlib.pyplot as plt
import math as math
from scipy.optimize import fsolve

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

    # # first we find the time to reach altitude
    # a = g*(ToW_TO-1)
    # t_TO = np.sqrt(2*alt/a) # takeoff time
    # # print(f't_TO = {t_TO}')

    # # then we use t_TO to find the change in weight
    # # we'll assume that the drone descends at the same rate as it ascends, so we double the fuel loss
    # W = W_TO - 2*mdot_f*(-g)*t_TO
    # print(f'initial weight = {W_TO}, weight minus takeoff and landing fuel = {W}')

    # use breguet range equation to evaluate range in cruise
    # calculate overall efficiency based on flight speed
    c = 100 * 0.51444 # knots --> m/s

    a0 = 340 # m/s
    T = t*mdot_1

    mu_0 = (T*c)/(mdot_f*LHV) # overall efficiency
    R = -(LHV/g)*mu_0*(LoD)*np.log(W0/Wtotal) # m
    print(f'Range = {R} (m)\n      = {R/1000} (km)\n      = {R*0.000621371} (mi)')

    return R

drone_range(0.000225182, 2.296, 1.93e-05, 0.03215)


def static_thrust():
    h = np.linspace(0, 15000 * 0.3048, 1000)    # altitudes from sea level to 15000 ft (expressed in m)
    p0 = np.nan # static air density
    return
