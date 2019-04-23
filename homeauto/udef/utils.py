'''
Created on Dec 8, 2018

@author: iskandar
'''

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
import pyimgur;
from twilio.rest import Client

def send_sms(txt="Motion Dectected", attach=None):

    ACCOUNT_SID="";
    AUTH_TOKEN="";
    
    TO_PHONE="";
    
    FROM_PHONE="";
    
    TXT_MSG="Door alarm triggered";
    
    CLIENT_ID="";
    
    client=Client(ACCOUNT_SID,AUTH_TOKEN);
    im=pyimgur.Imgur(CLIENT_ID);    

    if(attach):
        uploaded_image=im.upload_image(attach,title=TXT_MSG)
        client.messages.create(to=TO_PHONE, from_=FROM_PHONE,body=TXT_MSG, media_url=uploaded_image.link)
    
    client.messages.create(to=TO_PHONE, from_=FROM_PHONE,body=TXT_MSG);

def send_email(subject="Motion Detected", to_email="", attach=None):
    
    msg = MIMEMultipart()
    
    msg['Subject'] = subject 
    msg['From'] = '';
    msg['To'] = ', '.join(to_email);
    
    payload_txt = "Motion detected. Please see attached photo.";
    if(attach):
        attachment = open(attach, 'rb');
    
    msg.attach(MIMEText(payload_txt, 'plain'));
    
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    if(attach):
        part.add_header('Content-Disposition', "attachment; filename= %s" % attach);
     
    msg.attach(part);
    server = smtplib.SMTP('smtp.gmail.com', 587);
    server.starttls();
    server.login('', "");
    text = msg.as_string();
    server.sendmail('', to_email, text);
    server.quit();
    

if __name__ == "__main__":
    send_sms();
    
