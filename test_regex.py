import pytest
import re

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