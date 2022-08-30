#!/opt/xs-storage/xs-storage-env/bin/python

import sys, time
import XenAPI

# def myfunc(session, iteration):
#     # Find a non-template VM object
#     all = session.xenapi.VM.get_all()
#     vms = []
#     hosts = []
#     for vm in all:
#         record = session.xenapi.VM.get_record(vm)
#         if not(record["is_a_template"]) and \
#            not(record["is_control_domain"]) and \
#            record["power_state"] == "Running":
#             vms.append(vm)
#             hosts.append(record["resident_on"])
#     print("%d: Found %d suitable running VMs" % (iteration, len(vms)))

def getSR(session):
    all = session.xenapi.SR.get_all()
    print("---------------------")
    for vm in all:
        record = session.xenapi.SR.get_record(vm)
        if (record["type"] == "nfs"):
            print(record["uuid"], record["name_label"])
            print("---------------------")

def getVDI(session: XenAPI.Session):
    """
    1. zjisti vsechny VDI
    2. podle jednoho VDI se zjisti na jakem je SR, pokud je to na NFS pokracuje dal
    3. proskenuje vsechny VBDs a urkci k jakem VM patri

    tip:
    xapi používá OpaqueRef jako skutečný identifikátor objektu,
    primární klíč v interní databázi xapi. Když jeden objekt
    ukazuje na druhý, neříká 'link=uuid', říká 'link=opaqueref'.

    Jak tedy aktualizovat uuid disku? Jak zjistim zmenu?

    or = OpaqueRef
    """

    # zjisti vsechny idenfifikatory VDI. Vraci list OpaqueRef VDIs
    all_vdi_or = session.xenapi.VDI.get_all()

    for one_vdi_or in all_vdi_or:

        # VDI Record - kompletni informace o VDI (VDI je fyzicky soubor na disku, ktery se pripojuje s VM pres VBD)
        vdi_record = session.xenapi.VDI.get_record(one_vdi_or)

        # trochu to zrychlime - vdi musi mit VBD, jinak me nezajima
        if not vdi_record["VBDs"]:
            continue

        # get_SR - vraci OpaqueRef SR danneho VDI 
        # sr_or = session.xenapi.VDI.get_SR(one_vdi_or) # lze pouzit vdi_record['SR'] - setrime dotazy do xapi
        # print(sr_or)

        # z get_SR mam OpaqueRef dannerh SR, nyni porebuji podrobnosti o SR
        sr_record = session.xenapi.SR.get_record(vdi_record['SR'])

        # zajima nas jen co je na NFS SRs
        if sr_record["type"] != "nfs":
            continue

        print()
        print("VDI RECORD:")
        for key, value in vdi_record.items():
            print(key, ' : ', value)

        print()
        print("SR RECORD:")
        for key, value in sr_record.items():
            print(key, ' : ', value)

        # k jakemu VM disk (VDI) patri. Vraci seznam. Jeden disk muze byt tedy pripojen k vice VM
        # all_vbds_or = session.xenapi.VDI.get_VBDs(one_vdi_or) - lze pouzit vdi_record["VBDs"] - setrime dotazy do xapi
        for one_vbd_or in vdi_record["VBDs"]:
            # vrati informace o VBD, ale je v nem pouze OpaqueRef na VM
            vbd_record = session.xenapi.VBD.get_record(one_vbd_or)
            print()
            print("VBD RECORD:")
            for key, value in vbd_record.items():
                print(key, ' : ', value)
            
            # zjisti jakemu VM patri
            vm_record = session.xenapi.VM.get_record(vbd_record['VM'])
            print()
            print("VM RECORD:")
            for key, value in vm_record.items():
                print(key, ' : ', value)

        print("============================================================================================================")

def getMethods(session):
    """
    Get all methods from xapi (xmlrpc)
    https://www.pythonstudio.us/beginning-3/the-xmlrpc-introspection-api.html
    """
    all = session.system.listMethods()
    for method in all:
        print(method)
    # asi neni implementovano
    # print(session.system.methodHelp(<string MethodName>))
    

if __name__ == "__main__":
    iterations = 1
    session = XenAPI.Session("https://xcp-test.best-hosting.cz")
    session.xenapi.login_with_password("root", "LTerfnu20!", "2.3", "hexim xs-storage v0.1")
    try:
        for i in range(iterations):
            #myfunc(session, i)
            #getSR(session)
            getVDI(session)
            # getMethods(session)
    finally:
        session.xenapi.session.logout()
