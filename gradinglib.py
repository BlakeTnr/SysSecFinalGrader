from enum import Enum
import random
import ssl
import atexit
import time
from typing import List
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import re

def search_folder(folder, folder_name):
    for child in folder.childEntity:
        if isinstance(child, vim.Folder) and child.name == folder_name:
            return child
        elif isinstance(child, vim.Folder):
            print()
            found_folder = search_folder(child, folder_name)
            if found_folder:
                return found_folder

def get_folder_by_name(si, folder_name):
    """
    Retrieve a folder by its name using pyVmomi.

    :param si: ServiceInstance object connected to vCenter
    :param folder_name: Name of the folder to retrieve
    :return: Folder object if found, otherwise None
    """
    content = si.RetrieveContent()
    root_folder = content.rootFolder

    datacenter = root_folder.childEntity[0];
    vmFolder = datacenter.vmFolder
    
    return search_folder(vmFolder, folder_name);

def get_folder_by_name(folder, folder_name):
    for child in folder.childEntity:
        if(isinstance(child, vim.Folder) and child.name == folder_name):
            return child
        
    raise Exception(f"Folder '{folder_name}' not found.")

def get_folder_by_path(si, path):
    """
    Retrieve a folder by its path using pyVmomi.

    :param si: ServiceInstance object connected to vCenter
    :param path: Path of the folder to retrieve (e.g., 'Datacenter/vm/FolderName')
    :return: Folder object if found, otherwise None
    """
    path_parts = path.split('/')
    
    content = si.RetrieveContent()
    root_folder = content.rootFolder

    datacenter = root_folder.childEntity[0];
    vmFolder = datacenter.vmFolder

    currentFolder = vmFolder
    for i in range(len(path_parts)):
        currentFolder = get_folder_by_name(currentFolder, path_parts[i])

    return currentFolder

def get_vm_by_name(folder, vm_name):
    for child in folder.childEntity:
        if(child.name == vm_name):
            return child
        
    raise Exception(f"VM '{vm_name}' not found.")

def get_folders_by_regex(folder: vim.Folder, regex: str):
    """
    only retrives 1st level children
    """

    regex = re.compile(regex)

    folder_list = []
    for child in folder.childEntity:
        if isinstance(child, vim.Folder) and regex.match(child.name):
            folder_list.append(child)

    return folder_list

def get_vm_by_regex(folders: List[vim.Folder], regex: str):
    """
    only retrives 1st level children
    """

    regex = re.compile(regex)
    vm_list = []

    for folder in folders:
        for child in folder.childEntity:
            if isinstance(child, vim.VirtualMachine) and regex.match(child.name):
                vm_list.append(child)

    return vm_list

def execute_vm_command(vm: vim.VirtualMachine, guest_username: str, guest_password: str, command: str, content: vim.ServiceContent, shell_path: str):
    if vm is None:
        raise Exception(f"VM '{vm_name}' not found.")

    # --- Guest Ops Manager ---
    guest_ops_mgr = content.guestOperationsManager

    # --- Auth to Guest ---
    cred = vim.vm.guest.NamePasswordAuthentication(username=guest_username, password=guest_password)
    guest_ops = content.guestOperationsManager

    # --- Prepare Program Spec ---
    output_file_path = "/tmp/output.txt"
    program_spec = vim.vm.guest.ProcessManager.ProgramSpec(
        programPath=f"{shell_path}",
        arguments=f'-c "{command} > {output_file_path}"'
    )

    # --- Run the program ---
    pm = guest_ops_mgr.processManager
    pid = pm.StartProgramInGuest(vm, cred, program_spec)

    # print(f"Started process with PID: {pid}")

    # --- Wait briefly to ensure the file is written ---
    time.sleep(2)

    # --- Read the file content from the VM ---
    file_manager = guest_ops.fileManager

    # Initiate file transfer from guest
    file_transfer_info = file_manager.InitiateFileTransferFromGuest(vm, cred, output_file_path)

    import urllib.request

    # Download the file from the transfer URL
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    response = urllib.request.urlopen(file_transfer_info.url, context=ctx)
    file_content = response.read().decode()

    return file_content

def test_vm_execute_command(vm: vim.VirtualMachine, guest_username: str, guest_password: str, content: vim.ServiceContent):
    randint = random.randint(1, 1000)

    try:
        output = execute_vm_command(vm, guest_username, guest_password, f"echo {randint}", content, "/bin/bash")

        if(output != f"{randint}\n"):
            print(f"FAILED! {vm.name} in {vm.parent.name} failed to write correct number");
        else:
            print(f"PASSED! {vm.name} in {vm.parent.name} passed execute command check");
    except vim.fault.GuestOperationsUnavailable as e:
        print(f"FAILED! {vm.name} in {vm.parent.name} failed. Guest operations unavailable." );
    except vim.fault.InvalidGuestLogin as e:
        print(f"FAILED! {vm.name} in {vm.parent.name} failed. Invalid guest login." );
    except Exception as e:
        print(f"FAILED! {vm.name} in {vm.parent.name} failed. {e}" );

