from GetUEFC import UEFC
from UEFC_wing import UEFC_wing
from GetWingWeight import GetWingWeight
from vlm import vlm
import numpy as np
import os
from DS_report_opt_obj import report_opt_obj
from opt_obj import opt_obj
import matplotlib.pyplot as plt
import matplotlib.cm as cm
plt.style.use(os.path.join(os.path.dirname(__file__), "uefc.mplstyle"))
import scipy as scipy

from DS_mpay_sweep import mpay_sweep
from DS_scan_ARS import scan_ARS
from DS_report_opt_obj import report_opt_obj

from SM5 import staticmargin
from SM5 import change_in_cm
from SM5 import weight


if __name__ == "__main__":

    aircraft = UEFC()

    # design parameters (UEW-12-040)
    aircraft.mpay_g   = 250    # payload weight in grams
    aircraft.taper    = 0.60   # taper ratio
    aircraft.dihedral = 12.97   # Wing dihedral (degrees)
    aircraft.tau      = 0.12  # thickness-to-chord ratio
    aircraft.Sh = 0.033 # Wing area of horizontal tail (m^2)
    aircraft.Sv = 0.03 # Wing area of vertical tail (m^2)
    aircraft.l_AR = 1.63 # Fuselage length to wingspan ratio (-)
    aircraft.CLdes = 0.63  # maximum CL wing will be designed to fly at (in cruise)
    aircraft.e0    = 1.00  # Span efficiency for straight level flight
    aircraft.dbmax    = 0.10  # tip displacement bending constraint (<= 0.1)
    aircraft.rhofoam  = 25.2     # kg/m^3. high load foam
    aircraft.Efoam    = 19.3E6  # Pa.     high load foam


    ##### PART 1 SIMS #####
    # scan_ARS
    AR_start = 1.0
    AR_end = 15.0
    S_start = 0.1
    S_end = 2.0
    num_division = 50
    obj_opt, ARopt, Sopt = scan_ARS(aircraft, AR_start, AR_end, S_start, S_end, num_division, show_plots=True)

    S  = Sopt                # Wing area (m^2)
    AR = ARopt               # Wing aspect ratio
    print(f'\nARopt = {ARopt}')
    print(f'Sopt = {Sopt}\n')

    # mpay_sweep
    mpay_start = 200  # g
    mpay_end   = 300  # g
    mpay_num   = 101

    fig, ax = plt.subplots(3, 2, figsize=(15*0.75, 11*0.75))
    ax, mpay, obj, CL, CD, T_req, T_max, db, N = mpay_sweep(ax, 1, aircraft,
                                                        AR, S,
                                                        mpay_start=mpay_start,
                                                        mpay_end=mpay_end,
                                                        mpay_num=mpay_num,
                                                        show_plot=True)
    print("\n##### mpay_sweep Output #####\n")
    print(f"mpay = {mpay[50]}\nCL = {CL[50]}\nCD = {CD[50]}\nT_req = {T_req[50]}\nT_max = {T_max[50]}\ndb = {db[50]}\nN = {N[50]}")
    print("\n#############################\n")
    suptitle = (f"$AR = {AR:.1f}$, $S = {S:.3f}$ m$^2$, \n $C_{{L_{{\\mathrm{{des}}}}}} = {aircraft.CLdes:.2f}$,"
                "$\\lambda = {aircraft.taper:.2f}$, $\\tau = {aircraft.tau}$, $(\\delta/b)_{{\\mathrm{{max}}}} = {aircraft.dbmax}$")
    fig.suptitle(suptitle)
    plt.show()

    CL = CL[50]

    # report_opt_obj
    aircraft.mpay_g   = 250
    report_opt_obj(aircraft, AR, S)

    #########################


    ##### STATIC MARGIN #####
    c = aircraft.wing_dimensions(AR, S)["Mean chord"]
    b = aircraft.wing_dimensions(AR, S)["Span"]

    lv = 0.45
    lh = 0.54
    bh = 0.42

    fe = 0.6
    Clwnom = CL
    CMWnom = -0.13
    ARh = bh**2/aircraft.Sh

    x_cgoverc, SM, xnpoverc = staticmargin(c, lh,S, aircraft.Sh, AR, ARh, fe, Clwnom, CMWnom)
    print("X_cg empty", x_cgoverc[500]*c)
    print(f'xnpoverc = {xnpoverc}')

    #########################


    ##### WING ANALYSIS #####
    b        = aircraft.wing_dimensions(AR, S)["Span"]
    croot    = aircraft.wing_dimensions(AR, S)["Root chord"]
    ctip     = aircraft.wing_dimensions(AR, S)["Tip chord"]
    print(f'c = {aircraft.wing_dimensions(AR, S)["Mean chord"]}')
    print(f'croot = {croot}')
    print(f'b = {b}')
    agroot   = 3.0; root_angle = agroot
    washout_diff = -5.0
    agtip    = root_angle  + washout_diff
    dihedral = aircraft.dihedral
    wing = UEFC_wing(b=b, croot=croot, ctip=ctip, agroot=agroot, agtip=agtip, dihedral=dihedral)

    vlm(wing, CL, root_angle, washout_diff)
    B = lv/b * dihedral/CL

    l = b / aircraft.l_AR
    changex_cg, changex_payload, l_nose = change_in_cm(aircraft, AR, S, l, x_cgoverc, 250, aircraft.Sh, aircraft.Sv)

    print(f'l = {l}')
    print(f'l_nose = {l_nose}')
    d = l - (-l_nose + c*x_cgoverc[500] + lh)
    print(f'\n d = {d} ( >0.02 )\n')

    aetrim = np.linspace(-10, 10, 1000)
    plt.figure()
    plt.plot(aetrim, changex_payload, color = "#9900FF", label = "change in x payload")
    plt.plot(aetrim, changex_cg, color = "#0051FF", label = "change in x cg")
    plt.plot(aetrim, SM, color = "#00FFFF", label = "SM")
    plt.legend()
    plt.xlabel("aetrim")
    plt.title("Change in cg vs Trim")
    plt.suptitle(f'lh = {lh}, bh = {bh}, Sh = {aircraft.Sh}, Sv = {aircraft.Sv}')
    plt.grid()
    plt.show()

    print("\n##### vlm Output #####\n")
    print(f"B = {B} (must be >= 5)")
    print(f"AR = {wing.get_AR()} vs. ARopt = {ARopt}")
    print(f"S = {wing.get_S()} vs. Sopt = {Sopt}")
    print(f"wing weight = {GetWingWeight(aircraft, AR, S)} g")

    print("\n#############################\n")
    #########################
