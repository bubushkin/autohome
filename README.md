## OVERVIEW
home-auto is a web application written in Python 2.7 using a Flask framework. It uses Bootstrap for front-end and MySQL for backend.
Upon execution home-auto initialize all devices by creating a gpio device objects and registers them in database. Device objects are stored in application context for the duration of execution. 


## INSTALL:
Update and install required packages.
`````
iskandar@sparthos:~$ sudo apt-get update -y
iskandar@sparthos:~$ sudo apt-get upgrade -y
iskandar@sparthos:~$ sudo apt-get install apache2 -y
iskandar@sparthos:~$ sudo apt-get install apache2-dev -y
iskandar@sparthos:~$ sudo apt-get install apache2-mpm-worker -y
iskandar@sparthos:~$ sudo apt-get install libapache2-mod-wsgi -y
iskandar@sparthos:~$ sudo apt-get install apache2-utils
iskandar@sparthos:~$ apt-get install mysql-server
`````
Clone the repository from github. (username and password is stripped from the listing)
`````
iskandar@sparthos:~$ cd /tmp/
iskandar@sparthos:/tmp$ git clone https://github.com/bubushkin/home-auto.git
Cloning into 'home-auto'...
Username for 'https://github.com': 
Password for 'https://@github.com': 
remote: Enumerating objects: 345, done.
remote: Counting objects: 100% (345/345), done.
remote: Compressing objects: 100% (259/259), done.
remote: Total 345 (delta 89), reused 313 (delta 77), pack-reused 0
Receiving objects: 100% (345/345), 5.51 MiB | 5.27 MiB/s, done.
Resolving deltas: 100% (89/89), done.
Checking connectivity... done.
`````
Install python modules:
`````
iskandar@sparthos:/tmp$ cd home-auto/
iskandar@sparthos:/tmp/home-auto$ pip install -r requirements.txt
`````
## CONFIGURATION:
Create a virtual host record in httpd.conf | apache.conf
Also make sure you add your apache user to gpio group. Otherwise you will not be able to issue gpio calls. 
`````
Listen 8080
<VirtualHost *:8080>
    ServerName homeauto.home

    WSGIDaemonProcess homeauto user=www-data group=www-data threads=5
    WSGIScriptAlias / /var/www/html/webapps/homeautobot/index.wsgi

    <Directory /var/www/html/webapps/homeautobot>
        WSGIProcessGroup homeauto
        WSGIApplicationGroup %{GLOBAL}
        Order deny,allow
        Allow from all
    </Directory>
</VirtualHost>
``````
Import MySQL database:
`````
iskandar@sparthos:/tmp/home-auto$ mysql -u root -p < autohome-dev.sql
`````
Create directory for camera thread:
`````
iskandar@sparthos: mkdir -p /tmp/picamera/{picture,video}
`````

For simulation purposes application MySQL root user can be used to connect to database. ````root```` is also used in configurations. 
Please be certain to update database connection details in  ````home-auto/homeauto/config/config.py````.

## EXECUTION:
### WARNING: 
By default application starts separate "Visual" (````home-auto/homeauto/engine/visual.py````) thread. However, due to a resource limitations in
raspberry pi, wsgi module in apache is unable to initialize properly when "visual" thread is executed. It runs out of memory when tries to serve a webpage. 
Alernative to this is to run  ````python automain.py````. This will run application in development/testing mode spinning up  
visual thread and will listen on port 8080. (This can be used for simulations).

Apache version:
`````
iskandar@sparthos:$ cd /tmp/
iskandar@sparthos:/tmp$ cp -r home-auto /var/www/html/webapps/homeautobot
iskandar@sparthos:/tmp/home-auto$ /etc/init.d/apache2 restart
`````
(Alternative) Python:
`````
iskandar@sparthos:/tmp/home-auto$ python automain.py
`````
Application will be accessible via http://{FQDN}:8080/index




 