def get_vm_secret_logging_code(vm: vim.VirtualMachine):
    name = vm.name

    if name == "GraylogServer":
        return "GwayWogSwerver"
    elif name == "pfSenseRouter":
        return "PeFSwenseWouter"
    elif name == "RockyDB":
        return "WockyDB"
    elif name == "UbuntuClient":
        return "UwuntuWebCwient"
    elif name == "UbuntuWebServer":
        return "UwutuntuWebSewver"
    
    return "nocode"

def vm_execute_firewalloff_command(vm: vim.VirtualMachine, guest_username: str, guest_password: str, content: vim.ServiceContent):
    randint = random.randint(1, 1000)

    try:
        output = execute_vm_command(vm, guest_username, guest_password, f"pfctl -d", content, "/bin/sh")
        print(f"PASSED! {vm.name} in {vm.parent.name} didn't error executing 'pfctl -d' command");
    except vim.fault.GuestOperationsUnavailable as e:
        print(f"FAILED! {vm.name} in {vm.parent.name} failed. Guest operations unavailable." );
    except vim.fault.InvalidGuestLogin as e:
        print(f"FAILED! {vm.name} in {vm.parent.name} failed. Invalid guest login." );
    except Exception as e:
        print(f"FAILED! {vm.name} in {vm.parent.name} failed. {e}" );

def power_on_vm(vm: vim.VirtualMachine):
    """
    Power on a VM using pyVmomi.

    :param vm: VirtualMachine object
    """
    if vm is None:
        raise Exception(f"VM not found.")

    # --- Power on the VM ---
    try:
        print(f"Powering on {vm.name}...")
        task = vm.PowerOn()
        task.Wait()
        print(f"{vm.name} powered on successfully.")
    except vim.fault.InvalidPowerState as e:
        print(f"VM '{vm.name}' is already powered on.")
    except Exception as e:
        print(f"Failed to power on VM '{vm.name}': {e}")

def vm_execute_logger_command(vm: vim.VirtualMachine, guest_username: str, guest_password: str, content: vim.ServiceContent):
    randint = random.randint(1, 1000)

    os = get_vm_os(vm)
    secret_logging_code = get_vm_secret_logging_code(vm)

    try:
        if os == OS.WINDOWS:
            output = execute_vm_command(vm, guest_username, guest_password, f"logger {secret_logging_code}", content, "/bin/bash")
        elif os == OS.LINUX:
            output = execute_vm_command(vm, guest_username, guest_password, f"logger {secret_logging_code}", content, "/bin/bash")
        elif os == OS.FREEBSD:
            output = execute_vm_command(vm, guest_username, guest_password, f"logger {secret_logging_code}", content, "/bin/sh")
        print(f"PASSED! {vm.name} in {vm.parent.name} didn't error");
    except vim.fault.GuestOperationsUnavailable as e:
        print(f"FAILED! {vm.name} in {vm.parent.name} failed. Guest operations unavailable." );
    except vim.fault.InvalidGuestLogin as e:
        print(f"FAILED! {vm.name} in {vm.parent.name} failed. Invalid guest login." );
    except Exception as e:
        print(f"FAILED! {vm.name} in {vm.parent.name} failed. {e}" );

class OS(Enum):
    WINDOWS=1
    LINUX=2
    FREEBSD=3
    OTHER=4

def get_vm_os(vm: vim.VirtualMachine):
    """
    Retrieve the guest OS type from the VM's config.
    """
    if vm is None:
        raise Exception(f"VM '{vm_name}' not found.")

    # --- Get Guest Info ---
    guest_info = vm.config.guestFullName

    # --- Determine OS Type ---
    if "Windows" in guest_info:
        return OS.WINDOWS
    elif "Linux" in guest_info:
        return OS.LINUX
    elif "FreeBSD" in guest_info:
        return OS.FREEBSD
    else:
        return OS.OTHER

def get_vm_creds(vm: vim.VirtualMachine):
    """
    Retrieve the guest username and password from the VM's config.
    """
    if vm is None:
        raise Exception(f"VM '{vm_name}' not found.")

    vm_os = get_vm_os(vm)

    guest_username = "sysadmin"
    guest_password = "Change.me!"

    if vm_os == OS.WINDOWS:
        guest_username = "Administrator"
        guest_password = "Change.me!"
    elif vm_os == OS.LINUX:
        guest_username = "sysadmin"
        guest_password = "Change.me!"
    elif vm_os == OS.FREEBSD:
        guest_username = "admin"
        guest_password = "pfsense"

    # --- Return the credentials ---
    return guest_username, guest_password
