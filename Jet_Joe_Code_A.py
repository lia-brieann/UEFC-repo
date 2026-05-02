# ####################################
# ########  16.004 Jet Joe A #########
# ####################################

# import numpy as np
# import matplotlib.pyplot as plt
# import math as math
# from scipy.optimize import fsolve

# # Input Parameters #
# r_outer = 55.24/2*10**(-3)   # [m]
# r_inner = 37.2/2*10**(-3)    # [m]
# RPM_list = [0, 50000, 88000, 160000, 0]
# B2 = 65 * (math.pi/180)      # radians
# a2 = 0       # radians
# # cps and gammas #
# R = 287.        # J/(kgK)
# gi = 1.4        # i = inlet
# gc = 1.4        # c = combustor
# gb = 1.3        # b = burner
# gt = 1.3        # t = turbine
# gn = 1.3        # n = nozzle
# cpc = gc*R/(gc-1)
# cpb = gb*R/(gb-1)
# cpt = gt*R/(gt-1)
# cpn = gn*R/(gn-1)

# label = ["Pre-test", "Idle", "Intermediate", "Max", "Post"]
# mdot_f_list = [0, 0.000225182, 0.00048688, 0.001290232, 0]  # [kg/s]
# h = 44.5 * 10**6      # [J/kg] fuel heating value
# Tt5_list = [273.15, 877.15, 843.15, 1083.15, 333.15]    # [K]
# inlet_pres_list = [0, 26.87472, 111.48032, 456.37256, 0.49768] # [Pa]
# Tt0_list = [288.65, 289.25, 289.15, 288.45, 288.45]    # [K]
# T_list = [0, 4.003398, 15.123948, 66.7233, 0.889644]     # [N]
# Tt3_list = [291.45, 294.65, 305.15, 340.15, 298.65]       # [K]
# Pt3_list = [100663.496, 113074.064, 139274.152, 259242.976, 100663.496]       # [Pa]
# cell_pres_list = [102594.0288, 102594.0288, 102594.0288, 102594.0288, 102594.0288]    # [Pa]
# for i in [0, 1, 2, 3, 4]:
#     Tt5 = Tt5_list[i]
#     Patm = cell_pres_list[i]
#     # P1 = cell_pres_list[i] - inlet_pres_list[i]
#     P1 = Patm
#     Tt0 = Tt0_list[i]
#     RPM = RPM_list[i]
#     mdot_f = mdot_f_list[i]
#     Tt6 = Tt5       # [K]
#     Tt1 = Tt0       # [K]
#     Tt2 = Tt0       # [K]

#     #### Step 1 - Find wsh_T ####
#     rm = (r_outer+r_inner)/2      # [m]
#     omega = RPM*(2*math.pi/60)
#     A = math.pi*(2*rm)/12*.00548      # [m^2]
#     a1 = math.acos((5.48*10**(-3))/(math.pi*rm/6))      # radians
#     phi  = 1/(math.tan(a2)-math.tan(B2))
#     lamb = phi*(math.tan(a1)-math.tan(a2))
#     wideal_T = lamb*(omega*rm)**2
#     print(f'widealT = {wideal_T}')

#     #### Step 2 - Assume Adiabatic Turbine and Compressor Efficiencies ####
#     nc = 0.7    # we changed these values by comparing mdot_6 to mdot_1+mdot_f
#     nt = 0.7    # we changed these values by comparing mdot_6 to mdot_1+mdot_f

#     #### Step 3 - Find Compressor Pressure Ratio ####
#     wideal_c = -wideal_T
#     wact_t = nt*wideal_T
#     wact_c = nc*wideal_c
#     Tt3 = wact_c/cpc + Tt2
#     Tt3act = Tt3_list[i]
#     print(f'Tt3 = {Tt3act, Tt3}, Tt2 = {Tt2}')
#     pi = (nc*(Tt3/Tt2 - 1) + 1)**(gc/(gc-1))
#     print(f'pi = {pi}')

