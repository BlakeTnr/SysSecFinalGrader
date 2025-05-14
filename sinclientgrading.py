import gradinglib
from logger import logger
from pyVmomi import vim
import re

def check_public_ip(vm: vim.VirtualMachine, content: vim.ServiceInstanceContent):
    logger.debug(f"Running public IP checks for {vm.name}...")
    guest_username, guest_password = gradinglib.get_vm_creds(vm)
    gradinglib.power_on_vm(vm)
    gradinglib.vm_execute_firewalloff_command(vm, guest_username, guest_password, content)

    try:
        output = gradinglib.execute_vm_command(vm, guest_username, guest_password, "ifconfig em0", content, "/bin/sh")
        regex = "(?<=inet 192.168.)\d*(?=.0)"
        match = re.findall(regex, output)[0]
        pfsensepublic = "10" + match
        teamname = vm.parent.name
        teamnumber = gradinglib.team_name_to_number(teamname)

        if(pfsensepublic == "10" + str(teamnumber)):
            logger.info(f"SUCCESS! {vm.name} in {vm.parent.name} passed. Public IP is correct.")
        else:
            logger.warn(f"FAILED! {vm.name} in {vm.parent.name} failed. Public IP is incorrect.")
        print(output)
    except vim.fault.GuestOperationsUnavailable as e:
        logger.warn(f"FAILED! {vm.name} in {vm.parent.name} failed. Guest operations unavailable.")
        return
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return
    finally:
        gradinglib.power_off_vm(vm)
        logger.debug(f"Powering off {vm.name}...")