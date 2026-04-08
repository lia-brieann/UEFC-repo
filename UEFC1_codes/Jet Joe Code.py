####################################
##########  16.004 Jet Joe  ########
####################################

import numpy as np
import matplotlib.pyplot as plt
import math as math
from scipy.optimize import fsolve

# Input Parameters #
r_outer = 55.24/2*10**(-3)      # [m]
r_inner = 37.2/2*10**(-3)      # [m]
A = math.pi*(r_outer**2-r_inner**2)/12        # [m^2]
B1 = np.nan       # radians
B2 = 65       # radians
a1 = np.nan       # radians
a2 = 0       # radians
RPM = 160000
mdot_f = np.nan
h = np.nan      # fuel heating value
Tt5 = np.nan
Tt6 = Tt5
Tt0 = 298.15    # [K]
Tt1 = Tt0
Tt2 = Tt0
# cps and gammas #
R = 287         # J/(kgK)
gi = 1.4        # i = inlet
gc = 1.4        # c = combustor
gb = 1.3        # b = burner
gt = 1.3        # t = turbine
gn = 1.3        # n = nozzle
cpc = gc*R/(gc-1)
cpb = gb*R/(gb-1)
cpt = gt*R/(gt-1)
cpn = gn*R/(gn-1)

#### Step 1 - Fine wsh_T ####
rm = (r_outer-r_inner)/2      # [m]
omega = RPM*(2*math.pi/60)
phi  = 1/(math.tan(a2)-math.tan(B2))
lamb = phi*(math.tan(a1)-math.tan(a2))
wideal_T = lamb*(omega*rm)**2

#### Step 2 - Assume Adiabatic Turbine and Compressor Efficiencies ####
nc = 0.7    # we can change these
nt = 0.7    # we can change these

#### Step 3 - Find Compressor Pressure Ratio ####
wideal_c = wideal_T
wact_c = nc*wideal_c
Tt3 = wact_c/cpc + Tt2
pi = (nc*(Tt3/Tt2 - 1) + 1)**(gc/(gc-1))

#### Step 4 - Find Tt3 ####
def equations(vars):
    mdot_1, Tt4 = vars
    eq1 = mdot_1*cpb*(Tt4 - Tt3) - mdot_f*h
    eq2 = mdot_1*cpc*(Tt2 - Tt3) - (mdot_1 + mdot_f)*cpt*(Tt5 - Tt4)
    return [eq1, eq2]
solution  = fsolve(equations, [0, 0])
mdot_1 = solution[0]
Tt4 = solution[1]

#### Step 5 - Determine Nozzle KE ####

# Pressures in Pa #
Patm = 101325
Pt2 = Patm
Pt3 = Pt2/pi
Pt4 = Pt3
P6 = Patm
def equation(vars):
    Pt5 = vars
    eq1 = nt - (1-Tt5/Tt4)/(1-(Pt5/Pt4)**((gt-1)/gt))
    return [eq1]
Pt5 = fsolve(equation, 0)[0]
Pt6 = Pt5
T6 = Tt6*(Pt6/Patm)**(-gn/(gn-1))
c6 = math.sqrt(2*cpn*(Tt6-T6))
KE = .5*c6**2*(mdot_1+mdot_f)       # Check for correct mdot

#### Step 6 - Find Specific Thrust, t, and SFC ####
SFC = mdot_f/((mdot_1+mdot_f)*c6)
T = mdot_f/SFC
t = T/mdot_1/math.sqrt(R*gi*Tt0)        # Check if Tt0=Tinlet for speed of sound at inlet
print(c6, T/(mdot_1+mdot_f))

#### Step 7 - Find Turbine Mass Flow ####
mdot_6 = mdot_1 + mdot_f
print(mdot_6, Pt4*A/(math.sqrt(R*Tt4))*math.sqrt(gn)*(1+(gn-1)/2)**((-gn-1)/(2*(gn-1))))
# is g6 1.3 or 1.4?

#### Print Statements ####
print(f'Cycle pressure ratio (P2/P1) is {pi}.')
print(f'Inlet mass flow (mdot_1) is {mdot_1} kg/s.')
print(f'Turbine inlet temperature (T3) is {Tt3} K.')
print(f'Specific thrust (t) is {t} N/kg.')
print(f'Specific fuel consumption (SFC) is {SFC} kg/(sK).')
