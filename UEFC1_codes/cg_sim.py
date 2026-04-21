import numpy as np
import matplotlib.pyplot as plt


def staticmargin(c, lh, bh, S, Sh, Sv, lv, AR, fe, Clwnom, CMWnom):
    """
    c - chord of wings
    lh - length to the midpoint of the horizontal part of the tail
    bh - length of the horizontal part of the tail
    S - surface area of wing
    Sh - surface area of horizontal part of tail
    AR - aspect ratio wings
    fe - literally no clue use 0.6
    Clwnom - nomimal lift coeff, comes from wing choice
    CMWnom - nominal wing moment, comes from wing choice
    """
    ARh = (bh)**2/Sh

    #calculating additional parameters
    Vh = Sh*lh/(S*c)
    Vv = Sv*lv/(S*c)
    ah = 2*np.pi/(1+2/ARh)
    aw = 2*np.pi/(1+2/AR)
    zetae = np.arccos(1-2*fe)
    ae = 2*(np.pi-zetae+np.sin(zetae))

    #initalizing elevator trim
    aetrim = np.linspace(-10, 10, 1000)
    aerad = aetrim*(np.pi/180)

    #find alpha and alpha in degrees
    alpha = -(aerad*Vh*(c/lh))/((aw/ae)+Vh*(c/lh)*(ah/ae))
    alphadeg = alpha * (180/np.pi)

    CLW = Clwnom + aw*alpha
    CLH = ah*alpha+ae*aerad

    #finding x_cg/c
    x_cgoverc = (1/4*CLW+(1+1/4*c/lh)*Vh*CLH-CMWnom)/(CLW+Vh*CLH*c/lh)

    #finding static margin
    xnpoverc = ((0.25 * aw/ah) + (Vh*(1 + 0.25*(c/lh))))/ ((aw/ah) + ((c/lh)*Vh))
    SM = xnpoverc - x_cgoverc


    print("\n##### cg_sim Output #####\n")
    print(f'\nVh = {Vh}')
    print(f'Vv = {Vv}\n')
    print(f'Clwnom = {Clwnom}\n')
    print(f'CMWnom = {CMWnom}\n')
    print("\n#############################\n")

    plt.plot(aetrim, SM)
    plt.xlabel('aetrim')
    plt.ylabel('SM')
    plt.title("Static Margin vs. Trim")
    plt.grid(True)
    plt.show()

    return x_cgoverc, SM

def change_in_cm(c, lh, S, Sh, AR, ARh, fe, Clwnom):
    #this function is not finished because it doesn't account for the changing masses yet

    Vh = Sh*lh/(S*c)
    ah = 2*np.pi/(1+2/ARh)
    aw = 2*np.pi/(1+2/AR)
    zetae = np.arccos(1-2*fe)
    ae = 2*(np.pi-zetae+np.sin(zetae))

    aetrim = np.linspace(-10, 10, 1000)
    aerad = aetrim*(np.pi/180)

    #find alpha and alpha in degrees
    alpha = -(aerad*Vh*(c/lh))/((aw/ae)+Vh*(c/lh)*(ah/ae))
    alphadeg = alpha * (180/np.pi)

    CLW = Clwnom+aw*alpha
    CLH = ah*alpha+ae*aerad

    x_cgoverc = (1/4*CLW+(1+1/4*c/lh)*Vh*CLH-CMWnom)/(CLW+Vh*CLH*c/lh)

    xpayoverc = (0.2*630*x_cgoverc*100-3352.8)/(250*0.2*100) #convert from cm to m before dividing by c you dumbass
    changex_cg = x_cgoverc - 0.481
    changex_payload = xpayoverc-0.54

    return changex_cg, changex_payload
