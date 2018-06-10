
import os
import glob
import numpy
import math
import csv

import matplotlib.pyplot as plt
import pandas as pd

from scipy.fftpack import fft
from scipy.io import wavfile
from pathlib import Path

from managers.namingManager import nm_run
from db.db_insert import  insert


def fourier_transform(data):
   
    a = data.T[0] # this is a two channel soundtrack, I get the first track
    
    total_size = len(a)
    chunk_size = 4096;

    sampled_chunk_size = int(total_size/chunk_size);
    result = [];
    for j in range(0, sampled_chunk_size):
           complex_array = []; 
           
           for i in range(0, chunk_size):
                complex_array.append(complex(a[(j*chunk_size)+i], 0))
           result.append(fft(complex_array))

    #b=[(ele/2**10.)*2-1 for ele in a] # this is 8-bit track, b is now normalized on [-1,1)
    #c = fft(b) # calculate fourier transform (complex numbers list)
    #d = int(len(c)/2)  # you only need half of the fft list (real signal symmetry)

    return result

def get_index(freq):

    RANGE = [40, 80, 120, 180, 300]

    i = 0
    while ( RANGE[i] < freq ):
        i = i + 1

    return i


def hash(freq):
    FUZ_FACTOR = 2;
    p0 = freq[0]
    p1 = freq[1]
    p2 = freq[2]
    p3 = freq[3]
    return  (p3-(p3%FUZ_FACTOR)) * 100000000 + (p2-(p2%FUZ_FACTOR)) * 100000  + (p1-(p1%FUZ_FACTOR)) * 100 + (p0-(p0%FUZ_FACTOR));


def get_magnetude(result):
    high_scores = []
    freq_score = []
    for t in range(0, len(result)):
        max = [0,0,0,0,0]
        freq_max = [0,0,0,0,0]
        for freq in range(40,300):
            mag = math.log(abs(result[t][freq]) + 1)
    
            index = get_index(freq)
    
            if (mag > max[index]):
                max[index] = mag
                freq_max[index] = freq
    
        high_scores.append(max)
        freq_score.append(hash(freq_max))

    return high_scores, freq_score



def dm_run():

       path = os.path.dirname(os.path.abspath(__file__)) + '\\music\\' + '*.wav'

       #in_file = open("Come A Little Bit Closer  -  Jay  The Americans.wav.txt", "rb") # opening for [r]eading as [b]inary
       #data = in_file.read() # if you only wanted to read 512 bytes, do .read(512)
       #in_file.close()

       end_data = [];

       for filename in glob.glob(path):


           name = os.path.basename(filename).split('.')[0]
           print('Magic with file {0} started'.format(name))

           fs, data = wavfile.read(filename) # load the data

           result = fourier_transform(data) 

           high_scores, freq_score = get_magnetude(result)


           print(name)
           print(len(freq_score))
           print(freq_score)

           #plt.plot( high_scores, freq_score ,'ro')
           #plt.show()

           #plt.plot(freq_score, 'ro')
           #plt.show()


           end_data.append(freq_score)
           end_data.append(name)


       print('uploading started')


       my_df_name = pd.DataFrame(end_data)
       my_df_name.to_csv('data_names.csv', index=False, header=False)
       my_df = pd.DataFrame(end_data)
       my_df.to_csv('data.csv', index=False, header=False)

       print('uploading ended')



       tittle, author = nm_run(name)
       insert(tittle, author)