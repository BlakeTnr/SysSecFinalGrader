import gradinglib
from pyVmomi import vim
from logger import logger
import re

def check_pfsense(vm: vim.VirtualMachine, content: vim.ServiceInstanceContent):
    logger.debug(f"Running pfsense checks for {vm.name}...")
    guest_username, guest_password = gradinglib.get_vm_creds(vm)
    gradinglib.power_on_vm(vm)
    gradinglib.vm_execute_firewalloff_command(vm, guest_username, guest_password, content)

    try:
        output = gradinglib.execute_vm_command(vm, guest_username, guest_password, "ifconfig em0", content, "/bin/sh")
        regex = "(?<=inet 192.168.254.)\d\d\d"
        match = re.findall(regex, output)[0]

        print(output)
    except vim.fault.GuestOperationsUnavailable as e:
        logger.warn(f"FAILED! {vm.name} in {vm.parent.name} failed. Guest operations unavailable.")