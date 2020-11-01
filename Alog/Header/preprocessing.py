import numpy as np
import pandas as pd
from scipy.stats import skew, kurtosis
from scipy.signal import hilbert, welch, savgol_filter

from Alog.Header.transform import *

# Global var for ploty
freq_auto, autocorr, freq_psd, psd = 0, 0, 0, 0

def build_feature(time_arr, freq_arr):
    N = time_arr.shape[0]

    # build time domain feature
    Mean = np.mean(time_arr)
    Std = np.std(time_arr)
    Peak = 0.5 * (np.max(time_arr) - np.min(time_arr))
    RMS = np.sqrt(np.sum([ i ** 2 for i in time_arr]))
    Kurtosis = kurtosis(time_arr)
    Skew = skew(time_arr)
    Crest = Peak / RMS

    tmp = np.array([np.sqrt(np.abs(i)) for i in time_arr])
    Clearance = Peak / ((1 / N) * np.sum(tmp)) ** 2
    Allowance = Peak / np.mean(tmp) ** 2

    tmp = ((1 / N) * np.sum([np.abs(i) for i in time_arr]))
    Impulse = Peak / tmp
    Shape = RMS / tmp

    # build freq domain feature
    N = freq_arr.shape[0]
    st = 1e-2
    fs = 1 / st
    y = 2 * freq_arr / N
    f = np.array([(i + 1.) * fs / N for i in range(N)])
    F_Mean = np.mean(y)
    F_Std = np.std(y)
    FC = np.dot(f, y) / np.sum(y)
    MSF = np.dot(np.multiply(f, f), y) / np.sum(y)
    RMSF = np.sqrt(MSF)
    VF = np.dot(np.multiply(f - FC, f - FC),y)/ np.sum(y)
    RVF = np.sqrt(VF)

    return [Mean, Std, Peak, RMS, Skew,
            F_Mean, F_Std, FC, RMSF, RVF]

def outlier_detect_Isolation_Forest(data, percentage = 0.1):
    IF = IsolationForest(n_estimators=200, max_samples='auto', contamination=percentage, max_features=1.0, bootstrap=True, n_jobs=None, random_state=12, verbose=0, warm_start=False)
    IF.fit(data)
    outlier = IF.predict(data)
    mask = np.where(outlier == 1)[0]

    return mask

def read_file(file_name, wnd = 256, n = None):
    data = np.load(file_name)
    row, col = data.shape

    if n == None:
        pass
    elif n > row:
        raise ValueError("The number of data is too low to read. Please check data num")
    else:
        row = n
    
    time_arr = []
    for i in range(row):
        for j in range(wnd, col, wnd):
            time_arr.append(data[i][j: j + wnd])

    time_arr = np.array(time_arr)

    return time_arr

def read_train_file(file_lst, name_lst, n = 10, wnd = 256):
    # | file_lst: [檔名1, 檔名2, ...]
    # | name_lst: key 的名字
    # | n: 每個類別有幾筆 4096 的資料
    # | wnd: window size
    # | outlier_detect_mode: 0 -> no outlier detection, 1 -> moving average, 2 -> Isolation Forest, 3 -> both
    # | the parameter for moving average
    # | lower: 
    # | upper:
    # | the parameter for Isolation Forest


    data = dict()
    for i, name in enumerate(file_lst):
        # 取得資料
        data[name_lst[i]] = np.load(name)
    
    mag_arr = []
    time_arr = []
    label = []
    
    for i,  name in enumerate(name_lst):
        for j in range(n):
            for k in range(wnd, data[name].shape[1], wnd):
                time = data[name][j][k: k + wnd]
                time_arr.append(time)
                label.append(i)
            
                
    time_arr = np.array(time_arr)
    label = np.array(label)
    
    return time_arr, label

