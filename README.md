# Disaster backup of xenserver (XCP-NG) VDIs disk file names on NFS SR


## Install

- create MySQL database (/doc/database.sql)
- create venv (python3 -m venv /path/to/new/virtual/environment)
- activate venv
- install dependencies (pip3 install -r requirements.txt)
- copy config-default.yml to config.yml and configure it
- create log file in /var/log/xs-storage.log
- create logrotate config for log file
- available commands: xs_nfs_storage.py run | delete

## Install and run Unicorn webpage

- copy /doc/xs-nfs-storage.service to /etc/systemd/system/
- systemctl enable xs-nfs-storage.service
- install nginx
- configure nginx (template in /doc/)

## Tests on
- XCP-NG 8.2.1
- Mariadb 10.3.34
- PHP 8.1.6