#     #### Step 4 - Find Tt3 ####
#     def equations(vars):
#         mdot_1, Tt4 = vars
#         eq1 = mdot_1*cpb*(Tt4 - Tt3) - mdot_f*h
#         # print(mdot_1*cpb*(Tt4 - Tt3), mdot_f*h)
#         eq2 = mdot_1*cpc*(Tt2 - Tt3) - (mdot_1 + mdot_f)*cpt*(Tt5 - Tt4)
#         # print(mdot_1*cpc*(Tt2 - Tt3), (mdot_1 + mdot_f)*cpt*(Tt5 - Tt4))
#         return [eq1, eq2]
#     solution  = fsolve(equations, [1, 100])
#     mdot_1 = solution[0]
#     Tt4 = solution[1]
#     # print(f'mdot_1 = {mdot_1}, Tt4 = {Tt4}')

#     #### Step 5 - Determine Nozzle KE ####

#     # Pressures in Pa #
#     Pt2 = P1
#     # Pt3 = Pt2/pi
#     Pt3 = pi*Pt2
#     print(f'Pt3 = {Pt3}, {Pt3_list[i]}')
#     # Pt3 = Pt3_list[i]
#     Pt4 = 0.95*Pt3      # according to Joe during office hours
#     P6 = Patm
#     Pt5 = Pt4*(1 - (1-Tt5/Tt4)/nt)**(gt/(gt-1))
#     print(f'Pt5 = {Pt5}, Pt4 = {Pt4}')
#     Pt6 = Pt5
#     print(Pt6, P6)
#     T6 = Tt6*(Pt6/Patm)**(-gn/(gn-1))
#     print(Tt6, T6)
#     c6 = math.sqrt(2*cpn*(Tt6-T6))      # [m/s]
#     KE = .5*c6**2*(mdot_1+mdot_f)       # [W]

#     #### Step 6 - Find Specific Thrust, t, and SFC ####
#     SFC = mdot_f/((mdot_1+mdot_f)*c6)       # [s/m]
#     T = mdot_f/SFC      # [N]
#     # T = T_list[i]       # [N]
#     # if T == 0:
#     #     SFC = 0
#     # else:
#     #     SFC = mdot_f/T      # [s/m]
#     t = T/(mdot_1*math.sqrt(R*gi*Tt0))      # Tt0=Tinlet since the turbojet is stationary, this will change if it moves


#     #### Step 7 - Find Turbine Mass Flow ####
#     mdot_6 = 12*Pt4*A/(math.sqrt(R*Tt4))*math.sqrt(gn)*(1+(gn-1)/2)**((-gn-1)/(2*(gn-1)))
#     # print(mdot_1+mdot_f, mdot_6)

#     #### Print Statements ####
#     print(f'####### Thermodynamic cycle model outputs for {label[i]}: #######')
#     print(f'Cycle pressure ratio (P2/P1) is {pi:.2}.')
#     print(f'Inlet mass flow (mdot_1) is {mdot_1:.4} kg/s.')
#     print(f'Turbine inlet temperature (T3) is {Tt3:.4} K.')
#     print(f'Specific thrust (t) is {t:.4}.')
#     print(f'Specific fuel consumption (SFC) is {SFC:.2e} (s/m)).')
#     print(f'Nozzle exit mass flow (mdot_6) is {mdot_6:.4} kg/s.')
#     print(f'################################################################')


######################################
########## 16.004 Jet Joe A  #########
######################################

# import numpy as np
# import matplotlib.pyplot as plt
# import math as math
# from scipy.optimize import fsolve

# # Input Parameters #
# r_outer = 55.24/2*10**(-3)   # [m]
# r_inner = 37.2/2*10**(-3)    # [m]
# RPM = 160000.
# B2 = 65 * (math.pi/180)      # radians
# a2 = 0       # radians
# mdot_f = 0.000307119834  # [kg/s] from 6.5 oz/min * 60 s/min * 0.02834952 kg/oz
# h = 44.5 * 10**6      # [J/kg] fuel heating value
# Tt5 = 953.15    # [K]
# Tt6 = Tt5       # [K]
# Tt0 = 298.15    # [K]
# Tt1 = Tt0       # [K]
# Tt2 = Tt0       # [K]
# # cps and gammas #
# R = 287.        # J/(kgK)
# gi = 1.4        # i = inlet
# gc = 1.4        # c = combustor
# gb = 1.3        # b = burner
# gt = 1.3        # t = turbine
# gn = 1.3        # n = nozzle
# cpc = gc*R/(gc-1)
# cpb = gb*R/(gb-1)
# cpt = gt*R/(gt-1)
# cpn = gn*R/(gn-1)

