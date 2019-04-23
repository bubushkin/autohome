'''
Created on Nov 26, 2018

@author: iaskarov
'''


from homeauto.const import errno;
from flask import current_app;
import sys;
from types import NoneType;
from flask import session;
import MySQLdb;
import traceback;
from homeauto.const import dbquery;
from homeauto.const import FatalException;
from homeauto.model import GPIODevice;

class DBFactory(object):
    
    _conn = None;

    def __init__(self, config):
            self.__config = config;
            self.__connect();
            
    def close(self):
        self._conn.close();
    
    def __connect(self):
        try:
            
            self._conn = MySQLdb.connect(self.__config["DB_HOST"], 
                                         self.__config["DB_USER"],
                                         self.__config["DB_PASSWD"],
                                         self.__config["DB_NAME"]); 
            check = self._conn.ping(False);
        except MySQLdb.DatabaseError as ex:
            traceback.print_exc();
            sys.exit(errno.EXIT_FAILURE);

    def reset_db(self):

        cursor = None;
        try:
            cursor = self._conn.cursor();
            cursor.execute(dbquery['TRUNCATE_ACTIVITY']);
            self._conn.commit();
            cursor.execute(dbquery['TRUNCATE_DEVICE']);
            self._conn.commit();
        except MySQLdb.DatabaseError as ex:
            traceback.print_exc();
        finally:
            cursor.close();
        
    def validate_user(self, user):

        cursor = None;
        valid = False;

        try:
            cursor = self._conn.cursor(MySQLdb.cursors.DictCursor);
            cursor.execute(dbquery['GET_USER_COUNT'], user.username, user.passwd);
            rset = cursor.fetchone();
            if not (isinstance(rset, NoneType)):
                if(rset.get('count') == 0x1):
                    valid = True;
        except MySQLdb.DatabaseError as ex:
            traceback.print_exc();
        finally:
            cursor.close();
        return valid;
    
    def register_device(self, device):

        cursor = None;
        try:
            cursor = self._conn.cursor();
            cursor.execute(dbquery['REGISTER_DEVICE'], (device.get('device_id'), device.get('device_name'), device.get('device_io'), device.get('device_couple')));
            self._conn.commit();
            self.register_activity(device.get('device_id'), 0x3);            
        except MySQLdb.DatabaseError as ex:
            traceback.print_exc();
        finally:
            cursor.close();

    def get_current_status(self, attempt=0x0):

        cursor = None;
        events = [];
        
        try:
            cursor = self._conn.cursor(MySQLdb.cursors.DictCursor);
            cursor.execute(dbquery['GET_ALL_STATUS']);
            rset = cursor.fetchall();
            if not (isinstance(rset, NoneType)):
                for rdx in rset:
                    events.append(rdx);
        except MySQLdb.OperationalError as opex:
            if(attempt > 0x3):
                raise FatalException('Unrecovable exception caught. Exiting..');
                sys.exit(errno.EXIT_FAILURE);
            else:
                attempt += 0x1;
            self.__connect();
            self.get_all_activity(attempt);
        except MySQLdb.DatabaseError as ex:
            traceback.print_exc();
        finally:
            cursor.close();
        return events;
    
    def get_device_by_name(self, device_name):

        cursor = None;
        device = None;
        try:
            cursor = self._conn.cursor(MySQLdb.cursors.DictCursor);
            cursor.execute(dbquery['GET_DEVICE_BY_NAME'], [device_name]);
            rset = cursor.fetchone();
            if not (isinstance(rset, NoneType)):
                device = rset;
        except MySQLdb.DatabaseError as ex:
            traceback.print_exc();
        finally:
            cursor.close();
        return device;

    def get_device_by_id(self, device_id):

        cursor = None;
        device = None;
        try:
            cursor = self._conn.cursor(MySQLdb.cursors.DictCursor);
            cursor.execute(dbquery['GET_DEVICE_BY_ID'], [device_id]);
            rset = cursor.fetchone();
            if not (isinstance(rset, NoneType)):
                device = rset;
        except MySQLdb.DatabaseError as ex:
            traceback.print_exc();
        finally:
            cursor.close();
        return device;


    def get_action_by_name(self, status_name):

        cursor = None;
        device = None;
        try:
            cursor = self._conn.cursor(MySQLdb.cursors.DictCursor);
            cursor.execute(dbquery['GET_ACTION_BY_NAME'], [status_name]);
            rset = cursor.fetchone();
            if not (isinstance(rset, NoneType)):
                device = rset;
        except MySQLdb.DatabaseError as ex:
            traceback.print_exc();
        finally:
            cursor.close();
        return device;

    def register_activity(self, device_id, action):

        cursor = None;
        try:
            cursor = self._conn.cursor();
            cursor.execute(dbquery['REGISTER_ACTIVITY'], (device_id, action));
            self._conn.commit();
        except MySQLdb.DatabaseError as ex:
            traceback.print_exc();
        finally:
            cursor.close();

    def validate_connection(self):
        if (self._conn.open == 0x0):
            current_app.logger.warning(errno.DB_CONN_ERR);
            self.__connect();

    def get_all_devices(self, attempt=0x0):

        cursor = None;
        events = [];
        
        try:
            cursor = self._conn.cursor(MySQLdb.cursors.DictCursor);
            cursor.execute(dbquery['GET_ALL_DEVICES']);
            rset = cursor.fetchall();2 
            if not (isinstance(rset, NoneType)):
                for rdx in rset:
                    events.append(rdx);
        except MySQLdb.OperationalError as opex:
            if(attempt > 0x3):
                raise FatalException('Unrecovable exception caught. Exiting..');
                sys.exit(errno.EXIT_FAILURE);
            else:
                attempt += 0x1;
            self.__connect();
            self.get_all_activity(attempt);
        except MySQLdb.DatabaseError as ex:
            traceback.print_exc();
        finally:
            cursor.close();
        return events;
        
    def toggle_device(self, device_id, status):

        cursor = None;
        toggled = False;
        try:
            cursor = self._conn.cursor();
            cursor.execute(dbquery['UPDATE_DEVICE_STATUS'], (status, device_id));
            self._conn.commit();
            toggled = True;
        except MySQLdb.DatabaseError as ex:
            traceback.print_exc();
        finally:
            cursor.close();
            
        return toggled;
    
    def get_all_activity(self, attempt=0x0):

        cursor = None;
        events = [];
        
        try:
            cursor = self._conn.cursor(MySQLdb.cursors.DictCursor);
            cursor.execute(dbquery['GET_ALL_ACTIVITY']);
            rset = cursor.fetchall();
            if not (isinstance(rset, NoneType)):
                for rdx in rset:
                    events.append(rdx);
        except MySQLdb.OperationalError as opex:
            if(attempt > 0x3):
                raise FatalException('Unrecovable exception caught. Exiting..');
                sys.exit(errno.EXIT_FAILURE);
            else:
                attempt += 0x1;
            self.__connect();
            self.get_all_activity(attempt);
        except MySQLdb.DatabaseError as ex:
            traceback.print_exc();
        finally:
            cursor.close();
        return events;
    
if __name__ == '__main__':
    
    config = {
        'DB_HOST': '127.0.0.1',
        'DB_USER': 'root',
        'DB_PASSWD': 'root',
        'DB_NAME': 'autohome-dev',
        }
    
    db = DBFactory(config);
    #events = db.get_all_avtivity();
    db.toggle_device(8, 2);
    
    
    
    
    