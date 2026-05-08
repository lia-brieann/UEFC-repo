####################################
#######  16.004 Jet Joe D #########
####################################

import numpy as np
import matplotlib.pyplot as plt
import math as math
from scipy.optimize import fsolve
from ambiance import Atmosphere

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


g = 9.81 # m/s
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

    atmos = Atmosphere
    Tamb = atmos(alt*0.3048).temperature
    Pamb = atmos(alt*0.3048).pressure
    rho = atmos(alt*0.3048).density

    return rho, Tamb, Pamb

def drone_range(alt, c, SFC, mdot_f, RPM = 88000):
    """
    inputs:
        alt = altitude in feet
        c = airspeed in m/s
        SFC = specific fuel consumption (assumed independent of altitude)
        mdot_f = fuel mass flow rate
        RPM = rev/min

    returns:
        R = range for constant cruise conditions at altitude
    """

    rho, Tamb, Pamb = alt_conditions(alt)

    Tt5 = 953.15    # [K]
    Tt6 = Tt5       # [K]
    Tt0 = Tamb[0]      # [K]
    Tt1 = Tt0       # [K]
    Tt2 = Tt0       # [K]
    Patm = Pamb[0]
    P1 = Pamb[0]

    # Find wsh_T
    rm = (r_outer+r_inner)/2      # [m]
    omega = RPM*(2*math.pi/60)
    A = math.pi*(2*rm)/12*.00548      # [m^2]
    a1 = math.acos((5.48*10**(-3))/(math.pi*rm/6))      # radians
    phi  = 1/(math.tan(a2)-math.tan(B2))
    lamb = phi*(math.tan(a1)+math.tan(a2))
    wideal_T = lamb*(omega*rm)**2

    # Turbine and Compressor Efficiencies
    nc = 0.6    # we changed these values because other numbers gave very wrong values
    nt = 0.6    # we changed these values to get something that didn't break the code

    # Compressor Pressure Ratio
    wideal_c = -wideal_T
    wact_t = nt*wideal_T
    wact_c = wideal_c/nc
    Tt3 = wact_c/cpc + Tt2
    pi = (nc*(Tt3/Tt2 - 1) + 1)**(gc/(gc-1))

    # inlet mass flow
    def equations(vars):
        mdot_1, Tt4 = vars
        # print(type(Tt3), type(Tt2), type(Tt5), type(mdot_1))
        eq1 = mdot_1*cpb*(Tt4 - Tt3) - mdot_f*LHV
        eq2 = mdot_1*cpc*(Tt2 - Tt3) - (mdot_1 + mdot_f)*cpt*(Tt5 - Tt4)
        return [eq1, eq2]
    solution  = fsolve(equations, [0.01, 100])
    mdot_1 = solution[0]
    Tt4 = solution[1]

    # exit velocity
    Pt2 = P1
    Pt3 = pi*Pt2
    Pt4 = Pt3
    P6 = Patm
    Pt5 = Pt4*(1 - (1-Tt5/Tt4)/nt)**(gt/(gt-1))
    Pt6 = Pt5
    T6 = Tt6*(P6/Pt6)**((gn-1)/gn)
    c6 = math.sqrt(2*cpn*(Tt6-T6))      # [m/s]

    # mass flow #
    mdot_6 = 12*Pt4*A/(math.sqrt(R*Tt4))*math.sqrt(gn)*(1+(gn-1)/2)**((-gn-1)/(2*(gn-1)))
    mdot_i = mdot_1 # inlet mass flow
    mdot_e = mdot_6 # exit mass flow
    ce = c6 # exit speed

    # use breguet range equation to evaluate range in cruise
    KEdot = (mdot_e*ce**2)/2 - (mdot_i*c**2)/2
    T = mdot_e*ce - mdot_i*c   # N
    eta_therm = KEdot / (mdot_f*LHV)
    eta_prop = (T*c)/KEdot

    eta_0 = eta_therm * eta_prop
    r = (LHV/g)*eta_0*(LoD)*np.log(Wtotal/W0) # Range in m

    print(f'T = {T} N')
    print(f'eta_therm = {eta_therm}')
    print(f'eta_prop = {eta_prop}')
    print(f'eta_0 = {eta_0}')
    print(f'Range = {r} (m)\n      = {r/1000} (km)\n      = {r*0.000621371} (mi)')

    return r

# intermediate speed
SFC = 0.00009121
mdot_f = 0.00048688
RPM = 88000
drone_range(alt, c*0.51444, SFC, mdot_f, RPM)


