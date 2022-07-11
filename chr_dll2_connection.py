# -*- coding: utf-8 -*-
"""

Example programm for communication with a CHR device
Copyright Precitec Optronik GmbH, 2022

"""
from ctypes import *

#Connection to CHR device
import time
import numpy as np

class CHR_connection():
    
    '''
    The present class CHR_connection is intended to provide a python interface for the .dll-based connection
    to CHR and CHR2 devices. Note, that .dll in the current version supports connections of the second generation devices only over 
    only over TCP/IP protocol. Soon, the support for CHR RS-422 protocol should be implemented.

    Args:
        address_str (str): The arg is the IP Adress of CHR 
        device_type (int): the exact type of the device
        

    Attributes:
        dll: type of the dll
        chr_lib: path to the .dll Here, it is assumed that the .dll is in the same path as the current script
        pHandle: 
        pSpectrumLength:
        pnNumberOfSignals:
        pSpectrumBuffer:
        ppData:
        
    '''
    
    
    def __init__(self,address_str,device_type):
        """
        Initialize all necessary attributes and establish the connection to the CHR device.

        Parameters
        ----------
        address_str : IP Adress of the device in the form: 'IP: 192.168.170.2'
            citation from api reference(07.06.2021):
            For ethernet connection the string looks
            like 192.168.170.2, Port: 7891. If port number is not specified, the default value 7891
            will be taken.
            The connection information string for serial connection looks like COM15, Baud: 921600,
            Handshake: On.
            
        device_type : the exact type of the device for details look into api reference of the .dll
                CHR_Unspecified = -1;
                CHR_1_Device = 0;
                CHR_2_Device = 1;
                CHR_Multi_Channel_Device = 2;
                CHR_Compact_Device = 3;
            

        Returns
        -------
        None.

        """
        self.dll = CDLL('msvcrt')
        self.dll.malloc.restype = c_void_p
        self.chr_lib = CDLL('.\CHRocodileDll.dll')
        self.pHandle = c_int()
        self.pSpectrumLength = c_int()
        self.pnNumberOfSignals = c_int()
        self.pSpectrumBuffer = pointer(c_short())
        self.ppData = pointer(c_double())
        address_str = address_str.encode('utf-8')
        res = self.chr_lib.OpenConnection(address_str,device_type,byref(self.pHandle))
        
        
    def set_autobuffer_size(self,n_sample):
        """
        Set the size of autobuffer

        Parameters
        ----------
        n_sample : desired length of autobuffer

        Returns
        -------
        None.

        """
        self.n_sample = n_sample
        self.pBuffer = self.dll.malloc(n_sample * sizeof(c_double))
        self.pBuffer = cast(self.pBuffer,POINTER(c_double))
        
    def get_spectrum_multichannel(self,spectrum_type,channel_index):
        """
        Returns the spectrum recorded by the CHR device

        Parameters
        ----------
        spectrum_type : 0 - raw spectrum; 
                        1 - processed spectrum in confocal mode;
                        2 - FFT
        channel_index

        Returns
        -------
        spectrum : TYPE
            DESCRIPTION.

        """
        res = self.chr_lib.DownloadDeviceSpectrumMultiChannel(self.pHandle,c_int(spectrum_type),c_int(channel_index),byref(self.pSpectrumBuffer),byref(self.pSpectrumLength))
        n_spectrum = self.pSpectrumLength.value
        spectrum = self.pSpectrumBuffer[0:n_spectrum]
        return spectrum      
    
    def get_spectrum(self,spectrum_type):
        """
        Returns the spectrum recorded by the CHR device

        Parameters
        ----------
        spectrum_type : 0 - raw spectrum; 
                        1 - processed spectrum in confocal mode;
                        2 - FFT

        Returns
        -------
        spectrum : TYPE
            DESCRIPTION.

        """
        res = self.chr_lib.DownloadDeviceSpectrum(self.pHandle,c_int(spectrum_type),byref(self.pSpectrumBuffer),byref(self.pSpectrumLength))
        n_spectrum = self.pSpectrumLength.value
        spectrum = self.pSpectrumBuffer[0:n_spectrum]
        return spectrum
    
    
    def send_command(self,command_str):
        """
        Sends a command command_str to the device and returns the echo of the device.
        

        Parameters
        ----------
        command_str : TYPE
            DESCRIPTION.

        Returns
        -------
        response_str : TYPE
            DESCRIPTION.

        """
        command_str = c_char_p(command_str.encode('utf-8'))
        response_str = command_str
        res = self.chr_lib.ExecCommand(self.pHandle,command_str,byref(response_str))
        response_str = str(response_str.value)
        return response_str
    
    
    def flush_autobuffer(self):
        """
        Flushes the inputbuffer and returns an echo message of CHR when the command is carried out

        Returns
        -------
        res : TYPE
            DESCRIPTION.

        """
        res = self.chr_lib.FlushInputBuffer(self.pHandle)
        return res
    
    
    def start_autobuffer(self): 
        """
        Starts to save the data to the autobuffer and returns an echo message of CHR when the command is carried out

        Returns
        -------
        res : TYPE
            DESCRIPTION.

        """
        res = self.chr_lib.SetToAutoBufferSave(self.pHandle,self.pBuffer,self.n_sample)
        return res
    
    
    def read_autobuffer(self):
        """
        Reads the autobuffer of CHR and returns an echo message of CHR when the command is carried out        
        
        Returns
        -------
        buffer : TYPE
            DESCRIPTION.

        """
        res = 1
        while res == 1: #wait until buffer is ready
            res = self.chr_lib.IsAutoBufferSave(self.pHandle)
        buffer = self.pBuffer[0:self.n_sample]
        return buffer
    
    
    def get_last_sample(self):
        """
        Returns the last recorded signal data

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        #int GetLastSample(u32 _hConnection, double ** _ppData, int * _pnNumberOfSignals);
        res = self.chr_lib.GetLastSample(self.pHandle,byref(self.ppData),byref(self.pnNumberOfSignals))
        return self.ppData[0:self.pnNumberOfSignals.value]
    
    
    def close_connection(self):
        """
        Closes connection to the CHR device and returns an echo message of CHR when the command is carried out

        Returns
        -------
        None.

        """
        res = self.chr_lib.CloseConnection(self.pHandle)
        del self.pBuffer
        return(res)
    def delete_white_reference(self):
        """
		Deletes current white reference
		Returns
		-------
		None
		"""
        wht_array = 1000*np.ones(1024).astype('uint16')
        data = wht_array.tobytes()
        blob_size = 2048
        blob = create_string_buffer(blob_size)
        for i in range(blob_size):
            blob[i] = data[i]
        
        command_str = '$TABL 11 0 0 2048'
        command_str = c_char_p(command_str.encode('utf-8'))
        response_str = command_str
        res = self.chr_lib.ExecCommandWithBinArg(self.pHandle,command_str,blob,c_int(blob_size),byref(response_str))
        return res
def upload_wav_table(self,filename):
		"""
		Upload wavelength calibration table to device
		Returns
		-------
		None
		"""
		filename = c_char_p(filename.encode('utf-8'))
		res = self.chr_lib.UploadWaveLengthTableFromFile(self.pHandle,filename);
		return res
