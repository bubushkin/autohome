'''
Created on Nov 26, 2018

@author: iaskarov
'''

dbquery = {
    
    'GET_USER_COUNT': 'SELECT COUNT(*) as count FROM user WHERE username = %s and passwd=MD5(%s)',
    'GET_DEVICE_BY_NAME': 'SELECT device_id, device_name, device_io, device_couple, device_status, registration_timestamp FROM device WHERE device_name=%s',
    'GET_ACTION_BY_NAME': 'SELECT status_id, status_name FROM device_status WHERE status_name=%s',
    'GET_ALL_DEVICES': '''SELECT d.device_id, 
                                d.device_name, 
                                ds.status_name, 
                                d.registration_timestamp
                            FROM device d
                            INNER JOIN device_status ds 
                                ON ds.status_id = d.device_status''',
    'GET_ALL_STATUS_TYPES': 'SELECT status_id, status_name FROM device_status',
    'GET_ALL_EVENT_TYPES': 'SELECT event_id, event_name FROM device_event',
    'GET_ALL_ACTIVITY': '''SELECT da.activity_id, 
                                    da.device_id, 
                                    d.device_name, 
                                    da.timestamp, 
                                    de.event_id, 
                                    de.event_name 
                            FROM device_activity da
                            INNER JOIN device d ON d.device_id = da.device_id
                            INNER JOIN device_event de ON de.event_id = da.event_type
                            ORDER BY da.timestamp DESC''',
    'GET_ALL_STATUS': '''SELECT d.device_id, 
                            d.device_name, 
                            ds.status_id, 
                            ds.status_name, 
                            d.registration_timestamp,
                            (select max(da.timestamp) from device_activity da where da.device_id = d.device_id) last_activity_timestamp
                        FROM device d
                        INNER JOIN device_status ds 
                            ON ds.status_id = d.device_status
                        ORDER by d.device_name''',
    'REGISTER_DEVICE': '''INSERT INTO device(device_id, device_name, device_io, device_couple) VALUES (%s, %s, %s, %s)''',
    'UPDATE_DEVICE_STATUS': 'UPDATE device SET device_status = %s WHERE device_id = %s',
    'GET_DEVICE_STATUS': 'SELECT device_status FROM device WHERE device_id = %s',
    'REGISTER_ACTIVITY': 'INSERT INTO device_activity(device_id, event_type) values(%s, %s)',
    'GET_DEVICE_BY_ID': 'SELECT device_id, device_name, device_io, device_couple, device_status, registration_timestamp FROM device WHERE device_id=%s',
    'TRUNCATE_ACTIVITY': 'DELETE FROM device_activity',
    'TRUNCATE_DEVICE': 'DELETE FROM device',
                    }