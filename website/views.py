from dataclasses import dataclass
from tracemalloc import Snapshot
from flask import (
    Blueprint,
    flash,
    request,
    render_template,
    redirect,
    session,
    url_for
 )
#import os, re, glob, yaml, subprocess, pwd, grp
#from pathlib import PurePath
from .database import VDIMySQL
from src.Config import LoadConfig

views = Blueprint('views', __name__)

@dataclass
class vms():
    vm_uuid: str
    vm_name_label: str
    vm_name_description: str
    vdi_name_label: str
    vdi_uuid: str
    vbd_device: str
    storage_name_label: str
    storage_name_description: str
    snapshots: list

    def __str__(self):
        return f"VM uuid: {self.vm_uuid} | VM NAME: {self.vm_name_label} | Storage: {self.storage_name_label}"

    def __repr__(self):
        return str(self)

@dataclass
class snapshots():
    vm_uuid: str
    vm_name_label: str
    vm_snapshot_of: str
    vm_name_description: str
    vdi_name_label: str
    vdi_uuid: str
    vbd_device: str
    storage_name_label: str
    storage_name_description: str

    def __str__(self):
        return f"Snapshot of: {self.vm_snapshot_of} | VM uuid: {self.vm_uuid} | VM NAME: {self.vm_name_label} | Storage: {self.storage_name_label}"

    def __repr__(self):
        return str(self)

@views.route('/')
def home():
    user_id = session.get('user_id')

    if user_id is None:
        return redirect(url_for('auth.login'))

    config = LoadConfig()
    mysql = VDIMySQL(config)
    vdi_versions = mysql.get_versions()
    last_version = max(vdi_versions)[0]

    # get all vms from specific version
    all_vm = mysql.get_vms(last_version)
    vm_list = [];
    for one_vm in all_vm:
        vm_list.append(
            vms(
                vm_uuid = one_vm[0],
                vm_name_label = one_vm[1],
                vm_name_description = one_vm[2],
                vdi_name_label = one_vm[3],
                vdi_uuid = one_vm[4],
                vbd_device = one_vm[5],
                storage_name_label = one_vm[6],
                storage_name_description = one_vm[7],
                snapshots = []
                )
            )
    # print(vm_list)
    # exit()

    # get all snapshots and add it to right vm
    all_snapshots = mysql.get_snapshots(last_version)
    snapshots_list = []
    for one_snapshot in all_snapshots:
        snapshots_list.append(
            snapshots(
                vm_uuid = one_snapshot[0],
                vm_name_label = one_snapshot[1],
                vm_snapshot_of = one_snapshot[2],
                vm_name_description = one_snapshot[3],
                vdi_name_label = one_snapshot[4],
                vdi_uuid = one_snapshot[5],
                vbd_device = one_snapshot[6],
                storage_name_label = one_snapshot[7],
                storage_name_description = one_snapshot[8]
                )
            )
    # print(snapshots_list)
    # exit()

    # TODO prirad snapshoty vm

    return render_template("home.html", vdi_versions=vdi_versions, actual_version=last_version)

@views.route('/new-dkim', methods=['GET', 'POST'])
def newDkim():
    """
    Vygeneruje novy DKIM podle zaslaneho nazvu domeny.
    Nastavi zaroven vse potrebne na serveru.
    """
    user_id = session.get('user_id')

    if user_id is None:
        return redirect(url_for('auth.login'))

    # if request.method == 'POST':
    #     domain = request.form['domain'].strip()

    #     # Check domain whois and subdomain
    #     if is_registered(domain) and domain.count('.') == 1:

    #         # Check if domain is not existing in DKIM
    #         dkim_files = load_dkim()
    #         for x in dkim_files:
    #             if x.domain == domain:
    #                 flash('Doména už v seznamu existuje!', category='error')
    #                 return redirect(url_for('views.home'))

    #         # Generate DKIM
    #         # rspamadm dkim_keygen -s mail -b 2048 -d best-net.cz -k /etc/rspamd/local.d/dkim/best-net.cz.private > /etc/rspamd/local.d/dkim/best-net.cz.txt
    #         command = ["/usr/bin/rspamadm dkim_keygen -s mail -b 2048 -d " + domain + " -k " + cfg['dkim_path'] + domain + ".private > " + cfg['dkim_path'] + domain + ".txt"]
    #         subprocess.run(command, shell=True, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
    #         # Add domain keys to dkim_domains.map and add selector to dkim_selectors.map
    #         domain_map = domain + " " + cfg['dkim_path'] + domain + ".private\n"
    #         selector_map = domain + " mail\n"

    #         append_to_file(cfg['dkim_domains_path'], domain_map)
    #         append_to_file(cfg['dkim_selector_path'], selector_map)

    #         os.chmod(cfg['dkim_path'] + domain + ".private", 0o600)
    #         os.chmod(cfg['dkim_path'] + domain + ".txt", 0o600)

    #         uid = pwd.getpwnam("_rspamd").pw_uid
    #         gid = grp.getgrnam("_rspamd").gr_gid
    #         os.chown(cfg['dkim_path'] + domain + ".private", uid, gid)
    #         os.chown(cfg['dkim_path'] + domain + ".txt", uid, gid)

    #         flash('Vše proběhlo OK. Nyní si zobraz DKIM a přidej ho do DNS.', category='success')
    #         return redirect(url_for('views.home'))

    #     flash('Doména neexistuje, nebo je to subdoména. Zkus to bez www.', category='error')
        return redirect(url_for('views.home'))

    # Form POST error
    return redirect(url_for('views.home'))

# @views.route('/delete-dkim', methods=['GET', 'POST'])
# def deleteDkim():
#     """
#     TODO: delete dkim
#     """
#     return redirect(url_for('views.home'))

# class Dkim:
#     def __init__(self, id, path, raw):
#         self.id = id
#         self.path = path
#         self.domain = os.path.basename(path).replace('.txt', '')
#         self.raw = raw
#         self.dkim = self.__parse_dkim(raw)

#     def __parse_dkim(self, raw):
#         raw = re.sub(r"[\n\t\s\"]*", "", raw)
#         raw = re.sub(r".*p=", "", raw)
#         raw = re.sub(r"\);.*", "", raw)
#         return raw

#     def __repr__(self):
#         return f'<Dkim: {self.dkim}>'

# def is_registered(domain_name):
#     """
#     A function that returns a boolean indicating 
#     whether a `domain_name` is registered
#     """
#     try:
#         #w = whois.whois(domain_name)
#         pass
#     except Exception:
#         return False
#     else:
#         return bool(w.domain_name)

# def load_dkim():
#     """
#     Load info from dkim keys files to class
#     """
#     dkim = [];
#     files = glob.glob(cfg["dkim_path"] + '*.txt')
#     files.sort()
#     id = 0
#     for path in files:
#         with open(path) as f:
#             lines = f.readlines()
#         dkim.append(Dkim(id, path, ''.join(lines)))
#         id = id+1
#     return dkim

# def append_to_file(file_name, text_to_append):
#     """Append given text as a new line at the end of file"""
#     # Open the file in append & read mode ('a+')
#     with open(file_name, "a") as file_object:
#         # Append text at the end of file
#         file_object.write(text_to_append)