# #### Step 1 - Fine wsh_T ####
# rm = (r_outer+r_inner)/2      # [m]
# omega = RPM*(2*math.pi/60)
# A = math.pi*(2*rm)/12*.00548      # [m^2]
# a1 = math.acos((5.48*10**(-3))/(math.pi*rm/6))      # radians
# phi  = 1/(math.tan(a2)-math.tan(B2))
# lamb = phi*(math.tan(a1)-math.tan(a2))
# wideal_T = lamb*(omega*rm)**2

# #### Step 2 - Assume Adiabatic Turbine and Compressor Efficiencies ####
# nc = 0.7    # we changed these values by comparing mdot_6 to mdot_1+mdot_f
# nt = 0.7    # we changed these values by comparing mdot_6 to mdot_1+mdot_f

# #### Step 3 - Find Compressor Pressure Ratio ####
# wideal_c = -wideal_T
# wact_c = wideal_c/nc
# Tt3 = wact_c/cpc + Tt2
# pi = (nc*(Tt3/Tt2 - 1) + 1)**(gc/(gc-1))

# #### Step 4 - Find Tt3 ####
# def equations(vars):
#     mdot_1, Tt4 = vars
#     eq1 = mdot_1*cpb*(Tt4 - Tt3) - mdot_f*h
#     eq2 = mdot_1*cpc*(Tt2 - Tt3) - (mdot_1 + mdot_f)*cpt*(Tt5 - Tt4)
#     return [eq1, eq2]
# solution  = fsolve(equations, [1, 1])
# mdot_1 = solution[0]
# Tt4 = solution[1]

# #### Step 5 - Determine Nozzle KE ####

# # Pressures in Pa #
# Patm = 101325.
# Pt2 = Patm
# Pt3 = Pt2*pi
# Pt4 = 0.95*Pt3      # according to Joe during office hours
# P6 = Patm
# Pt5 = Pt4*(1 - (1-Tt5/Tt4)/nt)**(gt/(gt-1))
# Pt6 = Pt5
# T6 = Tt6*(Pt6/Patm)**(-gn/(gn-1))
# c6 = math.sqrt(2*cpn*(Tt6-T6))      # [m/s]
# KE = .5*c6**2*(mdot_1+mdot_f)       # [W]

# #### Step 6 - Find Specific Thrust, t, and SFC ####
# SFC = mdot_f/((mdot_1+mdot_f)*c6)       # [s/m]
# T = mdot_f/SFC      # [N]
# t = T/(mdot_1*math.sqrt(R*gi*Tt0))        # Tt0=Tinlet since the turbojet is stationary, this will change if it moves

# #### Step 7 - Find Turbine Mass Flow ####
# mdot_6 = 12*Pt4*A/(math.sqrt(R*Tt4))*math.sqrt(gn)*(1+(gn-1)/2)**((-gn-1)/(2*(gn-1)))
# # print(mdot_1+mdot_f, mdot_6)


# #### Print Statements ####
# print("####### Thermodynamic cycle and mean-line model outputs: #######")
# print(f'Cycle pressure ratio (P2/P1) is {pi:.2}.')
# print(f'Inlet mass flow (mdot_1) is {mdot_1:.4} kg/s.')
# print(f'Turbine inlet temperature (T3) is {Tt3:.4} K.')
# print(f'Specific thrust (t) is {t:.4}.')
# print(f'Specific fuel consumption (SFC) is {SFC:.2e} (s/m)).')
# print(f'Nozzle exit mass flow (mdot_6) is {mdot_6:.4} kg/s.')
# print(f'################################################################')

#################################################
########  16.004 Jet Joe D Best Version #########
#################################################

import numpy as np
import matplotlib.pyplot as plt
import math as math
from scipy.optimize import fsolve

# Input Parameters #
r_outer = 55.24/2*10**(-3)   # [m]
r_inner = 37.2/2*10**(-3)    # [m]
RPM_list = [0, 50000, 88000, 160000, 0]
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

