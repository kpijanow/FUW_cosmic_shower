class Constants:
    cable_length = 15
    det_X = calbelength * [1, 1, -1, -1]
    det_Y = cable_length * [1, -1, -1, 1]
    det_area = 0.31 * 0.27
    readOut_eff = 0.95
    det_eff = 0.75

    getDet_X():
        return det_X

    getDet_Y():
        return det_Y

    getDet_area():
        return det_area

    getDet_eff():
        return det_eff

    getReadOut_eff():
        return readOut_eff

    setDet_X(det_X0):
        det_X = det_X0

    setDet_Y(det_Y0):
        det_Y = det_Y0
    
