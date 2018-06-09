
import os
import glob

from scipy.fftpack import fft
from scipy.io import wavfile
from pathlib import Path

from managers.namingManager import nm_run
from db.db_insert import  insert


def fourier_transform(path):
    fs, data = wavfile.read(glob.glob(path)[1]) # load the data
    
    a = data.T[0] # this is a two channel soundtrack, I get the first track
    
    b=[(ele/2**8.)*2-1 for ele in a] # this is 8-bit track, b is now normalized on [-1,1)
    c = fft(b) # calculate fourier transform (complex numbers list)
    d = int(len(c)/2)  # you only need half of the fft list (real signal symmetry)

    return c, d

def dm_run():

       path = os.path.dirname(os.path.abspath(__file__)) + '\\music\\' + '*.wav'


       for filename in glob.glob(path):

           c, d = fourier_transform(path) 

           name = os.path.basename(filename) + '.txt'

           file_object = open(name, 'wb+')



           print('uploading started')

           end_data = c[:(d-1)].tostring()
           file_object.write(end_data)

           print('uploading ended')

           file_object.close()



           tittle, author = nm_run(name)
           insert(tittle, author)

           
           #plt.plot(a)
           #plt.show()
           #plt.plot(abs(c[:(d-1)]),'r')
           #plt.show()