label = ["Pre-test", "Idle", "Intermediate", "Max", "Post"]
mdot_f_list = [0, 0.000225182, 0.00048688, 0.001290232, 0]      # [kg/s]
h = 44.5 * 10**6      # [J/kg] fuel heating value
Tt5_list = [273.15, 877.15, 843.15, 1083.15, 333.15]    # [K]
inlet_pres_list = [0, 26.87472, 111.48032, 456.37256, 0.49768]      # [Pa]
Tt0_list = [288.65, 289.25, 289.15, 288.45, 288.45]    # [K]
T_list = [0, 4.003398, 15.123948, 66.7233, 0.889644]     # [N]
Tt3_list = [291.45, 294.65, 305.15, 340.15, 298.65]       # [K]
Pt3_list = [100663.496, 113074.064, 139274.152, 259242.976, 100663.496]       # [Pa]
cell_pres_list = [102594.0288, 102594.0288, 102594.0288, 102594.0288, 102594.0288]    # [Pa]
for i in [0, 1, 2, 3, 4]:
    Tt5 = Tt5_list[i]
    Patm = cell_pres_list[i]
    # P1 = cell_pres_list[i] - inlet_pres_list[i]
    P1 = Patm
    Tt0 = Tt0_list[i]
    RPM = RPM_list[i]
    mdot_f = mdot_f_list[i]
    Tt6 = Tt5       # [K]
    Tt1 = Tt0       # [K]
    Tt2 = Tt0       # [K]

    #### Step 1 - Find wsh_T ####
    rm = (r_outer+r_inner)/2      # [m]
    omega = RPM*(2*math.pi/60)
    A = math.pi*(2*rm)/12*.00548      # [m^2]
    a1 = math.acos((5.48*10**(-3))/(math.pi*rm/6))      # radians
    phi  = 1/(math.tan(a2)-math.tan(B2))
    lamb = phi*(math.tan(a1)+math.tan(a2))
    wideal_T = lamb*(omega*rm)**2
    print(f'widealT = {wideal_T}, lambda = {lamb}')

    #### Step 2 - Assume Adiabatic Turbine and Compressor Efficiencies ####
    nc = 0.7    # we changed these values because other numbers gave very wrong values
    nt = 0.5    # we changed these values to get something that didn't break the code

    #### Step 3 - Find Compressor Pressure Ratio ####
    wideal_c = -wideal_T
    wact_t = nt*wideal_T
    wact_c = wideal_c/nc
    Tt3 = wact_c/cpc + Tt2
    Tt3act = Tt3_list[i]
    print(f'wact_c = {wact_c}, Tt3 = {Tt3act, Tt3}, Tt2 = {Tt2}')
    pi = (nc*(Tt3/Tt2 - 1) + 1)**(gc/(gc-1))
    print(f'pi = {pi}')

    #### Step 4 - Find Tt3 ####
    def equations(vars):
        mdot_1, Tt4 = vars
        eq1 = mdot_1*cpb*(Tt4 - Tt3) - mdot_f*h
        eq2 = mdot_1*cpc*(Tt2 - Tt3) - (mdot_1 + mdot_f)*cpt*(Tt5 - Tt4)
        return [eq1, eq2]
    solution  = fsolve(equations, [0.01, 100])
    mdot_1 = solution[0]
    Tt4 = solution[1]
    print(f'check: {mdot_f*h/(cpb*(Tt4-Tt3))} = {mdot_f*cpt*(Tt5-Tt4)/(cpc*(Tt2-Tt3)-cpt*(Tt5-Tt4))}')
    print(f'mdot_1 = {mdot_1}, Tt4 = {Tt4}')

    #### Step 5 - Determine Nozzle KE ####

    # Pressures in Pa #
    Pt2 = P1
    Pt3 = pi*Pt2
    print(f'Pt3 = {Pt3}, {Pt3_list[i]}')
    Pt4 = Pt3
    P6 = Patm
    Pt5 = Pt4*(1 - (1-Tt5/Tt4)/nt)**(gt/(gt-1))
    print(f'Pt5 = {Pt5}, Pt4 = {Pt4}, Tt4 = {Tt4}')
    Pt6 = Pt5
    print(f'Pt6 = {Pt6}, P6 = {P6}')
    T6 = Tt6*(P6/Pt6)**((gn-1)/gn)
    print(f'Tt6 = {Tt6}, T6 = {T6}')
    c6 = math.sqrt(2*cpn*(Tt6-T6))      # [m/s]
    KE = .5*c6**2*(mdot_1+mdot_f)       # [W]

    #### Step 6 - Find Specific Thrust, t, and SFC ####
    SFC = mdot_f/((mdot_1+mdot_f)*c6)       # [s/m]
    T = mdot_f/SFC      # [N]
    t = T/(mdot_1*math.sqrt(R*gi*Tt0))      # Tt0=Tinlet since the turbojet is stationary, this will change if it moves

    #### Step 7 - Find Turbine Mass Flow ####
    mdot_6 = 12*Pt4*A/(math.sqrt(R*Tt4))*math.sqrt(gn)*(1+(gn-1)/2)**((-gn-1)/(2*(gn-1)))
    # mdot_6 = mdot_1 + mdot_f

    #### Print Statements ####
    print(f'####### Thermodynamic cycle model outputs for {label[i]}: #######')
    print(f'Cycle pressure ratio (P2/P1) is {pi:.2}.')
    print(f'Inlet mass flow (mdot_1) is {mdot_1:.4} kg/s.')
    print(f'Turbine inlet temperature (T4) is {Tt4:.4} K.')
    print(f'Specific thrust (t) is {t:.4}.')
    print(f'Specific fuel consumption (SFC) is {SFC:.2e} (s/m)).')
    print(f'Nozzle exit mass flow (mdot_6) is {mdot_6:.4} kg/s.')
    print(f'################################################################')

