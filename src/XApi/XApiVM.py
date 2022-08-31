from dataclasses import dataclass
from src.XApi.XApiConnect import XApiConnect
from src.XApi.XApiVBD import XApiOneVbd

@dataclass
class XApiOneVm():
    """
    VM structure from XAPI

    uuid  :  0e16dc5f-a169-c322-2790-fa4e3ca3e47f
    allowed_operations  :  ['destroy', 'export', 'revert', 'clone', 'copy']
    current_operations  :  {}
    name_label  :  Deb11 shapshot on SR01
    name_description  :  
    power_state  :  Halted
    user_version  :  1
    is_a_template  :  True
    is_default_template  :  False
    suspend_VDI  :  OpaqueRef:NULL
    resident_on  :  OpaqueRef:NULL
    scheduled_to_be_resident_on  :  OpaqueRef:NULL
    affinity  :  OpaqueRef:0a30f686-7f9b-46ee-807c-f2ee10033a11
    memory_overhead  :  11534336
    memory_target  :  1073741824
    memory_static_max  :  1073741824
    memory_dynamic_max  :  1073741824
    memory_dynamic_min  :  1073741824
    memory_static_min  :  536870912
    VCPUs_params  :  {}
    VCPUs_max  :  1
    VCPUs_at_startup  :  1
    actions_after_shutdown  :  destroy
    actions_after_reboot  :  restart
    actions_after_crash  :  restart
    consoles  :  []
    VIFs  :  ['OpaqueRef:96024719-26b9-4920-9d49-0d35474bf26c']
    VBDs  :  ['OpaqueRef:5c1c82ca-8e67-461b-904b-688c736ed58d', 'OpaqueRef:3426841d-4837-4347-a6a2-77d49b047167']
    VUSBs  :  []
    crash_dumps  :  []
    VTPMs  :  []
    PV_bootloader  :  
    PV_kernel  :  
    PV_ramdisk  :  
    PV_args  :  
    PV_bootloader_args  :  
    PV_legacy_args  :  
    HVM_boot_policy  :  BIOS order
    HVM_boot_params  :  {'firmware': 'bios', 'order': 'cdn'}
    HVM_shadow_multiplier  :  1.0
    platform  :  {'timeoffset': '1', 'videoram': '8', 'hpet': 'true', 'secureboot': 'false', 'device-model': 'qemu-upstream-compat', 'apic': 'true', 'device_id': '0001', 'vga': 'std', 'nx': 'true', 'pae': 'true', 'viridian': 'false', 'acpi': '1', 'cores-per-socket': '4'}
    PCI_bus  :  
    other_config  :  {'instant': 'true', 'base_template_name': 'Debian Bullseye 11', 'import_task': 'OpaqueRef:fd9ecd6c-7694-4725-9454-c3416ab61b20', 'mac_seed': '2ba0d6ac-2515-43bb-84ed-ec5687fe4692', 'install-methods': 'cdrom,nfs,http,ftp', 'linux_template': 'true'}
    domid  :  -1
    domarch  :  
    last_boot_CPU_flags  :  {'vendor': 'GenuineIntel', 'features': '1fcbfbff-809a2221-2c100800-00000001-00000000-00000000-00000000-00000000-00001000-9c000000-00000000-00000000-00000000-00000000-00000000-00000000-00000000-00000000'}
    is_control_domain  :  False
    metrics  :  OpaqueRef:736aa06e-cdfb-4e66-bd86-82fd2c0e8bce
    guest_metrics  :  OpaqueRef:NULL
    last_booted_record  :  
    recommendations  :  <restrictions><restriction field="memory-static-max" max="1649267441664"/><restriction field="vcpus-max" max="32"/><restriction field="has-vendor-device" value="false"/><restriction field="allow-gpu-passthrough" value="1"/><restriction field="allow-vgpu" value="1"/><restriction field="allow-network-sriov" value="1"/><restriction field="supports-bios" value="yes"/><restriction field="supports-uefi" value="no"/><restriction field="supports-secure-boot" value="no"/><restriction max="255" property="number-of-vbds"/><restriction max="7" property="number-of-vifs"/></restrictions>
    xenstore_data  :  {'vm-data/mmio-hole-size': '268435456', 'vm-data': ''}
    ha_always_run  :  False
    ha_restart_priority  :  
    is_a_snapshot  :  True
    snapshot_of  :  OpaqueRef:9c5a38a0-49c5-43c8-87d1-c7ba6ea75a40
    snapshots  :  []
    snapshot_time  :  20220830T13:59:24Z
    transportable_snapshot_id  :  
    blobs  :  {}
    tags  :  []
    blocked_operations  :  {}
    snapshot_info  :  {'disk-snapshot-type': 'crash_consistent', 'power-state-at-snapshot': 'Halted'}
    snapshot_metadata  :  (('xenstore_data' '((\'vm-data/mmio-hole-size\' \'268435456\') (\'vm-data\' \'\'))') ('version' '0') ('uuid' 'fb37964e-a7e7-a5bf-c1b5-02ae064223da') ('user_version' '1') ('transportable_snapshot_id' '') ('tags' '()') ('suspend_VDI' 'OpaqueRef:NULL') ('suspend_SR' 'OpaqueRef:984e8e56-b685-4a19-9640-aeddfa2e5652') ('start_delay' '0') ('snapshots' '()') ('snapshot_time' '19700101T00:00:00Z') ('snapshot_schedule' 'OpaqueRef:NULL') ('snapshot_of' 'OpaqueRef:NULL') ('snapshot_metadata' '') ('snapshot_info' '()') ('shutdown_delay' '0') ('scheduled_to_be_resident_on' 'OpaqueRef:NULL') ('resident_on' 'OpaqueRef:0a30f686-7f9b-46ee-807c-f2ee10033a11') ('requires_reboot' 'false') ('reference_label' 'debian-11') ('recommendations' '<restrictions><restriction field=\"memory-static-max\" max=\"1649267441664\"/><restriction field=\"vcpus-max\" max=\"32\"/><restriction field=\"has-vendor-device\" value=\"false\"/><restriction field=\"allow-gpu-passthrough\" value=\"1\"/><restriction field=\"allow-vgpu\" value=\"1\"/><restriction field=\"allow-network-sriov\" value=\"1\"/><restriction field=\"supports-bios\" value=\"yes\"/><restriction field=\"supports-uefi\" value=\"no\"/><restriction field=\"supports-secure-boot\" value=\"no\"/><restriction max=\"255\" property=\"number-of-vbds\"/><restriction max=\"7\" property=\"number-of-vifs\"/></restrictions>') ('protection_policy' 'OpaqueRef:NULL') ('power_state' 'Halted') ('platform' '((\'timeoffset\' \'1\') (\'videoram\' \'8\') (\'hpet\' \'true\') (\'secureboot\' \'false\') (\'device-model\' \'qemu-upstream-compat\') (\'apic\' \'true\') (\'device_id\' \'0001\') (\'vga\' \'std\') (\'nx\' \'true\') (\'pae\' \'true\') (\'viridian\' \'false\') (\'acpi\' \'1\') (\'cores-per-socket\' \'4\'))') ('parent' 'OpaqueRef:NULL') ('other_config' '((\'instant\' \'true\') (\'base_template_name\' \'Debian Bullseye 11\') (\'import_task\' \'OpaqueRef:fd9ecd6c-7694-4725-9454-c3416ab61b20\') (\'mac_seed\' \'2ba0d6ac-2515-43bb-84ed-ec5687fe4692\') (\'install-methods\' \'cdrom,nfs,http,ftp\') (\'linux_template\' \'true\'))') ('order' '0') ('name__label' 'Debian 11 on SR01') ('name__description' '') ('metrics' 'OpaqueRef:25d64d23-e129-4217-88b9-6b1844dcf361') ('memory__target' '1073741824') ('memory__static_min' '536870912') ('memory__static_max' '1073741824') ('memory__overhead' '11534336') ('memory__dynamic_min' '1073741824') ('memory__dynamic_max' '1073741824') ('last_booted_record' '') ('last_boot_CPU_flags' '((\'vendor\' \'GenuineIntel\') (\'features\' \'1fcbfbff-809a2221-2c100800-00000001-00000000-00000000-00000000-00000000-00001000-9c000000-00000000-00000000-00000000-00000000-00000000-00000000-00000000-00000000\'))') ('is_vmss_snapshot' 'false') ('is_snapshot_from_vmpp' 'false') ('is_default_template' 'false') ('is_control_domain' 'false') ('is_a_template' 'false') ('is_a_snapshot' 'false') ('has_vendor_device' 'false') ('hardware_platform_version' '0') ('ha_restart_priority' '') ('ha_always_run' 'false') ('guest_metrics' 'OpaqueRef:NULL') ('generation_id' '') ('domid' '-1') ('domarch' '') ('domain_type' 'hvm') ('current_operations' '((\'OpaqueRef:a9eda8af-5549-40cd-b56a-6e89054b4d0e\' \'snapshot\'))') ('crash_dumps' '()') ('consoles' '()') ('children' '()') ('blocked_operations' '()') ('blobs' '()') ('bios_strings' '((\'bios-vendor\' \'Xen\') (\'bios-version\' \'\') (\'system-manufacturer\' \'Xen\') (\'system-product-name\' \'HVM domU\') (\'system-version\' \'\') (\'system-serial-number\' \'\') (\'baseboard-manufacturer\' \'\') (\'baseboard-product-name\' \'\') (\'baseboard-version\' \'\') (\'baseboard-serial-number\' \'\') (\'baseboard-asset-tag\' \'\') (\'baseboard-location-in-chassis\' \'\') (\'enclosure-asset-tag\' \'\') (\'hp-rombios\' \'\') (\'oem-1\' \'Xen\') (\'oem-2\' \'MS_VM_CERT/SHA1/bdbeb6e0a816d43fa6d3fe8aaef04c2bad9d3e3d\'))') ('attached_PCIs' '()') ('appliance' 'OpaqueRef:NULL') ('allowed_operations' '(\'snapshot\')') ('affinity' 'OpaqueRef:0a30f686-7f9b-46ee-807c-f2ee10033a11') ('actions__after_shutdown' 'destroy') ('actions__after_reboot' 'restart') ('actions__after_crash' 'restart') ('_ref' 'OpaqueRef:9c5a38a0-49c5-43c8-87d1-c7ba6ea75a40') ('VUSBs' '()') ('VTPMs' '()') ('VIFs' '(\'OpaqueRef:1573533b-9b1f-413f-b7d1-15d56827f51b\')') ('VGPUs' '()') ('VCPUs__params' '()') ('VCPUs__max' '1') ('VCPUs__at_startup' '1') ('VBDs' '(\'OpaqueRef:ee5f3ba2-db7f-478a-98b9-3fe12fb4fd57\' \'OpaqueRef:8caab0d1-503c-47b6-8b12-2ea665d32b63\')') ('PV__ramdisk' '') ('PV__legacy_args' '') ('PV__kernel' '') ('PV__bootloader_args' '') ('PV__bootloader' '') ('PV__args' '') ('PCI_bus' '') ('NVRAM' '()') ('HVM__shadow_multiplier' '1') ('HVM__boot_policy' 'BIOS order') ('HVM__boot_params' '((\'firmware\' \'bios\') (\'order\' \'cdn\'))'))
    parent  :  OpaqueRef:NULL
    children  :  ['OpaqueRef:9c5a38a0-49c5-43c8-87d1-c7ba6ea75a40']
    bios_strings  :  {'bios-vendor': 'Xen', 'bios-version': '', 'system-manufacturer': 'Xen', 'system-product-name': 'HVM domU', 'system-version': '', 'system-serial-number': '', 'baseboard-manufacturer': '', 'baseboard-product-name': '', 'baseboard-version': '', 'baseboard-serial-number': '', 'baseboard-asset-tag': '', 'baseboard-location-in-chassis': '', 'enclosure-asset-tag': '', 'hp-rombios': '', 'oem-1': 'Xen', 'oem-2': 'MS_VM_CERT/SHA1/bdbeb6e0a816d43fa6d3fe8aaef04c2bad9d3e3d'}
    protection_policy  :  OpaqueRef:NULL
    is_snapshot_from_vmpp  :  False
    snapshot_schedule  :  OpaqueRef:NULL
    is_vmss_snapshot  :  False
    appliance  :  OpaqueRef:NULL
    start_delay  :  0
    shutdown_delay  :  0
    order  :  0
    VGPUs  :  []
    attached_PCIs  :  []
    suspend_SR  :  OpaqueRef:NULL
    version  :  0
    generation_id  :  
    hardware_platform_version  :  0
    has_vendor_device  :  False
    requires_reboot  :  False
    reference_label  :  debian-11
    domain_type  :  hvm
    NVRAM  :  {}
    """

    vm_uuid: str
    vm_name_label: str
    vm_name_description: str
    vm_is_a_snapshot: bool
    vbd: XApiOneVbd

    def __str__(self):
        return f"VM uuid: {self.vm_uuid} | VM Name: {self.vm_name_label} | VM Is Snapshot: {self.vm_is_a_snapshot} | VBD(object) {self.vbd}"

    def __repr__(self):
        return str(self)

class XApiVmList:
    """
    VMs
    """

    def __init__(self, xapi: XApiConnect) -> None:
        self.__xapi = xapi
        self.__all_vm: list[XApiOneVm] = []

    def set_VMs(self, vbds: list[XApiOneVbd]) -> None:
        """
        Set list[XApiOneVbd]
        """
        for one_vbd in vbds:
            self.__create_vm_list(one_vbd)

    def get_VMs(self) -> list[XApiOneVm]:
        """
        List with all information about VM (SR, VDI, VBD but for one VDI from VM)
        Return list[XApiOneVm]
        """
        return self.__all_vm

    def __create_vm_list(self, one_vbd: XApiOneVbd) -> None:
        """
        Get data from VM and append new XApiOneVm dataclasses to "all_vm" list
        :return: None
        """

        # load one by one VM to a dataclass list
        # ..._or = OpaqueRef
        record = self.__xapi.session.xenapi.VM.get_record(one_vbd.vbd_vm)
        self.__all_vm.append(
            XApiOneVm(
                vm_uuid = record["uuid"],
                vm_name_label = record["name_label"],
                vm_name_description = record["name_description"],
                vm_is_a_snapshot = record["is_a_snapshot"],
                vbd = one_vbd
                )
            )
