#!/usr/bin/env python
# coding: utf-8

# Revisions made summer 2020 by S. Neshyba

import numpy as np

# This is the exponential-with-time function
def test_func(t, A, t0): #first varible is the independent varible, then the subsequent are the ...
    return A*(1-np.exp(-t/t0))

def test_func2(t, A1, t01, A2, t02): #first varible is the independent varible, then the subsequent are the ...
    return A1*(1-np.exp(-t/t01)) + A2*(1-np.exp(-t/t02)) 

class LAHM_Parameters:
    def __init__(self, inst_number = 10):
        
        self.inst_number = inst_number
        self.exponential_prefactor = 3.43
        self.temperature_factor = 0.238
        self.ugbasic_offset = 3.0

        if inst_number == 10: self.inst_factor = 0.77
        elif inst_number == 14: self.inst_factor = 0.77
        elif inst_number == 15: self.inst_factor = 0.74
        elif inst_number == 20: self.inst_factor = 0.74
        else:
            self.inst_number = inst_number
            self.inst_factor = np.nan
            self.exponential_prefactor = np.nan
            self.temperature_factor = np.nan
            self.ugbasic_offset = np.nan
            print("Unknown instrument number", inst_number)

    def report(self):
        print("Parameters:")
        print("LAHM unit =", self.inst_number)
        print("inst_factor =", self.inst_factor)
        print("exponential_prefactor =", self.exponential_prefactor)
        print("temperature_factor =", self.temperature_factor)
        print("ugbasic_offset =", self.ugbasic_offset)

class Ttrace:
    def __init__(self, filename, volume, ngperg, ugbasic, t_av_out, T2_out):
        self.filename = filename
        self.volume = volume
        self.ngperg = ngperg
        self.ugbasic = ugbasic
        self.Temp_av = t_av_out
        self.time = T2_out
    def report(self):
        print(self.filename, self.volume, self.ngperg, self.ugbasic)

def getline0list(filename):
    fh = open(filename,'r')
    print(filename)
    line0_list = []
    while True:
    #for t in range(0,bignumber):
        line0=fh.readline().replace("\n", "")
        if len(line0) == 0:
            break
        line0_list.append(line0); #print(line0_list)
    fh.close() 
    number = len(line0_list)
    return (line0_list,number)

def getgpg(line0_list, myLAHM_Parameters, verbose=False):
    number = len(line0_list); print('From getgpg: number = ', number)
    filelist=[]
    T1 = np.zeros((2760,number))
    T2 = np.zeros((2760,number))
    mugrams = np.zeros(number)
    dT = np.zeros((2760,number))
    flatT = np.zeros((2760,number))
    temp = np.zeros((2760,number))
    on = np.zeros((2760,number))
    cycle = np.zeros((2760,number))
    t_av = np.zeros((480,number))
    vol = np.zeros(number)

    for t in range(0,number):
        print('From getgpg: t = ', t) 
        line0=line0_list[t] #fh.readline(); #print(line0)
        line1=line0.split(); print('From getgpg: ', line1)

        # This is to take into account the possibility that there are spaces in the file name
        nchars_for_vol = len(line1[-1])

        #make a subfolder in the folder ...
        # filename2=line1[0]
        filename2 = line0[0:-nchars_for_vol-1]
        print('From getgpg: filename2 = ', filename2)
        # vol[t]=float(line1[1])
        vol[t]=float(line1[-1])
        print('From getgpg: vol[t] = ', vol[t])
        
        fi = open(filename2)
        filelist.append(filename2)
        for i in range(0,2759):
            line1=fi.readline()
            # print('From getgpg: line1 = ', line1)
            line2=line1.split()
            #if verbose: print('From getgpg: line2 = ', line2)
            T1[i,t]=float(line2[0])
            T2[i,t]=float(line2[1])
            temp[i,t]=float(line2[2])
            on[i,t]=float(line2[3])
            # cycle[i,t]=float(line2[4])
        base2=temp[483:521,t].mean()
        base3=temp[964:1002,t].mean()
        base4=temp[1445:1483,t].mean()
        base5=temp[1926:1964,t].mean()
        base=(base2+base3+base4)/3.
        dT[0:2759,t]=temp[0:2759,t]-base
        flatT[0:2759,t]=temp[0:2759,t]-base5

        for i in range(0,479):
            t_av[i,t]=(dT[i+481,t]+dT[i+962,t]+dT[i+1443,t])/3            
            
    # Extract parameters for this instrument
    inst_factor = myLAHM_Parameters.inst_factor 
    exponential_prefactor = myLAHM_Parameters.exponential_prefactor
    temperature_factor = myLAHM_Parameters.temperature_factor
    ugbasic_offset = myLAHM_Parameters.ugbasic_offset
    
    # Compute the loading
    t_av = t_av*inst_factor
    ugbasic=exponential_prefactor*np.exp(t_av[160]*temperature_factor)-ugbasic_offset
    #vol=vol/1000#liters
    ngperg=ugbasic/vol*1000
    
    # Packaging output arrays to contain only the averages
    T2_out = T2[0:479,:]
    t_av_out = t_av[0:479,:]
    
    # Make the entries in the list of temperature traces
    myTtrace_list = []
    for i in range(0,number):
        myTtrace = Ttrace(filelist[i],vol[i],ngperg[i],ugbasic[i],t_av_out[:,i],T2_out[:,i])
        myTtrace_list.append(myTtrace)
        
    # Get out
    #return(ngperg,ugbasic,t_av_out,T2_out)
    return(myTtrace_list)

