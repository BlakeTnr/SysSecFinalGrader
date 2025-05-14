import pytest
import re
import gradinglib

def test_ipconfig_regex():
    output = """
em0: flags=1008843<UP,BROADCAST,RUNNING,SIMPLEX,MULTICAST,LOWER_UP> metric 0 mtu 1500
        description: WAN
        options=4e100bb<RXCSUM,TXCSUM,VLAN_MTU,VLAN_HWTAGGING,JUMBO_MTU,VLAN_HWCSUM,VLAN_HWFILTER,RXCSUM_IPV6,TXCSUM_IPV6,HWSTATS,MEXTPG>
        ether 00:50:56:86:f0:f5
        inet 192.168.254.127 netmask 0xffffff00 broadcast 192.168.254.255
        inet6 fe80::250:56ff:fe86:f0f5%em0 prefixlen 64 scopeid 0x1
        media: Ethernet autoselect (1000baseT <full-duplex>)
        status: active
        nd6 options=21<PERFORMNUD,AUTO_LINKLOCAL>
    """

    regex = "(?<=inet 192.168.254.)\d\d\d"
    match = re.findall(regex, output)[0]
    answer = match
    assert answer == "127"

def test_ipconfig_third_octet_regex():
    output = """
em0: flags=1008843<UP,BROADCAST,RUNNING,SIMPLEX,MULTICAST,LOWER_UP> metric 0 mtu 1500
        description: WAN
        options=4e100bb<RXCSUM,TXCSUM,VLAN_MTU,VLAN_HWTAGGING,JUMBO_MTU,VLAN_HWCSUM,VLAN_HWFILTER,RXCSUM_IPV6,TXCSUM_IPV6,HWSTATS,MEXTPG>
        ether 00:50:56:86:f0:f5
        inet 192.168.10.0 netmask 0xffffff00 broadcast 192.168.254.255
        inet6 fe80::250:56ff:fe86:f0f5%em0 prefixlen 64 scopeid 0x1
        media: Ethernet autoselect (1000baseT <full-duplex>)
        status: active
        nd6 options=21<PERFORMNUD,AUTO_LINKLOCAL>
    """

    regex = "(?<=inet 192.168.)\d*(?=.0)"
    match = re.findall(regex, output)[0]
    answer = match
    assert answer == "10"

def test_team_name_to_number():
    test1 = "Team_01"
    intmatch = gradinglib.team_name_to_number(test1)
    assert intmatch == 1

    test2 = "Team_33"
    intmatch = gradinglib.team_name_to_number(test2)
    assert intmatch == 33

def test_windows_adadmin_exists():
    output = """
User name                    Blake
Full Name                    Blake Turner
Comment
User's comment
Country/region code          000 (System Default)
Account active               Yes
Account expires              Never

Password last set            9/6/2024 10:15:40 AM
Password expires             Never
Password changeable          9/6/2024 10:15:40 AM
Password required            No
User may change password     Yes

Workstations allowed         All
Logon script
User profile
Home directory
Last logon                   9/6/2024 10:15:39 AM

Logon hours allowed          All

Local Group Memberships      *Administrators       *docker-users
Global Group memberships     *None
The command completed successfully.
    """

    regex = "not be found"

    match = re.findall(regex, output)
    assert len(match) == 0

def test_windows_adadmin_not_exists():
    output = """
The user name could not be found.

More help is available by typing NET HELPMSG 2221.
    """

    regex = "not be found"

    match = re.findall(regex, output)
    assert len(match) == 1

def test_windows_domain_name():
    test = """
Domain Name
catflix04.local
    """
    regex = "Domain\s+catflix(\d{2})\.local"
    match = re.findall(regex, test)
    assert len(match) == 1
    assert match[0] == "04"

def test_windows_domain_name_wrong():
    test = """
Domain Name
dogflix01.local
    """
    regex = "Domain\s+catflix(\d{2})\.local"
    match = re.findall(regex, test)
    assert len(match) == 0
