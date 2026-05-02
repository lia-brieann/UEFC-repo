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

g = -9.81 # m/s
gamma = 1.4
R = 273 # J/kg*K

LHV = 44.5 * 10**6      # [J/kg] fuel heating value
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
    alt = altitude in feet
    rho = air density at alttitude
    """

    Tamb = 15.04 - .00649*(alt*0.3048)
    Pamb = 101.29 * ((Tamb + 273.1)/288.08)**5.256
    rho = Pamb/(.2869 * (Tamb+273.1))

    return (rho,Tamb,Pamb)

def drone_range(c, conditions, mdot_f, t):
    """
    inputs:
        c = airspeed in knots
        alt = altitude in feet
        rho = density at altitude
        mdot_f = fuel mass flow rate
        t = specific thrust

    returns:
        R = range for c onstant cruise conditions at altitude
    """

    # use breguet range equation to evaluate range in cruise
    rho = conditions[0]
    Tamb = conditions[1]
    Pamb = conditions[2]

    mdot_i = rho*c*A
    a0 = np.sqrt(gamma*R*Tamb)

    T = t*mdot_i*a0
    mu_0 = (T*c)/(mdot_f*LHV) # overall efficiency
    r = (LHV/g)*mu_0*(LoD)*np.log(W0/Wtotal) # m
    print(f'Range = {r} (m)\n      = {r/1000} (km)\n      = {r*0.000621371} (mi)')

    return r

# placeholder values from intermediate speed
mdot_f = 0.000225182
t = 2.296
# mdot_1 = 0.03215
conditions = alt_conditions(alt)

drone_range(c*0.51444, conditions, mdot_f, t)


def static_thrust():

    h = np.linspace(0, 15000, 50)    # altitudes from sea level to 15000 ft (expressed in m)

    Tamb = 15.04 - .00649*(h*0.3048)
    Pamb = 101.29 * ((Tamb + 273.1)/288.08)**5.256
    R = 273 # J/kg*K
    rho0 = Pamb/(.2869 * (Tamb+273.1)) # static air density

    # assume pe and p0 are equal
    Wtotal = Wtotal*0.453592 # lbs --> kg
    T = Pamb**(2/3) * (2*rho0*A)**(1/3) # thrust?
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

# static_thrust() # @ max RPM
