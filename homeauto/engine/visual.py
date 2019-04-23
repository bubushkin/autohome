'''
Created on Dec 2, 2018

@author: iskandar
'''

import threading;
import time;
from homeauto.udef import send_sms;
from homeauto.udef import send_email;

class Visual(threading.Thread):
    
    def __init__(self, thname, thid, camera, pir):
        threading.Thread.__init__(self);
        self.thread_name = thname;
        self.thread_id = thid;
        self.camera = camera;
        self.pir = pir;
        
    def run(self):
        while(True):
            if(self.pir.input()):
                print("Motion detected");
                img_path = self.camera.capture();
                send_sms(attach=img_path);
                send_email(to_email="dibadog@gmail.com", attach=img_path);