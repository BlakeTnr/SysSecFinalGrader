import gradinglib
from pyVmomi import vim
from logger import logger
import re

def check_public_ip(vm: vim.VirtualMachine, content: vim.ServiceInstanceContent):
    guest_username, guest_password = gradinglib.get_vm_creds(vm)
    gradinglib.power_on_vm(vm)
    gradinglib.vm_execute_firewalloff_command(vm, guest_username, guest_password, content)

    try:
        output = gradinglib.execute_vm_command(vm, guest_username, guest_password, "ifconfig em0", content, "/bin/sh")
        regex = "(?<=inet 192.168.254.)\d\d\d"
        match = re.findall(regex, output)[0]
        teamname = vm.parent.name
        teamnumber = gradinglib.team_name_to_number(teamname)
        pfsensepublic = 100 + teamnumber;
        
        if(pfsensepublic == match):
            logger.info(f"SUCCESS! {vm.name} in {vm.parent.name} passed. Public IP is correct.")
        else:
            logger.warn(f"FAILED! {vm.name} in {vm.parent.name} failed. Public IP is incorrect.")
        

        print(output)
    except vim.fault.GuestOperationsUnavailable as e:
        logger.warn(f"FAILED! {vm.name} in {vm.parent.name} failed. Guest operations unavailable.")

def check_adminnet_ip(vm: vim.VirtualMachine, content: vim.ServiceInstanceContent):
    guest_username, guest_password = gradinglib.get_vm_creds(vm)
    gradinglib.power_on_vm(vm)
    gradinglib.vm_execute_firewalloff_command(vm, guest_username, guest_password, content)

    try:
        output = gradinglib.execute_vm_command(vm, guest_username, guest_password, "ifconfig em1", content, "/bin/sh")
        regex = "(?<=inet 10.42.)\d*(?=.0)"
        match = re.findall(regex, output)[0]
        teamname = vm.parent.name
        teamnumber = gradinglib.team_name_to_number(teamname)
        
        if(teamnumber == match):
            logger.info(f"SUCCESS! {vm.name} in {vm.parent.name} passed. ADMINNET is correct.")
        else:
            logger.warn(f"FAILED! {vm.name} in {vm.parent.name} failed. ADMINNET is incorrect.")
        

        print(output)
    except vim.fault.GuestOperationsUnavailable as e:
        logger.warn(f"FAILED! {vm.name} in {vm.parent.name} failed. Guest operations unavailable.")

def check_servernet_ip(vm: vim.VirtualMachine, content: vim.ServiceInstanceContent):
    guest_username, guest_password = gradinglib.get_vm_creds(vm)
    gradinglib.power_on_vm(vm)
    gradinglib.vm_execute_firewalloff_command(vm, guest_username, guest_password, content)

    try:
        output = gradinglib.execute_vm_command(vm, guest_username, guest_password, "ifconfig em2", content, "/bin/sh")
        regex = "(?<=inet 10.43.)\d*(?=.0)"
        match = re.findall(regex, output)[0]
        teamname = vm.parent.name
        teamnumber = gradinglib.team_name_to_number(teamname)
        
        if(teamnumber == match):
            logger.info(f"SUCCESS! {vm.name} in {vm.parent.name} passed. SERVERNET is correct.")
        else:
            logger.warn(f"FAILED! {vm.name} in {vm.parent.name} failed. SERVERNET is incorrect.")
        

        print(output)
    except vim.fault.GuestOperationsUnavailable as e:
        logger.warn(f"FAILED! {vm.name} in {vm.parent.name} failed. Guest operations unavailable.")

def check_pfsense(vm: vim.VirtualMachine, content: vim.ServiceInstanceContent):
    logger.debug(f"Running pfsense checks for {vm.name}...")
    check_public_ip(vm, content)
    check_adminnet_ip(vm, content)
    check_servernet_ip(vm, content)