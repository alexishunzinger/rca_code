import numpy as np
import matplotlib.pyplot as plt
import pyart


def rca_func_error(filename, hPCT_on_50, vPCT_on_50, uncorrectedZ=True):
    """Calculates the 95th percentile clutter area reflectivity and RCA using baseline and clutter map for one particular day (all available PPI times)"""

    radar = pyart.aux_io.read_gamic(filename, file_field_names=True)
    date_time = radar.time["units"].replace("seconds since ", "")

    # Constrain range between 0 - 10 km
    # r_start_idx = np.where(radar.range['data'] < 1000.)[0][-1]+1
    r_start_idx = 0
    r_stop_idx = np.where(radar.range["data"] > 10000.)[0][0]

    # Using lowest elevation angle of PPI (0.5 deg)
    sweep_start_idx = radar.sweep_start_ray_index["data"][0]
    sweep_stop_idx = radar.sweep_end_ray_index["data"][0] + 1

    if uncorrectedZ == True:
        # Get variables (only the rays/gates needed)
        zh = radar.fields["UZh"]["data"][
            sweep_start_idx:sweep_stop_idx, r_start_idx:r_stop_idx
        ]
        zv = radar.fields["UZv"]["data"][
            sweep_start_idx:sweep_stop_idx, r_start_idx:r_stop_idx
        ]
        r = radar.range["data"][r_start_idx:r_stop_idx]
        theta = radar.azimuth["data"][sweep_start_idx:sweep_stop_idx]

        # Eliminate duplicate azimuths to maintain a total # of azimuths = 360
        if len(theta) > 360:
            diff = len(theta) - 360
            zh = np.delete(zh, -diff, axis=0)
            zv = np.delete(zv, -diff, axis=0)
            theta = np.delete(theta, -diff)

        # Arrange/sort azimuths to span 0 to 360 deg. from index 0 to 359
        sorted_idx = np.argsort(theta)
        zh = zh[sorted_idx, :]
        zv = zv[sorted_idx]
        theta = theta[sorted_idx]

        # Create a false error in reflectivity (add 1 dBZ to Zh, Zv)
        zh = zh + 1.
        zv = zv + 1.

        # H POLARIZATION
        # Find and store all reflectivity values that fall within the PCT_on > 0.5 grid gate
        zh_car = zh[np.isfinite(hPCT_on_50)]

        # Calculate the PDF of the clutter area reflectivity (CAR)
        n, bins = np.histogram(zh_car, bins=525, range=(-40., 65.))

        # Calculate CDF of clutter area reflectivity
        cdf = np.cumsum(n)
        p = cdf / cdf[-1] * 100

        # Find coefficients of 13th degree polynomial for CDF
        x = np.arange(525) * (1 / 5) - 40
        coeff = np.polyfit(p, x, 13)
        #coeff = np.polynomial.polynomial.polyfit(p, x, 13)
        poly_func = np.poly1d(coeff)

        # Find the value of reflectivity at the 95th percentile of CDF
        dbz95 = poly_func(95.)

        # V POLARIZATION
        # Find and store all reflectivity values that fall within the PCT_on > 0.5 grid gate
        zv_car = zv[np.isfinite(vPCT_on_50)]

        # Calculate the PDF of the clutter area reflectivity (CAR)
        vn, vbins = np.histogram(zv_car, bins=525, range=(-40., 65.))

        # Calculate CDF of clutter area reflectivity
        cdf = np.cumsum(vn)
        vp = cdf / cdf[-1] * 100

        # Find coefficients of 13th degree polynomial for CDF
        #x = np.arange(525) * (1 / 5) - 40
        coeff = np.polyfit(vp, x, 13)
        #coeff = np.polynomial.polynomial.polyfit(vp, x, 13)
        poly_func = np.poly1d(coeff)

        # Find the value of reflectivity at the 95th percentile of CDF
        dbz95_v = poly_func(95.)

    elif uncorrectedZ == False:
        # Get variables (only the rays/gates needed)
        zh = radar.fields["Zh"]["data"][
            sweep_start_idx:sweep_stop_idx, r_start_idx:r_stop_idx
        ]
        zv = radar.fields["Zv"]["data"][
            sweep_start_idx:sweep_stop_idx, r_start_idx:r_stop_idx
        ]
        r = radar.range["data"][r_start_idx:r_stop_idx]
        theta = radar.azimuth["data"][sweep_start_idx:sweep_stop_idx]

        # Eliminate duplicate azimuths to maintain a total # of azimuths = 360
        if len(theta) > 360:
            diff = len(theta) - 360
            zh = np.delete(zh, -diff, axis=0)
            zv = np.delete(zv, -diff, axis=0)
            theta = np.delete(theta, -diff)

        # Arrange/sort azimuths to span 0 to 360 deg. from index 0 to 359
        sorted_idx = np.argsort(theta)
        zh = zh[sorted_idx, :]
        zv = zv[sorted_idx]
        theta = theta[sorted_idx]

        # H POLARIZATION
        # Find and store all reflectivity values that fall within the PCT_on > 0.5 grid gate
        zh_car = zh[np.isfinite(hPCT_on_50)]

        # Calculate the PDF of the clutter area reflectivity (CAR)
        n, bins = np.histogram(zh_car, bins=525, range=(-40., 65.))

        # Calculate CDF of clutter area reflectivity
        cdf = np.cumsum(n)
        p = cdf / cdf[-1] * 100

        # Find coefficients of 13th degree polynomial for CDF
        x = np.arange(525) * (1 / 5) - 40
        #coeff = np.polynomial.polynomial.polyfit(p, x, 13)
        coeff = np.polyfit(p, x, 13)
        poly_func = np.poly1d(coeff)

        # Find the value of reflectivity at the 95th percentile of CDF
        dbz95 = poly_func(95.)

        # V POLARIZATION
        # Find and store all reflectivity values that fall within the PCT_on > 0.5 grid gate
        zv_car = zv[np.isfinite(vPCT_on_50)]

        # Calculate the PDF of the clutter area reflectivity (CAR)
        vn, vbins = np.histogram(zv_car, bins=525, range=(-40., 65.))

        # Calculate CDF of clutter area reflectivity
        cdf = np.cumsum(vn)
        vp = cdf / cdf[-1] * 100

        # Find coefficients of 13th degree polynomial for CDF
        #x = np.arange(525) * (1 / 5) - 40
        #coeff = np.polynomial.polynomial.polyfit(vp, x, 13)
        coeff = np.polyfit(vp, x, 13)
        poly_func = np.poly1d(coeff)

        # Find the value of reflectivity at the 95th percentile of CDF
        dbz95_v = poly_func(95.)

    del radar
    return date_time, dbz95, dbz95_v