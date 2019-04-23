'''
Created on Dec 8, 2018

@author: iskandar
'''
import time;
import picamera;

class Camera(object):
    
    def __init__(self, params):
        
        self.device_id = params.get('device_id');
        self.device_name = params.get('device_name');
        self.device_io = params.get('device_io');
        self.device_couple = params.get('device_couple');
        
        self.camera=picamera.PiCamera();
        
        self.dims = {
            'motion': { 'w': 640, 'h': 480 },
            'still': { 'w': 1024, 'h': 768 }
            }

        self.camera.resolution=(self.dims['still']['w'],self.dims['still']['h']);
        time.sleep(0x2);
        
    def capture(self):
        captured_path = '/tmp/picamera/picture/' + str(int(time.time())) + '.jpg';
        self.camera.capture(captured_path);
        return captured_path;
    
    def video(self, duration=0xA):
        captured_path = '/tmp/picamera/video/' + str(int(time.time())) + '.h264';
        self.camera.resolution=(640,480);
        self.camera.start_recording(captured_path);
        self.camera.wait_recording(duration);
        self.camera.stop_recording();
        return captured_path;