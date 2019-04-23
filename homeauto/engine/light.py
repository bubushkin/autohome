'''
Created on Dec 2, 2018

@author: iskandar
'''

import threading;
import time;
from homeauto.udef import send_sms;
from homeauto.udef import send_email;

class Light(threading.Thread):
    
    def __init__(self, thname, thid, light, pir):
        threading.Thread.__init__(self);
        self.thread_name = thname;
        self.thread_id = thid;
        self.light = light;
        self.pir = pir;
        
    def run(self):
        while(True):
            if(self.pir.input()):
                print("Motion detected");
                self.light.signal(True);                
