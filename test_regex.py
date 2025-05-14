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


def test_windows_gpo_for_background():
    regex = """<q1:Policy>
          <q1:Name>Desktop Wallpaper</q1:Name>
          <q1:State>Enabled</q1:State>"""
    
    testgpo = re.findall(regex, wingpo_for_background)
    
    assert len(testgpo) == 1

def test_windows_gpo_for_not_background():
    regex = """<q1:Policy>
          <q1:Name>Desktop Wallpaper</q1:Name>
          <q1:State>Enabled</q1:State>"""
    
    testgpo = re.findall(regex, test_gpo_not_background)
    
    assert len(testgpo) == 0


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

wingpo_for_background = """
<?xml version="1.0" encoding="utf-16"?>
<GPO xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.microsoft.com/GroupPolicy/Settings">
  <Identifier>
    <Identifier xmlns="http://www.microsoft.com/GroupPolicy/Types">{9b074ed5-63dc-4c34-be43-272b3bd1f32d}</Identifier>
    <Domain xmlns="http://www.microsoft.com/GroupPolicy/Types">catflix01.local</Domain>
  </Identifier>
  <Name>picpolicy</Name>
  <IncludeComments>true</IncludeComments>
  <CreatedTime>2025-04-28T22:53:26</CreatedTime>
  <ModifiedTime>2025-04-29T21:26:28</ModifiedTime>
  <ReadTime>2025-05-14T00:30:25.5924982Z</ReadTime>
  <SecurityDescriptor>
    <SDDL xmlns="http://www.microsoft.com/GroupPolicy/Types/Security">O:DAG:DAD:PAI(OA;CI;CR;edacfd8f-ffb3-11d1-b41d-00a0c968f939;;DU)(OA;CI;CR;edacfd8f-ffb3-11d1-b41d-00a0c968f939;;WD)(OA;CI;CR;edacfd8f-ffb3-11d1-b41d-00a0c968f939;;AU)(A;;CCDCLCSWRPWPDTLOSDRCWDWO;;;DA)(A;CI;LCRPRC;;;DU)(A;CI;CCDCLCSWRPWPDTLOSDRCWDWO;;;DA)(A;CI;CCDCLCSWRPWPDTLOSDRCWDWO;;;S-1-5-21-4090698675-1526931094-3048149747-519)(A;CI;LCRPRC;;;WD)(A;CI;LCRPLORC;;;ED)(A;CI;LCRPLORC;;;AU)(A;CI;CCDCLCSWRPWPDTLOSDRCWDWO;;;SY)(A;CIIO;CCDCLCSWRPWPDTLOSDRCWDWO;;;CO)S:AI(OU;CIIDSA;WPWD;;f30e3bc2-9ff0-11d1-b603-0000f80367c1;WD)(OU;CIIOIDSA;WP;f30e3bbe-9ff0-11d1-b603-0000f80367c1;bf967aa5-0de6-11d0-a285-00aa003049e2;WD)(OU;CIIOIDSA;WP;f30e3bbf-9ff0-11d1-b603-0000f80367c1;bf967aa5-0de6-11d0-a285-00aa003049e2;WD)</SDDL>
    <Owner xmlns="http://www.microsoft.com/GroupPolicy/Types/Security">
      <SID xmlns="http://www.microsoft.com/GroupPolicy/Types">S-1-5-21-4090698675-1526931094-3048149747-512</SID>
      <Name xmlns="http://www.microsoft.com/GroupPolicy/Types">CATFLIX01\Domain Admins</Name>
    </Owner>
    <Group xmlns="http://www.microsoft.com/GroupPolicy/Types/Security">
      <SID xmlns="http://www.microsoft.com/GroupPolicy/Types">S-1-5-21-4090698675-1526931094-3048149747-512</SID>
      <Name xmlns="http://www.microsoft.com/GroupPolicy/Types">CATFLIX01\Domain Admins</Name>
    </Group>
    <PermissionsPresent xmlns="http://www.microsoft.com/GroupPolicy/Types/Security">true</PermissionsPresent>
    <Permissions xmlns="http://www.microsoft.com/GroupPolicy/Types/Security">
      <InheritsFromParent>false</InheritsFromParent>
      <TrusteePermissions>
        <Trustee>
          <SID xmlns="http://www.microsoft.com/GroupPolicy/Types">S-1-5-21-4090698675-1526931094-3048149747-513</SID>
          <Name xmlns="http://www.microsoft.com/GroupPolicy/Types">CATFLIX01\Domain Users</Name>
        </Trustee>
        <Type xsi:type="PermissionType">
          <PermissionType>Allow</PermissionType>
        </Type>
        <Inherited>false</Inherited>
        <Applicability>
          <ToSelf>true</ToSelf>
          <ToDescendantObjects>false</ToDescendantObjects>
          <ToDescendantContainers>true</ToDescendantContainers>
          <ToDirectDescendantsOnly>false</ToDirectDescendantsOnly>
        </Applicability>
        <Standard>
          <GPOGroupedAccessEnum>Apply Group Policy</GPOGroupedAccessEnum>
        </Standard>
        <AccessMask>0</AccessMask>
      </TrusteePermissions>
      <TrusteePermissions>
        <Trustee>
          <SID xmlns="http://www.microsoft.com/GroupPolicy/Types">S-1-1-0</SID>
          <Name xmlns="http://www.microsoft.com/GroupPolicy/Types">Everyone</Name>
        </Trustee>
        <Type xsi:type="PermissionType">
          <PermissionType>Allow</PermissionType>
        </Type>
        <Inherited>false</Inherited>
        <Applicability>
          <ToSelf>true</ToSelf>
          <ToDescendantObjects>false</ToDescendantObjects>
          <ToDescendantContainers>true</ToDescendantContainers>
          <ToDirectDescendantsOnly>false</ToDirectDescendantsOnly>
        </Applicability>
        <Standard>
          <GPOGroupedAccessEnum>Apply Group Policy</GPOGroupedAccessEnum>
        </Standard>
        <AccessMask>0</AccessMask>
      </TrusteePermissions>
      <TrusteePermissions>
        <Trustee>
          <SID xmlns="http://www.microsoft.com/GroupPolicy/Types">S-1-5-9</SID>
          <Name xmlns="http://www.microsoft.com/GroupPolicy/Types">NT AUTHORITY\ENTERPRISE DOMAIN CONTROLLERS</Name>
        </Trustee>
        <Type xsi:type="PermissionType">
          <PermissionType>Allow</PermissionType>
        </Type>
        <Inherited>false</Inherited>
        <Applicability>
          <ToSelf>true</ToSelf>
          <ToDescendantObjects>false</ToDescendantObjects>
          <ToDescendantContainers>true</ToDescendantContainers>
          <ToDirectDescendantsOnly>false</ToDirectDescendantsOnly>
        </Applicability>
        <Standard>
          <GPOGroupedAccessEnum>Read</GPOGroupedAccessEnum>
        </Standard>
        <AccessMask>0</AccessMask>
      </TrusteePermissions>
      <TrusteePermissions>
        <Trustee>
          <SID xmlns="http://www.microsoft.com/GroupPolicy/Types">S-1-5-21-4090698675-1526931094-3048149747-519</SID>
          <Name xmlns="http://www.microsoft.com/GroupPolicy/Types">CATFLIX01\Enterprise Admins</Name>
        </Trustee>
        <Type xsi:type="PermissionType">
          <PermissionType>Allow</PermissionType>
        </Type>
        <Inherited>false</Inherited>
        <Applicability>
          <ToSelf>true</ToSelf>
          <ToDescendantObjects>false</ToDescendantObjects>
          <ToDescendantContainers>true</ToDescendantContainers>
          <ToDirectDescendantsOnly>false</ToDirectDescendantsOnly>
        </Applicability>
        <Standard>
          <GPOGroupedAccessEnum>Edit, delete, modify security</GPOGroupedAccessEnum>
        </Standard>
        <AccessMask>0</AccessMask>
      </TrusteePermissions>
      <TrusteePermissions>
        <Trustee>
          <SID xmlns="http://www.microsoft.com/GroupPolicy/Types">S-1-5-18</SID>
          <Name xmlns="http://www.microsoft.com/GroupPolicy/Types">NT AUTHORITY\SYSTEM</Name>
        </Trustee>
        <Type xsi:type="PermissionType">
          <PermissionType>Allow</PermissionType>
        </Type>
        <Inherited>false</Inherited>
        <Applicability>
          <ToSelf>true</ToSelf>
          <ToDescendantObjects>false</ToDescendantObjects>
          <ToDescendantContainers>true</ToDescendantContainers>
          <ToDirectDescendantsOnly>false</ToDirectDescendantsOnly>
        </Applicability>
        <Standard>
          <GPOGroupedAccessEnum>Edit, delete, modify security</GPOGroupedAccessEnum>
        </Standard>
        <AccessMask>0</AccessMask>
      </TrusteePermissions>
      <TrusteePermissions>
        <Trustee>
          <SID xmlns="http://www.microsoft.com/GroupPolicy/Types">S-1-5-21-4090698675-1526931094-3048149747-512</SID>
          <Name xmlns="http://www.microsoft.com/GroupPolicy/Types">CATFLIX01\Domain Admins</Name>
        </Trustee>
        <Type xsi:type="PermissionType">
          <PermissionType>Allow</PermissionType>
        </Type>
        <Inherited>false</Inherited>
        <Applicability>
          <ToSelf>true</ToSelf>
          <ToDescendantObjects>false</ToDescendantObjects>
          <ToDescendantContainers>true</ToDescendantContainers>
          <ToDirectDescendantsOnly>false</ToDirectDescendantsOnly>
        </Applicability>
        <Standard>
          <GPOGroupedAccessEnum>Edit, delete, modify security</GPOGroupedAccessEnum>
        </Standard>
        <AccessMask>0</AccessMask>
      </TrusteePermissions>
      <TrusteePermissions>
        <Trustee>
          <SID xmlns="http://www.microsoft.com/GroupPolicy/Types">S-1-5-11</SID>
          <Name xmlns="http://www.microsoft.com/GroupPolicy/Types">NT AUTHORITY\Authenticated Users</Name>
        </Trustee>
        <Type xsi:type="PermissionType">
          <PermissionType>Allow</PermissionType>
        </Type>
        <Inherited>false</Inherited>
        <Applicability>
          <ToSelf>true</ToSelf>
          <ToDescendantObjects>false</ToDescendantObjects>
          <ToDescendantContainers>true</ToDescendantContainers>
          <ToDirectDescendantsOnly>false</ToDirectDescendantsOnly>
        </Applicability>
        <Standard>
          <GPOGroupedAccessEnum>Apply Group Policy</GPOGroupedAccessEnum>
        </Standard>
        <AccessMask>0</AccessMask>
      </TrusteePermissions>
    </Permissions>
    <AuditingPresent xmlns="http://www.microsoft.com/GroupPolicy/Types/Security">false</AuditingPresent>
  </SecurityDescriptor>
  <FilterDataAvailable>true</FilterDataAvailable>
  <Computer>
    <VersionDirectory>0</VersionDirectory>
    <VersionSysvol>0</VersionSysvol>
    <Enabled>true</Enabled>
  </Computer>
  <User>
    <VersionDirectory>6</VersionDirectory>
    <VersionSysvol>6</VersionSysvol>
    <Enabled>true</Enabled>
    <ExtensionData>
      <Extension xmlns:q1="http://www.microsoft.com/GroupPolicy/Settings/Registry" xsi:type="q1:RegistrySettings">
        <q1:Policy>
          <q1:Name>Desktop Wallpaper</q1:Name>
          <q1:State>Enabled</q1:State>
          <q1:Explain>Specifies the desktop background ("wallpaper") displayed on all users' desktops.

This setting lets you specify the wallpaper on users' desktops and prevents users from changing the image or its presentation. The wallpaper you specify can be stored in a bitmap (*.bmp) or JPEG (*.jpg) file.

To use this setting, type the fully qualified path and name of the file that stores the wallpaper image. You can type a local path, such as C:\Windows\web\wallpaper\home.jpg or a UNC path, such as \\Server\Share\Corp.jpg. If the specified file is not available when the user logs on, no wallpaper is displayed. Users cannot specify alternative wallpaper. You can also use this setting to specify that the wallpaper image be centered, tiled, or stretched. Users cannot change this specification.

If you disable this setting or do not configure it, no wallpaper is displayed. However, users can select the wallpaper of their choice.

Also, see the "Allow only bitmapped wallpaper" in the same location, and the "Prevent changing wallpaper" setting in User Configuration\Administrative Templates\Control Panel.

Note: This setting does not apply to remote desktop server sessions.</q1:Explain>
          <q1:Supported>At least Windows 2000</q1:Supported>
          <q1:Category>Desktop/Desktop</q1:Category>
          <q1:EditText>
            <q1:Name>Wallpaper Name:</q1:Name>
            <q1:State>Enabled</q1:State>
            <q1:Value>\\WIN-U1ARDQM9MEV.catflix01.local\thesharedfolder\catflix.png</q1:Value>
          </q1:EditText>
          <q1:Text>
            <q1:Name>Example: Using a local path:   C:\windows\web\wallpaper\home.jpg</q1:Name>
          </q1:Text>
          <q1:Text>
            <q1:Name>Example: Using a UNC path:     \\Server\Share\Corp.jpg</q1:Name>
          </q1:Text>
          <q1:DropDownList>
            <q1:Name>Wallpaper Style:</q1:Name>
            <q1:State>Enabled</q1:State>
            <q1:Value>
              <q1:Name>Fit</q1:Name>
            </q1:Value>
          </q1:DropDownList>
        </q1:Policy>
        <q1:Blocked>false</q1:Blocked>
      </Extension>
      <Name>Registry</Name>
    </ExtensionData>
  </User>
  <LinksTo>
    <SOMName>catflix01</SOMName>
    <SOMPath>catflix01.local</SOMPath>
    <Enabled>true</Enabled>
    <NoOverride>true</NoOverride>
  </LinksTo>
</GPO>
"""