# # from Jet_Joe_Code_D import drone_range

# # drone_range(mdot_f_list[3], t, mdot_6)


# import numpy as np
# import matplotlib.pyplot as plt
# import math as math
# from scipy.optimize import fsolve

# # Input Parameters #
# r_outer = 55.24/2*10**(-3)   # [m]
# r_inner = 37.2/2*10**(-3)    # [m]
# RPM_list = [0, 50000, 88000, 160000, 0]
# B2 = 65 * (math.pi/180)      # radians
# a2 = 0       # radians
# # cps and gammas #
# R = 287.        # J/(kgK)
# gi = 1.4        # i = inlet
# gc = 1.4        # c = combustor
# gb = 1.3        # b = burner
# gt = 1.3        # t = turbine
# gn = 1.3        # n = nozzle
# cpc = gc*R/(gc-1)
# cpb = gb*R/(gb-1)
# cpt = gt*R/(gt-1)
# cpn = gn*R/(gn-1)

# label = ["Pre-test", "Idle", "Intermediate", "Max", "Post"]
# mdot_f_list = [0, 0.000225182, 0.00048688, 0.001290232, 0]  # [kg/s]
# h = 44.5 * 10**6      # [J/kg] fuel heating value
# Tt5_list = [288.65, 877.15, 843.15, 1083.15, 288.45]    # [K]
# inlet_pres_list = [0, 26.87472, 111.48032, 456.37256, 0.49768] # [Pa]
# Tt0_list = [288.65, 289.25, 289.15, 288.45, 288.45]    # [K]
# T_list = [0, 4.003398, 15.123948, 66.7233, 0.889644]     # [N]
# Tt3_list = [291.45, 294.65, 305.15, 340.15, 298.65]       # [K]
# Pt3_list = [100663.496, 113074.064, 139274.152, 259242.976, 100663.496]       # [Pa]
# cell_pres_list = [102594.0288, 102594.0288, 102594.0288, 102594.0288, 102594.0288]    # [Pa]
# for i in [0, 1, 2, 3, 4]:
#     Tt5 = Tt5_list[i]
#     Patm = cell_pres_list[i]
#     # P1 = cell_pres_list[i] - inlet_pres_list[i]
#     P1 = Patm
#     Tt0 = Tt0_list[i]
#     RPM = RPM_list[i]
#     mdot_f = mdot_f_list[i]
#     Tt6 = Tt5       # [K]
#     Tt1 = Tt0       # [K]
#     Tt2 = Tt0       # [K]

#     #### Step 1 - Find wsh_T ####
#     rm = (r_outer+r_inner)/2      # [m]
#     omega = RPM*(2*math.pi/60)
#     A = math.pi*(2*rm)/12*.00548      # [m^2]
#     a1 = math.acos((5.48*10**(-3))/(math.pi*rm/6))      # radians
#     phi  = 1/(math.tan(a2)-math.tan(B2))
#     lamb = phi*(math.tan(a1)+math.tan(a2))
#     wideal_T = lamb*(omega*rm)**2
#     print(f'widealT = {wideal_T}, lambda = {lamb}')

#     #### Step 2 - Assume Adiabatic Turbine and Compressor Efficiencies ####
#     nc = 0.7    # we changed these values by comparing mdot_6 to mdot_1+mdot_f
#     nt = 0.7    # we changed these values by comparing mdot_6 to mdot_1+mdot_f

