import gradinglib
from logger import logger
from pyVmomi import vim

def check_adadmin_user(vm: vim.VirtualMachine, content: vim.ServiceInstanceContent):
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


def check_ad(vm: vim.VirtualMachine, content: vim.ServiceInstanceContent):
    logger.debug(f"Running AD checks for {vm.name}...")
    check_adadmin_user(vm, content)