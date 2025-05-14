import gradinglib
from logger import logger
from pyVmomi import vim

def check_adadmin_exists(vm: vim.VirtualMachine, content: vim.ServiceInstanceContent):
    guest_username, guest_password = gradinglib.get_vm_creds(vm)

    try:
        output = gradinglib.execute_vm_command(vm, guest_username, guest_password, "get-gporeport -all -ReportType xml", content, "powershell")
        regex = """<q1:Policy>
          <q1:Name>Desktop Wallpaper</q1:Name>
          <q1:State>Enabled</q1:State>"""
        match = regex.findall(output)

        if len(match) == 1:
            logger.info(f"SUCCESS! {vm.name} in {vm.parent.name} passed. Background GPO exists.")
        else:
            logger.warn(f"FAILED! {vm.name} in {vm.parent.name} failed. Background GPO does not exist.")

    except vim.fault.GuestOperationsUnavailable as e:
        logger.warn(f"FAILED! {vm.name} in {vm.parent.name} failed. Guest operations unavailable.")
        return