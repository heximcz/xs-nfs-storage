from dataclasses import dataclass
from typing import List
from flask import (
    Blueprint,
    flash,
    request,
    render_template,
    redirect,
    session,
    url_for
 )
from .database import VDIMySQL
from src.Config import LoadConfig

views = Blueprint('views', __name__)

@dataclass
class vms():
    vm_uuid: str
    vm_name_label: str
    vdi_name_label: str
    vdi_uuid: str
    vbd_device: str
    storage_name_label: str
    storage_uuid: str
    snapshots: list

    def __str__(self):
        return f"\nVM uuid: {self.vm_uuid} | VM NAME: {self.vm_name_label} | Storage: {self.storage_name_label} | Snapshots: {self.snapshots}\n"

    def __repr__(self):
        return str(self)

@dataclass
class snapshots():
    vm_uuid: str
    vm_name_label: str
    vm_snapshot_of: str
    vdi_name_label: str
    vdi_uuid: str
    vbd_device: str
    storage_name_label: str
    storage_uuid: str

    def __str__(self):
        return f"\nSnapshot of: {self.vm_snapshot_of} | VM uuid: {self.vm_uuid} | VM NAME: {self.vm_name_label} | Storage: {self.storage_name_label}\n"

    def __repr__(self):
        return str(self)

@views.route('/')
def home():
    """
    Select last version and show it
    """
    user_id = session.get('user_id')

    if user_id is None:
        return redirect(url_for('auth.login'))

    config = LoadConfig()
    mysql = VDIMySQL(config)

    # get all version
    vdi_versions = mysql.get_versions()
    # get last version
    last_version = max(vdi_versions)[0]
    # process data
    vm_list=processData(last_version, mysql)

    return render_template("home.html", vdi_versions=vdi_versions, actual_version=int(last_version), vm_list=vm_list)

@views.route('/show-version', methods=['GET', 'POST'])
def showVersion():
    """
    show selected version of backup
    """
    user_id = session.get('user_id')

    if user_id is None:
        return redirect(url_for('auth.login'))

    # get version from form
    if request.method == 'POST':
        version = request.form['version']
        config = LoadConfig()
        mysql = VDIMySQL(config)

        # get all version
        vdi_versions = mysql.get_versions()
        # process data
        vm_list=processData(version, mysql)

        return render_template("home.html", vdi_versions=vdi_versions, actual_version=int(version), vm_list=vm_list)

    return redirect(url_for('views.home'))

def processData(version: int, mysql: VDIMySQL) -> list:
    """
    process data from database for selected version
    """

    # get all vms from specific version
    all_vm = mysql.get_vms(version)

    # virtual machines list
    vm_list = [];
    for one_vm in all_vm:
        vm_list.append(
            vms(
                vm_uuid = one_vm[0],
                vm_name_label = one_vm[1],
                vdi_name_label = one_vm[2],
                vdi_uuid = one_vm[3],
                vbd_device = one_vm[4],
                storage_name_label = one_vm[5],
                storage_uuid = one_vm[6],
                snapshots = []
                )
            )

    # get all snapshots
    all_snapshots = mysql.get_snapshots(version)

    # snapshots list
    snapshots_list = []
    for one_snapshot in all_snapshots:
        snapshots_list.append(
            snapshots(
                vm_uuid = one_snapshot[0],
                vm_name_label = one_snapshot[1],
                vm_snapshot_of = one_snapshot[2],
                vdi_name_label = one_snapshot[3],
                vdi_uuid = one_snapshot[4],
                vbd_device = one_snapshot[5],
                storage_name_label = one_snapshot[6],
                storage_uuid = one_snapshot[7]
                )
            )

    # add all snapshots to vm.snapshots[]
    for one_vm in vm_list:
        for one_snapshot in snapshots_list:
            if one_vm.vm_uuid == one_snapshot.vm_snapshot_of:
                one_vm.snapshots.append(one_snapshot)

    return vm_list