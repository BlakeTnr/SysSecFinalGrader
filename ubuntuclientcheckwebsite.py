import gradinglib
from logger import logger
from pyVmomi import vim
import re

def check_servernet_ip(vm: vim.VirtualMachine, content: vim.ServiceInstanceContent):
    guest_username, guest_password = gradinglib.get_vm_creds(vm)
    gradinglib.power_on_vm(vm)
    gradinglib.vm_execute_firewalloff_command(vm, guest_username, guest_password, content)

    try:
        teamname = vm.parent.name
        teamnumber = gradinglib.team_name_to_number(teamname)
        output = gradinglib.execute_vm_command(vm, guest_username, guest_password, f"wget -O- 10.43.{teamnumber}.102", content, "/bin/sh")
        regex = "mw\-panel"
        match = re.findall(regex, output)

        if(len(match) == 0):
            logger.warn(f"FAILED! {vm.name} in {vm.parent.name} failed. Wget doesn't have mediawiki panel (mw-panel).")
            return
        
        regex = "[cC]atflix"
        match = re.findall(regex, output)
        
        if(len(match) > 5):
            logger.info(f"SUCCESS! {vm.name} in {vm.parent.name} passed. Wget has more than 5 catflix texts.")
        else:
            logger.warn(f"FAILED! {vm.name} in {vm.parent.name} failed. Wget did not have more than 5 catflix texts.")
        

        print(output)
    except vim.fault.GuestOperationsUnavailable as e:
        logger.warn(f"FAILED! {vm.name} in {vm.parent.name} failed. Guest operations unavailable.")