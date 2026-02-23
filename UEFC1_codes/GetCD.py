import numpy as np

def GetCD(UEFC, opt_vars, AR, S):

    # HINT: we have functions for these in the UEFC calss

    # Profile drag
    CDp = np.nan

    # Induced drag coefficient
    CDi = np.nan

    # Fuselage drag model
    CDfuse = np.nan

    # Payload drag coefficient increment
    CDpay = np.nan

    # Total drag coefficient
    CD = CDfuse + CDp + CDi + CDpay

    return {
            "Total": CD,
            "Breakdown": {
                    "Fuselage": CDfuse,
                    "Wing":     CDp,
                    "Payload":  CDpay,
                    "Induced":  CDi,
                    }
            }

# DO NOT MODIFY THIS
def check_close(truth_val, test_val, close_tol):
    return np.abs(truth_val - test_val) < close_tol

def tests() -> None:
    # DO NOT CHANGE THE VALUES HERE
    from GetUEFC        import UEFC
    aircraft = UEFC()
    aircraft.mpay_g = 250. # set payload mass (g)
    aircraft.tau = 0.12
    aircraft.taper = 0.7
    aircraft.dbmax = 0.10
    AR = 9
    S = 0.354
    opt_vars = np.array([1.1]) # load factor
    cd_breakdown = GetCD(aircraft, opt_vars, AR, S)
    CLOSE_TOL = 1E-10

    assert check_close(cd_breakdown["Total"], 0.053325915568752255, CLOSE_TOL)
    assert check_close(cd_breakdown["Breakdown"]['Fuselage'], 0.014538606403013183, CLOSE_TOL)
    assert check_close(cd_breakdown["Breakdown"]['Wing'], 0.021508608136407932, CLOSE_TOL)
    assert check_close(cd_breakdown["Breakdown"]['Payload'], 0.0, CLOSE_TOL)
    assert check_close(cd_breakdown["Breakdown"]['Induced'], 0.017278701029331146, CLOSE_TOL)

    aircraft = UEFC()
    aircraft.mpay_g = 280. # set payload mass (g)
    aircraft.tau = 0.10
    aircraft.taper = 0.4
    aircraft.dbmax = 0.05
    AR = 11
    S = 0.7
    opt_vars = np.array([1.06]) # load factor
    cd_breakdown = GetCD(aircraft, opt_vars, AR, S)

    assert check_close(cd_breakdown["Total"], 0.044856724898180766, CLOSE_TOL)
    assert check_close(cd_breakdown["Breakdown"]['Fuselage'], 0.011746031746031746, CLOSE_TOL)
    assert check_close(cd_breakdown["Breakdown"]['Wing'], 0.021868070895473282, CLOSE_TOL)
    assert check_close(cd_breakdown["Breakdown"]['Payload'], 0.0, CLOSE_TOL)
    assert check_close(cd_breakdown["Breakdown"]['Induced'], 0.01124262225667574, CLOSE_TOL)

    print(f"==> All GetCD tests have passed!")

if __name__ == "__main__":
    tests()