#     #### Step 3 - Find Compressor Pressure Ratio ####
#     wideal_c = -wideal_T
#     wact_t = nt*wideal_T
#     wact_c = wideal_c/nc
#     Tt3 = wact_c/cpc + Tt2
#     Tt3act = Tt3_list[i]
#     print(f'Tt3 = {Tt3act, Tt3}, Tt2 = {Tt2}')
#     pi = (nc*(Tt3/Tt2 - 1) + 1)**(gc/(gc-1))
#     print(f'pi = {pi}')

#     #### Step 4 - Find Tt3 ####
#     def equations(vars):
#         mdot_1, Tt4 = vars
#         eq1 = mdot_1*cpb*(Tt4 - Tt3) - mdot_f*h
#         # print(mdot_1*cpb*(Tt4 - Tt3), mdot_f*h)
#         eq2 = mdot_1*cpc*(Tt2 - Tt3) - (mdot_1 + mdot_f)*cpt*(Tt5 - Tt4)
#         # print(mdot_1*cpc*(Tt2 - Tt3), (mdot_1 + mdot_f)*cpt*(Tt5 - Tt4))
#         return [eq1, eq2]
#     solution  = fsolve(equations, [1, 100])
#     mdot_1 = solution[0]
#     Tt4 = Tt3
#     # print(f'check: {mdot_f*h/(cpb*(Tt4-Tt3))} = {mdot_f*cpt*(Tt5-Tt4)/(cpc*(Tt2-Tt3)-cpt*(Tt5-Tt4))}')
#     print(f'mdot_1 = {mdot_1}, Tt4 = {Tt4}')

#     #### Step 5 - Determine Nozzle KE ####

#     # Pressures in Pa #
#     Pt2 = P1
#     # Pt3 = Pt2/pi
#     Pt3 = pi*Pt2
#     print(f'Pt3 = {Pt3}, {Pt3_list[i]}')
#     # Pt3 = Pt3_list[i]
#     Pt4 = Pt3      # according to Joe during office hours
#     P6 = Patm
#     Pt5 = Pt4*(1 - (1-Tt5/Tt4)/nt)**(gt/(gt-1))
#     print(f'Pt5 = {Pt5}, Pt4 = {Pt4}, Tt4 = {Tt4}')
#     Pt6 = Pt5
#     print(f'Pt6 = {Pt6}, P6 = {P6}')
#     T6 = Tt6*(Pt6/Patm)**(-gn/(gn-1))
#     print(f'Tt6 = {Tt6}, T6 = {T6}')
#     c6 = math.sqrt(2*cpn*(Tt6-T6))      # [m/s]
#     KE = .5*c6**2*(mdot_1+mdot_f)       # [W]

#     #### Step 6 - Find Specific Thrust, t, and SFC ####
#     SFC = mdot_f/((mdot_1+mdot_f)*c6)       # [s/m]
#     T = mdot_f/SFC      # [N]
#     # T = T_list[i]       # [N]
#     # if T == 0:
#     #     SFC = 0
#     # else:
#     #     SFC = mdot_f/T      # [s/m]
#     t = T/(mdot_1*math.sqrt(R*gi*Tt0))      # Tt0=Tinlet since the turbojet is stationary, this will change if it moves


#     #### Step 7 - Find Turbine Mass Flow ####
#     mdot_6 = 12*Pt4*A/(math.sqrt(R*Tt4))*math.sqrt(gn)*(1+(gn-1)/2)**((-gn-1)/(2*(gn-1)))
#     # print(mdot_1+mdot_f, mdot_6)

#     #### Print Statements ####
#     print(f'####### Thermodynamic cycle model outputs for {label[i]}: #######')
#     print(f'Cycle pressure ratio (P2/P1) is {pi:.2}.')
#     print(f'Inlet mass flow (mdot_1) is {mdot_1:.4} kg/s.')
#     print(f'Turbine inlet temperature (T4) is {Tt4:.4} K.')
#     print(f'Specific thrust (t) is {t:.4}.')
#     print(f'Specific fuel consumption (SFC) is {SFC:.2e} (s/m)).')
#     print(f'Nozzle exit mass flow (mdot_6) is {mdot_6:.4} kg/s.')
#     print(f'#######################################################')
