####################################
#######  16.004 Jet Joe D #########
####################################

import numpy as np
import matplotlib.pyplot as plt
import math as math
from scipy.optimize import fsolve

r_outer = 55.24/2*10**(-3)        # [m]
r_inner = 37.2/2*10**(-3)         # [m]
rm = (r_outer+r_inner)/2          # [m]
A = math.pi*(2*rm)/12*.00548      # [m^2]
B2 = 65 * (math.pi/180)      # radians
a2 = 0       # radians

# cps and gammas #
R = 287.        # J/(kgK)
gi = 1.4        # i = inlet
gc = 1.4        # c = combustor
gb = 1.3        # b = burner
gt = 1.3        # t = turbine
gn = 1.3        # n = nozzle
cpc = gc*R/(gc-1)
cpb = gb*R/(gb-1)
cpt = gt*R/(gt-1)
cpn = gn*R/(gn-1)


g = -9.81 # m/s
gamma = 1.4
R = 273 # J/kg*K

LHV = 44.5 * 10**6  # [J/kg] fuel heating value
LoD = 10 # cruise L/D
ToW_TO = 0.34 # takeoff T/W
ToW_C = 0.1 # cruise T/W
W0 = 32 # empty aircraft weight (lbs)
fmax = 1.0 # fuel capacity (gal)
rho_f = 6.843 # fuel density (lbs/gal)
Wf0 = fmax * rho_f # fuel weight (lbs)
Wtotal = (W0 + Wf0) # total takeoff weight (lbs)

alt = 2000 #ft
c = 100 # knots

def alt_conditions(alt):
    """
    inputs:
        alt = altitude in feet
    returns:
        rho = air density at alttitude
        Tamb = ambient temperature at altitude
        Pamb = ambient pressure at altitude
    """

    Tamb = 15.04 - .00649*(alt*0.3048)
    Pamb = 101.29 * ((Tamb + 273.1)/288.08)**5.256
    rho = Pamb/(.2869 * (Tamb+273.1))

    return rho, Tamb, Pamb

def drone_range(c, SFC, alt, mdot_f):
    """
    inputs:
        c = airspeed in m/s
        SFC = specific fuel consumption (assumed independent of altitude)
        alt = altitude in feet
        mdot_f = fuel mass flow rate
        t = specific thrust

    returns:
        R = range for c onstant cruise conditions at altitude
    """

    # use breguet range equation to evaluate range in cruise
    rho, Tamb, Pamb = alt_conditions(alt)
    mdot_i = rho*c*A
    a0 = np.sqrt(gamma*R*Tamb)

    # T = mdot_f/SFC
    # mu_0 = (T*c)/(mdot_f*LHV)  # overall efficiency

    mu_0 = c/(SFC*LHV)
    r = (LHV/g)*mu_0*(LoD)*np.log(W0/Wtotal) # Range in m
    print(f'Range = {r} (m)\n      = {r/1000} (km)\n      = {r*0.000621371} (mi)')

    return r

# placeholder values from intermediate speed
mdot_f = 0.000225182
# t = 2.296
# mdot_1 = 0.03215
SFC = 0.00009121475656

drone_range(c*0.51444, SFC, alt, mdot_f)



def static_thrust(mdot_f, Wtotal):
    """
    Plots static thrust and roll length ratio as functions of altitude from SL to 15000 ft

    Inputs:
    - mdot_f: fuel mass flow
    - Wtotal: total weight of aircraft at takeoff (in lbs)

    """
    h = np.linspace(0, 15000, 50)    # altitudes from sea level to 15000 ft (expressed in m)
    Wtotal = Wtotal*0.453592 # lbs --> kg
    rho0, Tamb, Pamb = alt_conditions(h)

    mdot_i = np.nan # inlet mass flow
    mdot_e = np.nan # exit mass flow
    ce = np.nan # exit speed

    # calculate static thrust
    f = mdot_f / mdot_e
    t = (f+1) * (ce/np.sqrt(gc*R*Tamb))
    T = t * mdot_i
    # T = mdot_i*c - mdot_6*c6

    plt.figure()
    plt.plot(h, T)
    plt.xlabel('h (ft)')
    plt.ylabel('static thrust T')
    plt.title(f'static thrust as a function of altitude')
    plt.grid(True)
    plt.show()

    s_alt = 1/(rho0*T/Wtotal)
    s_SL = 1/(rho0[0]*T[0]/Wtotal)
    s_ratio = s_alt/s_SL

    plt.figure()
    plt.plot(h, s_ratio)
    plt.xlabel('h (ft)')
    plt.ylabel('s_alt/s_SL')
    plt.title(f's_alt/s_SL as a function of altitude')
    plt.grid(True)
    plt.show()

    return

# assume fuel mass flow independent of altitude
# need to calculate mdot_e and mdot_i as functions of alt?

mdot_f = 0.001290232

# static_thrust(Wtotal) # @ max RPM
