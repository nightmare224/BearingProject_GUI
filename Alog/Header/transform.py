import numpy as np
import pandas as pd
from scipy.signal import hilbert, welch
import matplotlib.pyplot as plt

def getEnvelope (data):
    env = np.abs(hilbert(data))
    return env

def normalize(data):
    a = data.copy()
    a = (a - np.mean(a)) / np.std(a)
    return a

def fft(arr, envelope = True):
    # --------------------------
    # | Parameter:
    # | arr: Please input an 1darray, list, or series.
    # | envelope: time -> hilbert -> fft
    # --------------------------
    
    # --------------------------
    # | Return:
    # | out: freq spectrum
    # --------------------------
    
    arr = np.asarray(arr, dtype = 'float64')
    
    if envelope:
            arr = getEnvelope(arr)

    # 左右對稱 -> 取一半的資料
    FFT = np.fft.fft(arr, norm='ortho')[:len(arr)//2]
    
    # get magnitude
    FFT = np.abs(FFT)
    
    return FFT

def get_first_n_peaks(data, n, height = 0):
    if n > data.shape[0]:
        raise ValueError('first_n_peaks > peak_location, please check.')
    if height == 'auto':
        mean = np.mean(data)
        std = np.std(data)
        height = mean + 3 * std
    peaks_location, peaks_val = find_peaks(data, height = height)
    peaks_val = peaks_val['peak_heights']
    exc = 2
    if ((peaks_location.shape[0]) - n) < exc:
        fill = n - peaks_location.shape[0] + exc
        peaks_location = np.array(peaks_location.tolist() + [0 for _ in range(fill)])
        peaks_val = np.array(peaks_val.tolist() + [0 for _ in range(fill)])
        
    return peaks_location[exc: (n + exc)], peaks_val[1: (n + 1)]

def autocorr(x):
    result = np.correlate(x, x, mode='full')
    return result[len(result)//2:]
 
def get_autocorr_values(y_values, N, f_s):
#     y_values = (y_values - np.mean(y_values)) / np.std(y_values)
    autocorr_values = autocorr(y_values)
#     autocorr_values += np.abs(autocorr_values)
    return autocorr_values

def get_atc_corr_intercept(y):
    r = np.corrcoef(y)
    i = np.max(y)
    return r, i
