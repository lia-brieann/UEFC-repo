from GetUEFC import UEFC
import numpy as np
import os
from DS_report_opt_obj import report_opt_obj
from opt_obj import opt_obj
import matplotlib.pyplot as plt
import matplotlib.cm as cm
plt.style.use(os.path.join(os.path.dirname(__file__), "uefc.mplstyle"))

from DS_mpay_sweep import mpay_sweep
from DS_scan_ARS import scan_ARS
from DS_report_opt_obj import report_opt_obj


if __name__ == "__main__":

    aircraft = UEFC()

    # design parameters
    aircraft.mpay_g   = 250    # payload weight in grams
    S  = np.nan                  # Wing area (m^2)
    AR = np.nan                  # Wing aspect ratio
    aircraft.taper    = 0.50   # taper ratio
    aircraft.dihedral = 10   # Wing dihedral (degrees)
    aircraft.tau      = 0.12  # thickness-to-chord ratio
    aircraft.Sh = 0.04 # Wing area of horizontal tail (m^2)
    aircraft.Sv = 0.03 # Wing area of vertical tail (m^2)
    aircraft.l_AR = 1.63 # Fuselage length to wingspan ratio (-)
    aircraft.CLdes = 0.75  # maximum CL wing will be designed to fly at (in cruise)
    aircraft.e0    = 1.0  # Span efficiency for straight level flight
    aircraft.dbmax    = 0.10  # tip displacement bending constraint
    aircraft.rhofoam  = 32.     # kg/m^3. high load foam
    aircraft.Efoam    = 19.3E6  # Pa.     high load foam
    num_division = 41

    # run necessary simulations
    mpay_sweep()
    scan_ARS()
    report_opt_obj()
    # TODO: also need to do wing simulation?
