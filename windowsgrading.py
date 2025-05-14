import gradinglib
from logger import logger
from pyVmomi import vim

def check_adadmin_exists(vm: vim.VirtualMachine, content: vim.ServiceInstanceContent):
    guest_username, guest_password = gradinglib.get_vm_creds(vm)

    try:
        output = gradinglib.execute_vm_command(vm, guest_username, guest_password, "net user ADAdmin", content, "powershell")
        regex = "not be found"
        match = regex.findall(output)

        if len(match) == 0:
            logger.info(f"SUCCESS! {vm.name} in {vm.parent.name} passed. ADAdmin user exists.")
        else:
            logger.warn(f"FAILED! {vm.name} in {vm.parent.name} failed. ADAdmin user does not exist.")

    except vim.fault.GuestOperationsUnavailable as e:
        logger.warn(f"FAILED! {vm.name} in {vm.parent.name} failed. Guest operations unavailable.")
        return

def check_adadmin_in_secdev(vm: vim.VirtualMachine, content: vim.ServiceInstanceContent):
    guest_username, guest_password = gradinglib.get_vm_creds(vm)

    try:
        output = gradinglib.execute_vm_command(vm, guest_username, guest_password, "net user ADAdmin", content, "powershell")
        regex = "SecDev"
        match = regex.findall(output)

        if len(match) == 1:
            logger.info(f"SUCCESS! {vm.name} in {vm.parent.name} passed. ADAdmin is in SecDev.")
        else:
            logger.warn(f"FAILED! {vm.name} in {vm.parent.name} failed. ADAdmin is in SecDev.")

    except vim.fault.GuestOperationsUnavailable as e:
        logger.warn(f"FAILED! {vm.name} in {vm.parent.name} failed. Guest operations unavailable.")
        return

def check_ad(vm: vim.VirtualMachine, content: vim.ServiceInstanceContent):
    logger.debug(f"Running AD checks for {vm.name}...")
    check_adadmin_exists(vm, content)
    check_adadmin_in_secdev(vm, content)