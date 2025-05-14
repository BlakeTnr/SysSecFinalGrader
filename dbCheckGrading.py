import gradinglib
from logger import logger
from pyVmomi import vim
import re

def check_mariadb_wikidb(vm: vim.VirtualMachine, content: vim.ServiceInstanceContent):
    logger.debug(f"Running MariaDB check for 'wikidb' on {vm.name}...")
    guest_username, guest_password = gradinglib.get_vm_creds(vm)

    try:
        # First command: Check if we can log in to MariaDB
        login_command = "mysql -u root -e 'SELECT 1;'"
        login_output = gradinglib.execute_vm_command(vm, guest_username, guest_password, login_command, content, "/bin/bash")
        
        if "ERROR" in login_output or "Access denied" in login_output:
            logger.warn(f"FAILED! Unable to log in to MariaDB on {vm.name}.")
            return

        # Second command: Fetch the list of databases
        fetch_command = "mysql -u root -e 'SHOW DATABASES;'"
        fetch_output = gradinglib.execute_vm_command(vm, guest_username, guest_password, fetch_command, content, "/bin/bash")
        
        # Check if 'wikidb' is in the list of databases
        if "wikidb" in fetch_output:
            logger.info(f"SUCCESS! {vm.name} has the 'wikidb' database.")
        else:
            logger.warn(f"FAILED! {vm.name} does not have the 'wikidb' database.")
    except vim.fault.GuestOperationsUnavailable as e:
        logger.warn(f"FAILED! {vm.name} in {vm.parent.name} failed. Guest operations unavailable.")
        return
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return

