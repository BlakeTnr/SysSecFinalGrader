import gradinglib
from enum import Enum
import random
import ssl
import atexit
import time
from typing import List
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import re
import pfsensegrading
from logger import logger

# --- Config ---
vcenter = "cdr-vcenter.cse.buffalo.edu"
username = "blaketnr@vsphere.local"
password = ""

guest_username = "sysadmin"
guest_password = "Change.me!"

# --- Disable SSL verification ---
context = ssl._create_unverified_context()

# --- Connect to vCenter ---
si = SmartConnect(host=vcenter, user=username, pwd=password, sslContext=context)
atexit.register(Disconnect, si)

content = si.RetrieveContent()

# --- Find the VM ---
vm = None
logger.debug("getting syssec folder...")
syssecfolder = gradinglib.get_folder_by_path(si, "SysSec")
teamfolder = gradinglib.get_folder_by_name(syssecfolder, "Team_16")
logger.debug("getting teams folder...")
teamfolders = gradinglib.get_folders_by_regex(syssecfolder, "Team_.*")
logger.debug("getting vms...")
vms = gradinglib.get_vm_by_regex(teamfolders, "pfSenseRouter - Final");

logger.debug("running checks...")
for vm in vms:
    pfsensegrading.check_pfsense(vm, content)