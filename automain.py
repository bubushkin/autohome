'''
Created on Nov 25, 2018

@author: iskandar
'''

from homeauto import initialize, init_devices;
from homeauto import db;
from homeauto.engine import Visual


thread_pool = [];

app = initialize('development');
init_devices(app);

pir = None;
for idx in app.gpio:
    if(app.camera.device_couple == idx.device_id):
        pir = idx;
        break;

visual = Visual("thread-camera",  app.camera.device_id, app.camera, pir);
thread_pool.append(visual);

visual.start();


if __name__ == '__main__':
    app.run(use_reloader=False, host="0.0.0.0", port=8080, debug=True);