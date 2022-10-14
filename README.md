# Disaster backup for XCP-NG (XenServer) VDI disks files on NFS storages

## Reason

This script is used in case the NFS storage was inadvertently removed (forgotten). In this situation the virtual servers lose information about the connected disks without the possibility of recovery. This simple script stores the link of the vdi uuid on the disk with the name of the virtual server for disaster recovery. Script simply stores individual versions from the time of the backup and can be viewed using the built-in web application. Cron is used to set how often the current status should be saved. The function for deleting old versions at the same time is included. For more information see configuration file. This disaster recovery should not run in the virtual environment that you are backing up! This script only reads the values from the XAPI and stores them in a database that can be viewed through the built-in web interface.

## Install

- create MySQL database (/doc/database.sql)
- create venv (python3 -m venv /path/to/new/virtual/environment)
- activate venv
- install dependencies (pip3 install -r requirements.txt)
- copy config-default.yml to config.yml and configure it
- to generate new password for web use /doc/BCrypt.py
- create log file (touch /var/log/xs-storage.log)

## Usage

```
python3 xs_nfs_storage.py <run|delete>
```

before use built-in web app you must first run: python3 xs_nfs_storage.py run

## Cron
- edit cron_nfs_storage.sh file and configure 'INSTALL_PATH' and 'VENV_DIR_NAME' options
```
# cron example
30 3    * * *   root    /opt/xs-nfs-storage/cron_nfs_storage.sh run
30 4    * * 0   root    /opt/xs-nfs-storage/cron_nfs_storage.sh delete
```

## Webpage

- copy /doc/xs-nfs-storage.service to /etc/systemd/system/
- systemctl enable xs-nfs-storage.service
- install nginx
- configure nginx (template in /doc/nginx-template.conf)
- systemctl start xs-nfs-storage.service
- if web app is working, secure web (certbot --nginx -d xsnfs.example.com)
- flask app with Gunicorn example here: https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04

## Successfuly tested with
- XCP-NG 8.2.1 with october 2022 maintenance update
- Mariadb 10.3.34 and 10.6.7
- Python 3.10.6 and 3.10.7
- Ubuntu 22.04.1
- venv: Package / Version
  - bcrypt                 4.0.1
  - click                  8.1.3
  - fire                   0.4.0
  - Flask                  2.2.2
  - Flask-Bcrypt           1.0.1
  - Flask-WTF              1.0.1
  - future                 0.18.2
  - gunicorn               20.1.0
  - itsdangerous           2.1.2
  - Jinja2                 3.1.2
  - MarkupSafe             2.1.1
  - mysql-connector-python 8.0.30
  - pathlib2               2.3.7.post1
  - pip                    22.0.2
  - protobuf               3.20.1
  - python-whois           0.8.0
  - PyYAML                 6.0
  - setuptools             59.6.0
  - six                    1.16.0
  - termcolor              2.0.1
  - Werkzeug               2.2.2
  - WTForms                3.0.1
  - XenAPI                 2.14

## [License MIT](license.txt)

## Conclusion

This script was created based on the [XAPI](https://github.com/xapi-project/xen-api) study and is not intended to replace standard disaster recovery tools. It is not a priority to develop the script without the interest of the community or other developers. I will be glad for any warnings about bugs in the code or pull requests.

## Special thanks
Thank you very much to [BEST-HOSTING s.r.o.](https://best-hosting.cz) for providing resources for testing.