'''
Created on Nov 26, 2018

@author: iaskarov
'''

#import RPi.GPIO as GPIO;

class GPIODevice(object):

    def __init__(self, params, gpio):
        self.device_id = int(params.get('device_id'));
        self.device_name = params.get('device_name');
        self.device_couple = params.get('device_couple');
        self.gpio = gpio;
        self.status = 0x0;
        self.io = params.get('device_io');
        self.gpio.setup(self.device_id, self.io);
        self.registration_date = params.get('registration_timestamp');

    def release(self):
        self.gpio.cleanup();

    @property
    def gpio(self):
        return self._gpio;

    @gpio.setter
    def gpio(self, val):
        self._gpio = val;
        
    @property
    def io(self):
        return self._io;

    @io.setter
    def io(self, val):
        if(val):
            self._io = self.gpio.IN;
        else:
            self._io = self.gpio.OUT;

    @property
    def device_id(self):
        return self._device_id;

    @device_id.setter
    def device_id(self, val):
        self._device_id = val;
        
    @property
    def device_name(self):
        return self._device_name;

    @device_name.setter
    def device_name(self, val):
        self._device_name = val;

    @property
    def status(self):
        return self._status;

    @status.setter
    def status(self, val):
        self._status = val; 
        
    @property
    def registration_date(self):
        return self._registration_date;

    @registration_date.setter
    def registration_date(self, val):
        self._registration_date = val;
        
    def input(self):
        return self.gpio.input(self.device_id);
    
    def signal(self, high=True):
        if(high):
            self.gpio.output(self.device_id, 0x1);
            self.status = 0x1;
        else:
            self.gpio.output(self.device_id, 0x0);
            self.status = 0x0;