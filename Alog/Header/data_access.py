from Alog.Header.preprocessing import build_feature
from Alog.Header.transform import fft, autocorr, normalize

import numpy as np
from scipy.signal import welch


from Alog.Header.transform import *

class DataAccess():
    
    def __init__(self, mask_file: str, mask_num: int = 15, wnd: int = 1024, fs: int = 3025):
        # Parameter:
        # mask_file: It is a npy file. Its function is filtering the important frequency
        # mask_num: It is an integer. It will the size of the bandwith
        # wnd: window size
        # fs: sample rate
        
        # Function:
        # The constructor just initialize some parameter. It don't do other things.
        
        self.display_num = 2 * wnd
        self.mask = np.load(mask_file)
        self.mask_num = mask_num
        self.wnd = wnd
        self.fs = fs 
        
    def read_file(self, file_name: str):
        # Parameter:
        # file_name: the name of the file
        
        # Function: read the data from the file
        
        time_arr = self.read(file_name)
        self.set_val(time_arr)
        
    def deal(self, arr):
        # Parameter:
        # arr: It must be a list or a numpy.ndarray
        
        # Function: read the data from the vector that you give
        
        arr = np.asarray(arr)
        time_arr = self.segment(arr)
        self.set_val(time_arr)
        
    def read(self, file_name):
        data = np.load(file_name)
        time_arr = []
        if len(data.shape) == 1:
            # If the data is 1-d array
            data = data[np.newaxis, :]
            
        row, col = data.shape
        for i in range(row):
            for j in range(self.wnd, col, self.wnd):
                #time_norm = normalize(data[i][j: j + wnd])
                time_arr.append(data[i][j: j + self.wnd])
        
        time_arr = np.array(time_arr)
        
        if (row * col) < 2 * self.wnd:
            raise ValueError('The size of the input array is too small! It must be bigger than {}.'.format(2 * self.wnd))
        
        return time_arr
    
    def preprocessing(self, X):
        
        if len(X.shape) == 1:
            # If the data is 1-d array
            X = X[np.newaxis, :]
            
        row, col = X.shape
        freq_filter = np.zeros((row, 15))
        new_features = np.zeros((row, 10))
        for i in range(row):
            time_norm = normalize(X[i])
            freq = fft(time_norm, envelope = False)
            new_features[i] = build_feature(time_norm, freq)
            freq_filter[i] = freq[self.mask[:self.mask_num]]
        
        
        all_features = np.concatenate([freq_filter, new_features], axis = 1)
        
        return all_features
    
    def segment(self, arr):
        arr = np.asarray(arr)
        size = len(arr)
        if size > self.wnd:
            time_arr = []
            for i in range(self.wnd, size, self.wnd):
                time_arr.append(arr[i: i + self.wnd])
        elif size == self.wnd:
            time_arr = arr
        else:
            raise ValueError('The size of the input array is larger than window size, please check!')
        
        time_arr = np.array(time_arr)
        
        row, col = time_arr.shape
        if (row * col) < 2 * self.wnd:
            raise ValueError('The size of the input array is too small ! It must be bigger than {}.'.format(2 * self.wnd))
        
        return time_arr
    
    def produce_ploty_data(self, arr):
        x_freq = np.linspace(0, self.fs // 2, self.display_num//2)[2: ]
        y_freq = fft(arr, envelope = False)[2: ]
        
        x_psd, y_psd = welch(arr, fs = self.fs)
        
        y_auto = autocorr(normalize(arr))
        x_auto = np.arange(y_auto.shape[0])
        return x_freq, y_freq, x_psd, y_psd, x_auto, y_auto
    
    def set_val(self, time_arr):
        self.X = self.preprocessing(time_arr)
        
        num = self.display_num // self.wnd
        self.x_time = np.array([i * (1 / self.fs) for i in range(self.display_num)]) 
        self.y_time = np.concatenate([time_arr[i] for i in range(num)])
        self.x_freq, self.y_freq, self.x_psd,\
        self.y_psd, self.x_atc, self.y_atc = self.produce_ploty_data(self.y_time)
    
    def get_data_for_classifier(self):
        return self.X
    
    def get_data_for_ploty(self):
        return self.x_time, self.y_time, self.x_freq, self.y_freq, self.x_psd, self.y_psd, self.x_atc, self.y_atc
