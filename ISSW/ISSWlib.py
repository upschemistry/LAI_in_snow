import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import uniform_filter1d


# Functions to help with the analysis
def get_spectrum_list(filename):
    fh = open(filename,'r')
    line0_list = []
    while True:
        line0=fh.readline().replace("\n", "")
        if len(line0) == 0:
            break
#         line0_list.append(line0)
        line0_list.append(line0)
    fh.close()
    number = len(line0_list)
    print('From getline0list: In ',filename, ', finding these spectra:')
    for i in range (number):
        print('     ',line0_list[i])
    return (line0_list,number)

def get_spectrum(filename):
    data = np.loadtxt(filename,skiprows=17,comments='>')
    lambda_nm = data[:,0]
    lambda_cm = lambda_nm/1e7
    nubar_cm = 1/lambda_cm
    I = data[:,1]
    return lambda_nm, I

# def getAngstromExponent(I,I0,lambda_nm,title,
#                         I_1 = 100, I_2 = 250,
#                         smoothsize=60,I_skootch=0.001,plotting=True,verbose=False,alpha=.5,Dark_correction=True):


#     # Smoothing and getting AE
#     I_smooth = uniform_filter1d(I,size=smoothsize)
#     I0_smooth = uniform_filter1d(I0,size=smoothsize)

#     # Correcting mismatches with the blank
#     if Dark_correction:
#         I_smooth *= I0_smooth[-1]/I_smooth[-1]

#     # Shifting the intensities
#     I_smooth = I_smooth-np.min(I_smooth) + I_skootch
#     I0_smooth = I0_smooth-np.min(I0_smooth) + I_skootch
#     tau = np.log(I0_smooth/I_smooth)
#     tau_ratio = tau[I_1]/tau[I_2]
#     lambda_ratio = lambda_nm[I_1]/lambda_nm[I_2]
#     AAE = -np.log(tau_ratio) / np.log(lambda_ratio)
#     if verbose: print('Angstrom exponent = ', AAE)
#     if verbose: print('Minimum of I0_smooth = ', np.min(I0_smooth))

#     if plotting:
#         plt.figure()
#         plt.plot(lambda_nm,I0,'k',alpha=alpha,label='I0')
#         plt.plot(lambda_nm,I,'blue',alpha=alpha,label='I')
#         plt.ylabel('Intensity')
#         plt.xlabel('Wavelenth (nm)')
#         plt.title(title+' before smoothing & baseline subtraction')
#         plt.legend()
#         plt.grid(True)

#         plt.figure()
#         plt.plot(lambda_nm[I_1],I_smooth[I_1],'ko')
#         plt.plot(lambda_nm[I_2],I_smooth[I_2],'ko')
#         plt.plot(lambda_nm,I0_smooth,'k',label='I0 (blank)')
#         plt.plot(lambda_nm,I_smooth,'blue',label='I')
#         plt.ylabel('Intensity')
#         plt.xlabel('Wavelenth (nm)')
#         plt.title(title)
#         plt.legend()
#         plt.grid(True)

#         plt.figure()
#         plt.plot(lambda_nm[I_1],tau[I_1],'ko')
#         plt.plot(lambda_nm[I_2],tau[I_2],'ko')
#         plt.plot(lambda_nm,tau)
#         plt.xlabel('wavelength (nm)')
#         plt.ylabel('optical depth, tau')
#         plt.xlim([350,800])
#         plt.ylim([0,tau[I_1]*1.5])
#         plt.title(title)
#         plt.grid(True)

#         plt.figure()
#         plt.loglog(lambda_nm[I_1],tau[I_1],'ko')
#         plt.loglog(lambda_nm[I_2],tau[I_2],'ko')
#         plt.loglog(lambda_nm,tau)
#         plt.xlabel('wavelength (nm)')
#         plt.ylabel('optical depth, tau')
#         plt.xlim([350,800])
#         plt.ylim([0.4,tau[I_1]*1.9])
#         plt.title(title)
#         plt.grid(True)

#     return AAE, I_smooth, tau

# def getAngstromExponent(I,I0,lambda_nm,title,
#                         I_1 = 100, I_2 = 250,
#                         smoothsize=60,I_skootch=0.001,plotting=True,verbose=False,alpha=.5,Dark_correction=True,R1R2=0.353):


#     # Smoothing
#     I_smooth = uniform_filter1d(I,size=smoothsize)
#     I0_smooth = uniform_filter1d(I0,size=smoothsize)

#     # Correcting mismatches with the blank
#     if Dark_correction:
#         I_smooth *= I0_smooth[-1]/I_smooth[-1]

#     # Shifting the intensities
#     I_smooth = I_smooth-np.min(I_smooth) + I_skootch
#     I0_smooth = I0_smooth-np.min(I0_smooth) + I_skootch
    
    
#     chi = getchi(I,I0,lambda_nm,title,
#                         I_1 = 100, I_2 = 250,
#                         smoothsize=60,I_skootch=0.001,plotting=True,verbose=False,alpha=.5,Dark_correction=True)
    
