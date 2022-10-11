# Disaster backup for XCP-NG (XenServer) VDI disks files on NFS storages

## Reason

In case the mounted NFS array is forgotten in xcp-ng (xenserver) and the array itself is fine. In this case, the virtual servers will lose their disks without the possibility of recovery. This simple script stores the link of the vdi uuid on the disk with the name of the virtual server for disaster recovery. It simply stores individual versions from the time of the backup and can be viewed using the built-in web application. Cron is used to set how often the current status should be saved, and at the same time a function for deleting old versions is included. More in the configuration file. Remember that this disaster recovery should not run in the virtual environment you are backing up! This script only reads the values from the xapi and stores them in a database that can be viewed through the built-in web interface.

## Install

- create MySQL database (/doc/database.sql)
- create venv (python3 -m venv /path/to/new/virtual/environment)
- activate venv
- install dependencies (pip3 install -r requirements.txt)
- copy config-default.yml to config.yml and configure it
- generate new password for web (/doc/BCrypt.py)
- create log file (touch /var/log/xs-storage.log)
- available commands: python3 xs_nfs_storage.py run | delete
- before use built-in web app you must use command 'run'

## Install and run Unicorn webpage

- copy /doc/xs-nfs-storage.service to /etc/systemd/system/
- systemctl enable xs-nfs-storage.service
- install nginx
- configure nginx (template in /doc/nginx-template.conf)
- systemctl start xs-nfs-storage.service
- if web app is working, secure web (certbot --nginx -d xsnfs.example.com)
- full example" https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04

## Test on
- XCP-NG 8.2.1 with october 2022 maintenance update
- Mariadb 10.3.34 and 10.6.7
- Python 3.10.6 and 3.10.7