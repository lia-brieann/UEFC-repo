import numpy as np
import matplotlib.pyplot as plt
import scipy as scipy


#parameters
c = 0.2
lh = 0.65
Sh = 0.04
S = 0.354
Vh = 0.367
AR = 9
ARh = (0.525)**2/0.04
fe = 0.6
Clwnom = 0.75
CMWnom = -0.15

def staticmargin(c, lh, S, Sh, AR, ARh, fe, Clwnom):

    #calculating additional parameters
    Vh = Sh*lh/(S*c)
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

    CLW = Clwnom+aw*alpha
    CLH = ah*alpha+ae*aerad

    #finding x_cg/c
    x_cgoverc = (1/4*CLW+(1+1/4*c/lh)*Vh*CLH-CMWnom)/(CLW+Vh*CLH*c/lh)

    #finding static margin
    xnpoverc = ((0.25 * aw/ah) + (Vh*(1 + 0.25*(c/lh))))/ ((aw/ah) + ((c/lh)*Vh))
    SM = xnpoverc - x_cgoverc

    return x_cgoverc, SM


def change_in_cm(x_cgoverc, m_payload, Sh, Sv): #finding the change in the cg and the change in payload location v elevator trim
    Xempty, m_empty, l_nose = weight(0.195, Sh, Sv, 0.766, x_cgoverc, 0.156)
    x_cgoverc = np.array(x_cgoverc)

    xpayoverc = ((m_empty+m_payload)*x_cgoverc - (m_empty*Xempty))/m_payload

    changex_cg = x_cgoverc - Xempty
    changex_payload = xpayoverc - Xempty

    return changex_cg, changex_payload, l_nose

def weight(S, Sh, Sv, l, xcgoverc, c = 0.156):
    m_nose = 94.2 #g
    m_tail = (Sh+Sv)/0.07*14 #g
    m_wing = 64
    m_rbwm = 132.8 + 9.1 + 12*S/0.354
    m_servo = 16.6
    m_fuselage = 38.9*l/0.92
    m_prhw = 24 * l/0.92

    m_other = m_nose + m_tail + m_wing + m_rbwm + m_servo + m_fuselage + m_prhw

    def xcg(l_nose):

        num = m_nose*(l_nose) + m_tail*(l+l_nose) + m_wing*0.25*c + m_rbwm*0.5*c + m_servo*1.5*c + m_fuselage*(0.5*l+l_nose) + m_prhw*((l+1.5*c)*0.5+l_nose)

        xovercgnom = (num / (m_other*c) - xcgoverc[500])
        return xovercgnom

    l_nose = scipy.optimize.root(xcg, -.13).x[0]

    num = m_nose*(l_nose) + m_tail*(l+l_nose) + m_wing*0.25*c + m_rbwm*0.5*c + m_servo*1.5*c + m_fuselage*(0.5*l+l_nose) + m_prhw*((l+1.5*c)*0.5+l_nose)
    xovercgnom = num / (m_other*c)
    return xovercgnom, m_other, l_nose
