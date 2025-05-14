import gradinglib
from logger import logger
from pyVmomi import vim
import re

def check_servernet_ip(vm: vim.VirtualMachine, content: vim.ServiceInstanceContent):
    guest_username, guest_password = gradinglib.get_vm_creds(vm)
    gradinglib.power_on_vm(vm)
    gradinglib.vm_execute_firewalloff_command(vm, guest_username, guest_password, content)

    try:
        output = gradinglib.execute_vm_command(vm, guest_username, guest_password, "ip a", content, "/bin/sh")
        regex = "(?<=inet 10.43.)\d*(?=.101)"
        match = re.findall(regex, output)[0]
        teamname = vm.parent.name
        teamnumber = gradinglib.team_name_to_number(teamname)
        
        if(teamnumber == match):
            logger.info(f"SUCCESS! {vm.name} in {vm.parent.name} passed. RockyDB IP is correct.")
        else:
            logger.warn(f"FAILED! {vm.name} in {vm.parent.name} failed. RockyDB IP is incorrect.")
        

        print(output)
    except vim.fault.GuestOperationsUnavailable as e:
        logger.warn(f"FAILED! {vm.name} in {vm.parent.name} failed. Guest operations unavailable.")