def static_thrust(mdot_f, Wtotal, RPM = 160000):
    """
    Plots static thrust and roll length ratio as functions of altitude from SL to 15000 ft

    Inputs:
    - mdot_f: fuel mass flow
    - Wtotal: total weight of aircraft at takeoff (in lbs)
    - RPM: rev/min

    """

    # set up
    h = np.linspace(0, 15000, 50)    # altitudes from sea level to 15000 ft
    Wtotal = Wtotal*0.453592 # lbs --> kg
    rho, Tamb, Pamb = alt_conditions(h)
    Tt5 = 953.15    # [K]
    Tt6 = Tt5       # [K]

    T_list = []
    s_ratio = []

    for i in range(50):

        # ambient conditions
        Tt0 = Tamb[i]      # [K]
        Tt1 = Tt0       # [K]
        Tt2 = Tt0       # [K]
        Patm = Pamb[i]
        P1 = Pamb[i]

        # Find wsh_T
        rm = (r_outer+r_inner)/2      # [m]
        omega = RPM*(2*math.pi/60)
        A = math.pi*(2*rm)/12*.00548      # [m^2]
        a1 = math.acos((5.48*10**(-3))/(math.pi*rm/6))      # radians
        phi  = 1/(math.tan(a2)-math.tan(B2))
        lamb = phi*(math.tan(a1)+math.tan(a2))
        wideal_T = lamb*(omega*rm)**2

        # Turbine and Compressor Efficiencies
        nc = 0.7    # we changed these values because other numbers gave very wrong values
        nt = 0.6    # we changed these values to get something that didn't break the code

        # Compressor Pressure Ratio
        wideal_c = -wideal_T
        wact_t = nt*wideal_T
        wact_c = wideal_c/nc
        Tt3 = wact_c/cpc + Tt2
        pi = (nc*(Tt3/Tt2 - 1) + 1)**(gc/(gc-1))

        # inlet mass flow
        def equations(vars):
            mdot_1, Tt4 = vars
            # print(type(Tt3), type(Tt2), type(Tt5), type(mdot_1))
            eq1 = mdot_1*cpb*(Tt4 - Tt3) - mdot_f*LHV
            eq2 = mdot_1*cpc*(Tt2 - Tt3) - (mdot_1 + mdot_f)*cpt*(Tt5 - Tt4)
            return [eq1, eq2]
        solution  = fsolve(equations, [0.01, 100])
        mdot_1 = solution[0]
        Tt4 = solution[1]

        # exit velocity
        Pt2 = P1
        Pt3 = pi*Pt2
        Pt4 = Pt3
        P6 = Patm
        Pt5 = Pt4*(1 - (1-Tt5/Tt4)/nt)**(gt/(gt-1))
        Pt6 = Pt5
        T6 = Tt6*(P6/Pt6)**((gn-1)/gn)
        c6 = math.sqrt(2*cpn*(Tt6-T6))      # [m/s]

        # mass flow #
        mdot_6 = 12*Pt4*A/(math.sqrt(R*Tt4))*math.sqrt(gn)*(1+(gn-1)/2)**((-gn-1)/(2*(gn-1)))
        mdot_i = mdot_1 # inlet mass flow
        mdot_e = mdot_6 # exit mass flow
        ce = c6 # exit speed

        # static thrust and takeoff length
        T = mdot_e*ce   # N
        T_list.append(T)

        s_alt = 1/(rho[i]*T_list[i])
        s_SL = 1/(rho[0]*T_list[0])
        s_ratio.append(s_alt/s_SL)

    # plotting
    plt.figure()
    plt.plot(h, T_list)
    plt.xlabel('h (ft)')
    plt.ylabel('static thrust T (N)')
    plt.title(f'Static Thrust vs Altitude')
    plt.xlim(min(h),max(h))
    plt.ylim(min(T_list),max(T_list))
    plt.grid(True)
    plt.show()

    plt.figure()
    plt.plot(h, s_ratio)
    plt.xlabel('h (ft)')
    plt.ylabel(r'$s_{alt}$/$s_{SL}$')
    plt.title(r'$s_{alt}$/$s_{SL}$ vs altitude')
    plt.xlim(min(h),max(h))
    plt.ylim(min(s_ratio),max(s_ratio))
    plt.grid(True)
    plt.show()

    return

mdot_f = 0.001290232
RPM = 160000
# static_thrust(mdot_f, Wtotal, RPM) # @ max RPM
