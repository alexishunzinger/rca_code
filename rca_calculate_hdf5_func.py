def rca_calculate_hdf5_func(filename, PCT_on_50, vPCT_on_50):
    '''Calculates the 95th percentile clutter area reflectivity and RCA using baseline and clutter map for one particular day (all available PPI times)'''
    
    import numpy as np
    import matplotlib.pyplot as plt
    import pyart    
    #from netCDF4 import Dataset

    #dataset = Dataset('/home/hunzinger/data/rca_baseline_20181109.nc')
    #PCT_on_50 = dataset.variables['Flagged clutter grid gates'][:,:]
    #vPCT_on_50 = dataset.variables['Flagged clutter grid gates (V)'][:,:]
    #dbz95_baseline = dataset.variables['Baseline 95th reflectivity'][:]
    #vdbz95_baseline = dataset.variables['Baseline 95th reflectivity (V)'][:]
    #dataset.close()
    
    radar = pyart.aux_io.read_gamic(filename, file_field_names=True) 
    date_time = radar.time['units'].replace('seconds since ', '')
    
    # Constrain range between 0 - 10 km
    #r_start_idx = np.where(radar.range['data'] < 1000.)[0][-1]+1
    r_start_idx = 0
    r_stop_idx = np.where(radar.range['data'] > 10000.)[0][0]
    
    # Using lowest elevation angle of PPI (0.5 deg)
    sweep_start_idx = radar.sweep_start_ray_index['data'][0]
    sweep_stop_idx = radar.sweep_end_ray_index['data'][0]+1
    
    # Get variables (only the rays/gates needed)
    zh = radar.fields['Zh']['data'][sweep_start_idx:sweep_stop_idx,r_start_idx:r_stop_idx]
    zv = radar.fields['Zv']['data'][sweep_start_idx:sweep_stop_idx,r_start_idx:r_stop_idx]
    r = radar.range['data'][r_start_idx:r_stop_idx]
    theta = radar.azimuth['data'][sweep_start_idx:sweep_stop_idx]
    
    # Eliminate duplicate azimuths to maintain a total # of azimuths = 360
    if len(theta) > 360:
        diff = len(theta) - 360
        zh = np.delete(zh,-diff,axis=0)
        zv = np.delete(zv,-diff,axis=0)
        theta = np.delete(theta,-diff)
        
    # Arrange/sort azimuths to span 0 to 360 deg. from index 0 to 359
    sorted_idx = np.argsort(theta)
    zh = zh[sorted_idx,:]
    zv = zv[sorted_idx]
    theta = theta[sorted_idx]
    
    # Create array to store qualifying reflectivities (fall within PCT_on > 0.5)
    zh_car = np.empty((zh.shape))
    zh_car[:,:] = np.nan
    zv_car = np.empty((zv.shape))
    zv_car[:,:] = np.nan

    # H POLARIZATION
    # Find and store all reflectivity values that fall within the PCT_on > 0.5 grid gate
    for i in range(0,len(PCT_on_50[:,0])):
        for j in range(0,len(PCT_on_50[0,:])):
            if np.isfinite(PCT_on_50[i,j]):
                zh_car[i,j*10-10:j*10] = zh[i,j*10-10:j*10]
                
    # Calculate the PDF of the clutter area reflectivity (CAR)
    mask = np.where(np.isfinite(zh_car))  
    #n,bins,patches=plt.hist(zh_car[mask],bins=525,range=(-40.,65.))
    n,bins=np.histogram(zh_car[mask],bins=525,range=(-40.,65.))
    
    # Calculate CDF of clutter area reflectivity
    cdf = np.cumsum(n)
    p = cdf/cdf[-1]*100
    
    # Find coefficients of 13th degree polynomial for CDF
    x = np.arange(525)*(1/5)-40
    coeff = np.polyfit(p,x,13)
    poly_func = np.poly1d(coeff)
    #x_poly = np.linspace(p[0],p[-1],105)
    #y_poly = poly_func(x_poly)
    
    # Find the value of reflectivity at the 95th percentile of CDF
    dbz95 = poly_func(95.)
    
    # V POLARIZATION
    # Find and store all reflectivity values that fall within the PCT_on > 0.5 grid gate
    for i in range(0,len(vPCT_on_50[:,0])):
        for j in range(0,len(vPCT_on_50[0,:])):
            if np.isfinite(vPCT_on_50[i,j]):
                zv_car[i,j*10-10:j*10] = zv[i,j*10-10:j*10]
                
    # Calculate the PDF of the clutter area reflectivity (CAR)
    mask = np.where(np.isfinite(zv_car))  
    #vn,vbins,vpatches=plt.hist(zv_car[mask],bins=525,range=(-40.,65.))
    vn,vbins=np.histogram(zv_car[mask],bins=525,range=(-40.,65.))
    
    # Calculate CDF of clutter area reflectivity
    cdf = np.cumsum(vn)
    vp = cdf/cdf[-1]*100
    
    # Find coefficients of 13th degree polynomial for CDF
    x = np.arange(525)*(1/5)-40
    coeff = np.polyfit(vp,x,13)
    poly_func = np.poly1d(coeff)
    #x_poly = np.linspace(p[0],p[-1],105)
    #y_poly = poly_func(x_poly)
    
    # Find the value of reflectivity at the 95th percentile of CDF
    dbz95_v = poly_func(95.)
    
    del radar
    return date_time, dbz95, dbz95_v