def preprocessing(
    X, fs = 2048, normalize = True, smooth = False, preprocessing_mode = 'fft',
    envelope = False, first_n_peaks = 10, height = 0, mask = True,
    mask_num = 15
):
    # --------------------------
    # | X: time domain data
    # | Y: the label of the data
    # |
    # | preprocessing_mode: 
    # |     It is a list. Ex. preprocessing_mode = ['fft', 'construct']
    # |     1. time (no preprocessing)
    # |     2. construct (14 features), (construct some features by time domain and freq domain)
    # |     3. fft (mask_num features), (Fourier Transform),
    # |     4. psd (first_n_peaks features), (Power Spectral Density)
    # |     5. autocorrelation (first_n_peaks features)
    # |
    # | envelope: time -> hilbert -> fft
    # |
    # | outlier_mode:
    # |     1. 0: no outlier detection
    # |     2. 1: Isolaiton Forest
    # |
    # | percentage: 
    # |     How many oulier do you want to remove?
    # |     It is a number between [0, 1], default is 0.1.
    # --------------------------
    
    data = dict()
    preprocessing_mode = [mode.lower() for mode in preprocessing_mode]
    time_arr = X.copy()
    
    row, col = X.shape
    
    if normalize:
        if len(time_arr.shape) == 1:
            time_arr = (time_arr - np.mean(time_arr)) / np.std(time_arr)
        else:
            for i in range(row):
                time_arr[i] = (time_arr[i] - np.mean(time_arr[i])) / np.std(time_arr[i])
    
    if smooth:
        for i in range(row):
            time_arr[i] = savgol_filter(time_arr[i], window_length = 5, polyorder = 3)
    
    new_features = np.zeros((row, 10))
    
    
    flag = 0
    if 'time' in preprocessing_mode:
        return X
    if 'fft' in preprocessing_mode:
        freq_spectrum = np.zeros((row, col // 2))
        
        for i in range(row):
            freq_spectrum[i] = fft(time_arr[i], envelope = envelope)
            new_features[i] = build_feature(time_arr[i], freq_spectrum[i])
        if mask:
            mask = np.load('./feature_importance_mask/mask_wnd_1024.npy')
            freq_spectrum = freq_spectrum[:, mask[:mask_num]]
            
        data['fft'] = freq_spectrum
        flag += 1
    if 'construct' in preprocessing_mode:
        if 'fft' not in preprocessing_mode:
            for i in range(row):
                freq = fft(time_arr[i], envelope = envelope)
                new_features[i] = build_feature(time_arr[i], freq)
        
        flag += 1
        data['construct'] = new_features
        flag += 1
    if 'psd' in preprocessing_mode:
        psd_peak = np.zeros((row, first_n_peaks))
        for i in range(row):
            freq_psd, psd = welch(time_arr[i], fs = 2048)
            psd_peak[i], _ = get_first_n_peaks(psd, first_n_peaks, height)
            
        data['psd'] = psd_peak
        flag += 1
    if 'autocorrelation' in preprocessing_mode:
        # auto_peak = np.zeros((row, first_n_peaks))
        auto_peak = np.zeros((row, 2))
        for i in range(row):
            autocorr = get_autocorr_values(time_arr[i], N = col, f_s = fs)
#             auto_peak[i], _ = get_first_n_peaks(autocorr, first_n_peaks, height)
            auto_peak[i] = get_atc_corr_intercept(autocorr)
            
        data['autocorrelation'] = auto_peak
        flag += 1
    if flag == 0:
        raise ValueError("I don't know what you mean ?")
        
    all_features = np.concatenate([data[mode] for mode in preprocessing_mode], axis = 1)

    return all_features

def outlier_detection(X, Y, outlier_mode = 0, percentage = 0.1):
    if outlier_mode == 1:
        mask = outlier_detect_Isolation_Forest(X, percentage = percentage)
        X_inlier = X[mask]
        Y_inlier = Y[mask]
    return X_inlier, Y_inlier

def train_test_split_by_time(x, y, test_size):
    class_num = np.unique(y).shape[0]
    
    x_train = []
    x_test = []
    y_train = []
    y_test = []
    
    for i in range(class_num):
        mask = np.where(y == i)[0]
        train_size = int(mask.shape[0] * (1 - test_size))
#         print('HiHi', train_size)
#         print(mask[:10])
        
        for j in mask[: train_size]:
            x_train.append(x[j])
            y_train.append(y[j])
        
        for j in mask[train_size: ]:
            x_test.append(x[j])
            y_test.append(y[j])
        
    x_train, y_train = shuffle(np.array(x_train), np.array(y_train))
    x_test, y_test = shuffle(np.array(x_test), np.array(y_test))

    return x_train, x_test, y_train, y_test
