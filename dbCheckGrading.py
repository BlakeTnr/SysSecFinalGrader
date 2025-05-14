import gradinglib
from logger import logger
from pyVmomi import vim
import re

def check_mariadb_wikidb(vm: vim.VirtualMachine, content: vim.ServiceInstanceContent):
    logger.debug(f"Running MariaDB check for 'wikidb' on {vm.name}...")
    guest_username, guest_password = gradinglib.get_vm_creds(vm)

    try:
        command = "mysql -u root -e 'SHOW DATABASES;'"
        output = gradinglib.execute_vm_command(vm, guest_username, guest_password, command, content, "/bin/bash")
        
        if "wikidb" in output:
            logger.info(f"SUCCESS! {vm.name} has the 'wikidb' database.")
        else:
            logger.warn(f"FAILED! {vm.name} does not have the 'wikidb' database.")
    except vim.fault.GuestOperationsUnavailable as e:
        logger.warn(f"FAILED! {vm.name} in {vm.parent.name} failed. Guest operations unavailable.")
        return
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return

