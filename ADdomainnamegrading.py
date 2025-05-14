import gradinglib
from logger import logger
from pyVmomi import vim
import re

def check_ad_domain_name(vm: vim.VirtualMachine, content: vim.ServiceInstanceContent):
    logger.debug(f"Running AD domain name check for {vm.name}...")
    guest_username, guest_password = gradinglib.get_vm_creds(vm)

    try:
        command = "wmic computersystem get domain"
        output = gradinglib.execute_vm_command(vm, guest_username, guest_password, command, content, "cmd.exe")
        
        regex = r"Domain\s+([\w.-]+)"
        match = re.search(regex, output)
        
        if not match:
            logger.warn(f"FAILED! {vm.name} in {vm.parent.name} failed. Could not find a domain name.")
            return
        
        domain_name = match.group(1).strip()
        logger.debug(f"Extracted domain name: {domain_name}")
        
        expected_domain = "catflix.local" 
        if domain_name.lower() == expected_domain.lower():
            logger.info(f"SUCCESS! {vm.name} in {vm.parent.name} passed. Domain name is correct.")
        else:
            logger.warn(f"FAILED! {vm.name} in {vm.parent.name} failed. Domain name is incorrect.")
    except vim.fault.GuestOperationsUnavailable as e:
        logger.warn(f"FAILED! {vm.name} in {vm.parent.name} failed. Guest operations unavailable.")
        return
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return