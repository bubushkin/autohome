'''
Created on Dec 3, 2018

@author: iskandar
'''
import time;
import sys;
import imaplib;
import email;
from email.parser import HeaderParser
import datetime;
import requests;
from dbfactory import DBFactory;

config = {
    'ACCOUNT': '',
    'PASSWD': '',
    'SMTP_SERVER': 'imap.gmail.com',
    'SMTP_PORT': 993,
    'MAILBOX': 'inbox',
    'DB_HOST': '127.0.0.1',
    'DB_USER': '',
    'DB_PASSWD': '',    
    'DB_NAME': '',
    'API_ENDPOINT': 'http://localhost:8080/action'
    };

GMAIL = imaplib.IMAP4_SSL(config.get('SMTP_SERVER'))

def process_mailbox(M, db):
    rv, data = M.search(None, "ALL")
    if rv != 'OK':
        print "No messages found!"
        return

    for num in data[0].split():
        rv, data = M.fetch(num, '(RFC822)')
        if rv != 'OK':
            print "ERROR getting message", num
            return;

    msg = email.message_from_string(data[0][1])
    print 'Message %s: %s' % (num, msg['Subject'])
    print 'Raw Date:', msg['Date']
    print msg.get_payload();
    payload = msg.get_payload();
    module = parse_directive(payload[0].get_payload().rstrip());
    
    device = db.get_device_by_name(module.get('DEVICE'));
    action = db.get_action_by_name(module.get('ACTION'));
    
    module['DEVICE'] = device['device_id'];
    module['ACTION'] = action['status_id'];
    start_time = time.time(); 
    webcall(module);
    print("REST web call execution time:" + str(time.time() - start_time));
    date_tuple = email.utils.parsedate_tz(msg['Date'])
    if date_tuple:
        local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
        print "Local Date:", local_date.strftime("%a, %d %b %Y %H:%M:%S")
        
def delete_emails(M):

    rv, data = M.search(None, "ALL");
    typ, data = M.search(None, 'ALL')
    for num in data[0].split():
        M.store(num, '+FLAGS', r'(\Deleted)')
    M.expunge()

def webcall(module):
    
    data = {
            'device_id': module['DEVICE'],
            'action': module['ACTION']
            };
    print("Webcall to :" + config['API_ENDPOINT'] + " data: " + str(data));            
    response = requests.post(url = config['API_ENDPOINT'], data = data);
    print("Response:" + response.text);

def parse_directive(directive):
    
    return {
        'DEVICE': directive.split(';')[0x0].split('=')[0x1],
        'ACTION': directive.split(';')[0x1].split('=')[0x1]
        }
    
if __name__ == "__main__":

    try:
        GMAIL.login(config.get('ACCOUNT'), config.get('PASSWD'));
        db = DBFactory(config);
    except imaplib.IMAP4.error:
        print('Unable to login\n');
        sys.exit(0x1);
    
    rv, data = GMAIL.select(config.get('MAILBOX'));
    if(rv == 'OK'):
        print("Processing mailbox " + config.get('MAILBOX'));
        process_mailbox(GMAIL, db);
        delete_emails(GMAIL);
        GMAIL.close()
    GMAIL.logout()    
    db.close();
    