test_gpo_not_background = """
<?xml version="1.0" encoding="utf-16"?>
<GPO xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.microsoft.com/GroupPolicy/Settings">
  <Identifier>
    <Identifier xmlns="http://www.microsoft.com/GroupPolicy/Types">{31b2f340-016d-11d2-945f-00c04fb984f9}</Identifier>
    <Domain xmlns="http://www.microsoft.com/GroupPolicy/Types">catflix01.local</Domain>
  </Identifier>
  <Name>Default Domain Policy</Name>
  <IncludeComments>true</IncludeComments>
  <CreatedTime>2025-04-28T22:35:12</CreatedTime>
  <ModifiedTime>2025-04-28T22:39:14</ModifiedTime>
  <ReadTime>2025-05-14T03:00:22.7963389Z</ReadTime>
  <SecurityDescriptor>
    <SDDL xmlns="http://www.microsoft.com/GroupPolicy/Types/Security">O:DAG:DAD:PAI(A;;CCLCSWRPWPLORCWDWO;;;DA)(A;CIIO;CCDCLCSWRPWPDTLOSDRCWDWO;;;DA)(A;;CCLCSWRPWPLORCWDWO;;;S-1-5-21-4090698675-1526931094-3048149747-519)(A;CIIO;CCDCLCSWRPWPDTLOSDRCWDWO;;;S-1-5-21-4090698675-1526931094-3048149747-519)(A;;CCLCSWRPWPLORCWDWO;;;DA)(A;CIIO;CCDCLCSWRPWPDTLOSDRCWDWO;;;CO)(A;CI;CCDCLCSWRPWPDTLOSDRCWDWO;;;SY)(A;CI;LCRPLORC;;;AU)(OA;CI;CR;edacfd8f-ffb3-11d1-b41d-00a0c968f939;;AU)(A;CI;LCRPLORC;;;ED)S:AI(OU;CIIDSA;WPWD;;f30e3bc2-9ff0-11d1-b603-0000f80367c1;WD)(OU;CIIOIDSA;WP;f30e3bbe-9ff0-11d1-b603-0000f80367c1;bf967aa5-0de6-11d0-a285-00aa003049e2;WD)(OU;CIIOIDSA;WP;f30e3bbf-9ff0-11d1-b603-0000f80367c1;bf967aa5-0de6-11d0-a285-00aa003049e2;WD)</SDDL>
    <Owner xmlns="http://www.microsoft.com/GroupPolicy/Types/Security">
      <SID xmlns="http://www.microsoft.com/GroupPolicy/Types">S-1-5-21-4090698675-1526931094-3048149747-512</SID>
      <Name xmlns="http://www.microsoft.com/GroupPolicy/Types">CATFLIX01\Domain Admins</Name>
    </Owner>
    <Group xmlns="http://www.microsoft.com/GroupPolicy/Types/Security">
      <SID xmlns="http://www.microsoft.com/GroupPolicy/Types">S-1-5-21-4090698675-1526931094-3048149747-512</SID>
      <Name xmlns="http://www.microsoft.com/GroupPolicy/Types">CATFLIX01\Domain Admins</Name>
    </Group>
    <PermissionsPresent xmlns="http://www.microsoft.com/GroupPolicy/Types/Security">true</PermissionsPresent>
    <Permissions xmlns="http://www.microsoft.com/GroupPolicy/Types/Security">
      <InheritsFromParent>false</InheritsFromParent>
      <TrusteePermissions>
        <Trustee>
          <SID xmlns="http://www.microsoft.com/GroupPolicy/Types">S-1-5-9</SID>
          <Name xmlns="http://www.microsoft.com/GroupPolicy/Types">NT AUTHORITY\ENTERPRISE DOMAIN CONTROLLERS</Name>
        </Trustee>
        <Type xsi:type="PermissionType">
          <PermissionType>Allow</PermissionType>
        </Type>
        <Inherited>false</Inherited>
        <Applicability>
          <ToSelf>true</ToSelf>
          <ToDescendantObjects>false</ToDescendantObjects>
          <ToDescendantContainers>true</ToDescendantContainers>
          <ToDirectDescendantsOnly>false</ToDirectDescendantsOnly>
        </Applicability>
        <Standard>
          <GPOGroupedAccessEnum>Read</GPOGroupedAccessEnum>
        </Standard>
        <AccessMask>0</AccessMask>
      </TrusteePermissions>
      <TrusteePermissions>
        <Trustee>
          <SID xmlns="http://www.microsoft.com/GroupPolicy/Types">S-1-5-18</SID>
          <Name xmlns="http://www.microsoft.com/GroupPolicy/Types">NT AUTHORITY\SYSTEM</Name>
        </Trustee>
        <Type xsi:type="PermissionType">
          <PermissionType>Allow</PermissionType>
        </Type>
        <Inherited>false</Inherited>
        <Applicability>
          <ToSelf>true</ToSelf>
          <ToDescendantObjects>false</ToDescendantObjects>
          <ToDescendantContainers>true</ToDescendantContainers>
          <ToDirectDescendantsOnly>false</ToDirectDescendantsOnly>
        </Applicability>
        <Standard>
          <GPOGroupedAccessEnum>Edit, delete, modify security</GPOGroupedAccessEnum>
        </Standard>
        <AccessMask>0</AccessMask>
      </TrusteePermissions>
      <TrusteePermissions>
        <Trustee>
          <SID xmlns="http://www.microsoft.com/GroupPolicy/Types">S-1-5-11</SID>
          <Name xmlns="http://www.microsoft.com/GroupPolicy/Types">NT AUTHORITY\Authenticated Users</Name>
        </Trustee>
        <Type xsi:type="PermissionType">
          <PermissionType>Allow</PermissionType>
        </Type>
        <Inherited>false</Inherited>
        <Applicability>
          <ToSelf>true</ToSelf>
          <ToDescendantObjects>false</ToDescendantObjects>
          <ToDescendantContainers>true</ToDescendantContainers>
          <ToDirectDescendantsOnly>false</ToDirectDescendantsOnly>
        </Applicability>
        <Standard>
          <GPOGroupedAccessEnum>Apply Group Policy</GPOGroupedAccessEnum>
        </Standard>
        <AccessMask>0</AccessMask>
      </TrusteePermissions>
    </Permissions>
    <AuditingPresent xmlns="http://www.microsoft.com/GroupPolicy/Types/Security">false</AuditingPresent>
  </SecurityDescriptor>
  <FilterDataAvailable>true</FilterDataAvailable>
  <Computer>
    <VersionDirectory>3</VersionDirectory>
    <VersionSysvol>3</VersionSysvol>
    <Enabled>true</Enabled>
    <ExtensionData>
      <Extension xmlns:q1="http://www.microsoft.com/GroupPolicy/Settings/Security" xsi:type="q1:SecuritySettings">
        <q1:Account>
          <q1:Name>ClearTextPassword</q1:Name>
          <q1:SettingBoolean>false</q1:SettingBoolean>
          <q1:Type>Password</q1:Type>
        </q1:Account>
        <q1:Account>
          <q1:Name>LockoutBadCount</q1:Name>
          <q1:SettingNumber>0</q1:SettingNumber>
          <q1:Type>Account Lockout</q1:Type>
        </q1:Account>
        <q1:Account>
          <q1:Name>MaximumPasswordAge</q1:Name>
          <q1:SettingNumber>42</q1:SettingNumber>
          <q1:Type>Password</q1:Type>
        </q1:Account>
        <q1:Account>
          <q1:Name>MinimumPasswordAge</q1:Name>
          <q1:SettingNumber>1</q1:SettingNumber>
          <q1:Type>Password</q1:Type>
        </q1:Account>
        <q1:Account>
          <q1:Name>MinimumPasswordLength</q1:Name>
          <q1:SettingNumber>7</q1:SettingNumber>
          <q1:Type>Password</q1:Type>
        </q1:Account>
        <q1:Account>
          <q1:Name>PasswordComplexity</q1:Name>
          <q1:SettingBoolean>true</q1:SettingBoolean>
          <q1:Type>Password</q1:Type>
        </q1:Account>
        <q1:Account>
          <q1:Name>PasswordHistorySize</q1:Name>
          <q1:SettingNumber>24</q1:SettingNumber>
          <q1:Type>Password</q1:Type>
        </q1:Account>
        <q1:Account>
          <q1:Name>MaxClockSkew</q1:Name>
          <q1:SettingNumber>5</q1:SettingNumber>
          <q1:Type>Kerberos</q1:Type>
        </q1:Account>
        <q1:Account>
          <q1:Name>MaxRenewAge</q1:Name>
          <q1:SettingNumber>7</q1:SettingNumber>
          <q1:Type>Kerberos</q1:Type>
        </q1:Account>
        <q1:Account>
          <q1:Name>MaxServiceAge</q1:Name>
          <q1:SettingNumber>600</q1:SettingNumber>
          <q1:Type>Kerberos</q1:Type>
        </q1:Account>
        <q1:Account>
          <q1:Name>MaxTicketAge</q1:Name>
          <q1:SettingNumber>10</q1:SettingNumber>
          <q1:Type>Kerberos</q1:Type>
        </q1:Account>
        <q1:Account>
          <q1:Name>TicketValidateClient</q1:Name>
          <q1:SettingBoolean>true</q1:SettingBoolean>
          <q1:Type>Kerberos</q1:Type>
        </q1:Account>
        <q1:SecurityOptions>
            <q1:KeyName>MACHINE\System\CurrentControlSet\Control\Lsa\\NoLMHash</q1:KeyName>
            <q1:SettingNumber>1</q1:SettingNumber>
          <q1:Display>
            <q1:Name>Network security: Do not store LAN Manager hash value on next password change</q1:Name>
            <q1:Units />
            <q1:DisplayBoolean>true</q1:DisplayBoolean>
          </q1:Display>
        </q1:SecurityOptions>
        <q1:SecurityOptions>
          <q1:SystemAccessPolicyName>ForceLogoffWhenHourExpire</q1:SystemAccessPolicyName>
          <q1:SettingNumber>0</q1:SettingNumber>
        </q1:SecurityOptions>
        <q1:SecurityOptions>
          <q1:SystemAccessPolicyName>LSAAnonymousNameLookup</q1:SystemAccessPolicyName>
          <q1:SettingNumber>0</q1:SettingNumber>
        </q1:SecurityOptions>
        <q1:Blocked>false</q1:Blocked>
      </Extension>
      <Name>Security</Name>
"""