#     tau = np.log(I0_smooth/I_smooth)
#     tau_ratio = tau[I_1]/tau[I_2]
#     lambda_ratio = lambda_nm[I_1]/lambda_nm[I_2]
#     AAE = -np.log(tau_ratio) / np.log(lambda_ratio)
#     if verbose: print('Angstrom exponent = ', AAE)
#     if verbose: print('Minimum of I0_smooth = ', np.min(I0_smooth))

#     return AAE, I_smooth

def smooth_and_shift(I,I0,smoothsize=60,I_skootch=0.001,plotting=True,verbose=False,Dark_correction=True):

    # Smoothing
    I_smooth = uniform_filter1d(I,size=smoothsize)
    I0_smooth = uniform_filter1d(I0,size=smoothsize)

    # Correcting mismatches with the blank
    if Dark_correction:
        I_smooth *= I0_smooth[-1]/I_smooth[-1]

    # Shifting the intensities
    I_smooth = I_smooth-np.min(I_smooth) + I_skootch
    I0_smooth = I0_smooth-np.min(I0_smooth) + I_skootch
    
    # Done
    return I_smooth, I0_smooth

# def invert_chi_theory(chi,niter_max=10,tolerance=0.01,R1R2=0.5):
#     tau = chi/2
#     bot = 1 - R1R2
#     for iter in range(niter_max):
#         print(iter,tau)
#         tau_last = tau
#         top = 1 - R1R2*np.exp(-4*tau_last)
#         tau = (chi - np.log(top/bot))/2
#         error = (tau-tau_last)/tau
#         if np.abs(error) < tolerance:
#             break
#     print('Quitting after iter = ', iter, ' w/error = ',error)
#     if iter == niter_max-1:
#         flag = False
#     else:
#         flag = True
#     return tau, flag

def invert_chi_theory_numerical(chilist,R1R2,ntau_test=5000):
    taulist = np.empty(0)
    if np.size(chilist) == 1:
        chilist = [chilist]
    tau_test = np.linspace(0,5,ntau_test)
    chi_test = np.zeros(ntau_test)
    
    for chi in chilist:
        for itau in range(ntau_test):
            tau = tau_test[itau]
            chi_test[itau] = get_chi_theory(tau,R1R2)
        error = (chi_test-chi)**2
        ibest = np.argmin(error)
        thistau = tau_test[ibest]
        taulist = np.append(taulist,thistau)
    return taulist

def invert_chi_theory(chilist,R1R2):
    taulist = np.empty(0)
    if np.size(chilist) == 1:
        chilist = [chilist]
    for chi in chilist:
        top = (1-R1R2)*np.exp(chi)+np.sqrt((1-R1R2)**2*np.exp(2*chi)+4*R1R2)
        thistau = 1/2*np.log(top/2)        
        taulist = np.append(taulist,thistau)
    return taulist

def get_f_fp_fpp(chilist,R1R2):
    # This is the same as invert_chi_theory, but includes derivatives
    from numpy import exp
    from numpy import sqrt
    flist = np.empty(0)
    fplist = np.empty(0)
    fpplist = np.empty(0)
    if np.size(chilist) == 1:
        chilist = [chilist]
    for chi in chilist:
        top = (1-R1R2)*np.exp(chi)+np.sqrt((1-R1R2)**2*np.exp(2*chi)+4*R1R2)
        f = 1/2*np.log(top/2)        
        flist = np.append(flist,f)

        fp =  0.5*(-exp(chi)/2 + ((2*R1R2 - 2)*exp(2*chi)/2 + 2)/(2*sqrt(4*R1R2 + \
              (1 - R1R2)**2*exp(2*chi))))/((1 - R1R2)*exp(chi)/2 + sqrt(4*R1R2 + (1 - R1R2)**2*exp(2*chi))/2) 
        fplist = np.append(fplist,fp)

        fpp =  -0.5*((exp(chi) - ((R1R2 - 1)*exp(2*chi) + 2)/sqrt(4*R1R2 + (R1R2 - 1)**2*exp(2*chi)))**2/((R1R2 - 1)*exp(chi) \
               - sqrt(4*R1R2 + (R1R2 - 1)**2*exp(2*chi))) + (exp(2*chi) - ((R1R2 - 1)*exp(2*chi) \
               + 2)**2/(4*R1R2 + (R1R2 - 1)**2*exp(2*chi)))/sqrt(4*R1R2 + (R1R2 - 1)**2*exp(2*chi)))/((R1R2 - 1)*exp(chi) \
               - sqrt(4*R1R2 + (R1R2 - 1)**2*exp(2*chi))) 
        fpplist = np.append(fpplist,fpp)

    f_arrays = [flist, fplist, fpplist]
    return f_arrays

def get_P_Pp_Ppp(kappa,tau_range,f,fp,fpp):
    # Get penalty function values and derivatives
    P = np.sum( (tau_range-kappa*f)**2 )
    Pp = -2*kappa*np.sum( (tau_range-kappa*f)*fp)
    Ppp = -2*kappa*np.sum(-kappa*fp**2 + (tau_range-kappa*f)*fpp)
    P_arrays = [P, Pp, Ppp]
    return P_arrays

def get_R1R1_and_kappa(chi_range,tau_range,R1R2_test, niter=6, verbose=False):
    for i in range(niter):
    
        # Reporting
        if verbose: print('\nFor iteration ', i)
        
        # Get f, fp, and fpp values for different values of R1R2
        f_arrays = get_f_fp_fpp(chi_range,R1R2_test)
        f_retrieved = f_arrays[-3]
        fp_retrieved = f_arrays[-2]
        fpp_retrieved = f_arrays[-1]
        
        # Get kappa values
        kappa_retrieved = np.median(tau_range/f_retrieved)
        if verbose: print('kappa_retrieved = ', kappa_retrieved)
        
        # Get P arrays
        P_arrays = get_P_Pp_Ppp(kappa_retrieved,tau_range,f_retrieved,fp_retrieved,fpp_retrieved)
        Pp = P_arrays[-2]
        Ppp = P_arrays[-1]
    
        # Predict corrections in R1R2
        delta_R1R2_predicted = -Pp/Ppp
        if verbose: print('Predicted delta_R1R2 = ', delta_R1R2_predicted)
        R1R2_test -= delta_R1R2_predicted
        
    return kappa_retrieved, R1R2_test

def get_chi_theory(tau,R1R2):
    return 2*tau+np.log((1-R1R2*np.exp(-4*tau))/(1-R1R2))

def get_chi_obs(I, I0, lambda_nm, plotting=True, title='chi', I_1 = 100, I_2 = 250, alpha=.5):
    
    # Calculate chi
    chi = np.log(I0/I)
    
    # Plot
    if plotting:
        plt.figure()
        plt.plot(lambda_nm,I0,'k',alpha=alpha,label='I0')
        plt.plot(lambda_nm,I,'blue',alpha=alpha,label='I')
        plt.ylabel('Intensity')
        plt.xlabel('Wavelenth (nm)')
        plt.title(title)
        plt.legend()
        plt.grid(True)

        plt.figure()
        plt.plot(lambda_nm[I_1],chi[I_1],'ko')
        plt.plot(lambda_nm[I_2],chi[I_2],'ko')
        plt.plot(lambda_nm,chi)
        plt.xlabel('wavelength (nm)')
        plt.ylabel('chi')
        plt.xlim([350,800])
        plt.ylim([0,chi[I_1]*1.5])
        plt.title(title)
        plt.grid(True)
    
    # Done
    return chi

def get_best_R1R2(L_range_raw, LRF, R1R2_range, beta1, beta2, chi_observed, spectrum_list):
    # Looking for optimal R1R2 values

    # Scale the loading
    L_range = L_range_raw*LRF
    
    # This is how many loadings we are using in the reference set
    number_of_loadings = len(L_range)
    
    # Assuming two wavelengths (450 and 600)
    chi_theory = np.zeros((number_of_loadings,2))
    error1_range = np.zeros(np.shape(R1R2_range))
    error2_range = np.zeros(np.shape(R1R2_range))
    for iR1R2 in range(len(R1R2_range)):

        R1R2 = R1R2_range[iR1R2]
        for i in range(number_of_loadings):
            L = L_range[i]
            tau1 = L*beta1/100 # Dividing by 100 makes it dimensionless
            tau2 = L*beta2/100
            chi_theory[i,0] = get_chi_theory(tau1,R1R2)
            chi_theory[i,1] = get_chi_theory(tau2,R1R2)

        error1_range[iR1R2] = np.sum((chi_observed[:,0]-chi_theory[:,0])**2)
        error2_range[iR1R2] = np.sum((chi_observed[:,1]-chi_theory[:,1])**2)
        
    imin1 = np.argmin(error1_range); R1R2_1 = R1R2_range[imin1]; R1R2_1_error = error1_range[imin1]
    imin2 = np.argmin(error2_range); R1R2_2 = R1R2_range[imin2]; R1R2_2_error = error2_range[imin2]
    

    # Let's see how we did
    plt.figure()
    plt.plot(R1R2_range,error1_range,marker='o',label='450 nm')
    plt.plot(R1R2_range,error2_range,marker='o',label='600 nm')
    plt.grid(True)
    plt.xlabel('R1R2')
    plt.title('LRF='+str(LRF)+' ('+str(imin1)+' & '+str(imin2)+' out of '+str(len(R1R2_range))+')')
    plt.legend()
       
    return R1R2_1, R1R2_2, R1R2_1_error, R1R2_2_error
