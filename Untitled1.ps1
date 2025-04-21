$directoryPath = "C:\ProgramData\ssh\logs" 
$acl = Get-Acl -Path $directoryPath 
$sddlString = "O:BAD:PAI(A;OICI;FA;;;SY)(A;OICI;FA;;;BA)(A;OICI;0x1200a9;;;AU)" 
$securityDescriptor = New-Object System.Security.AccessControl.RawSecurityDescriptor $sddlString 
$acl.SetSecurityDescriptorSddlForm($securityDescriptor.GetSddlForm("All")) 
Set-Acl -Path $directoryPath -AclObject $acl

Get-NetFirewallRule -Name OpenSSH-Server-In-TCP |Enable-NetFirewallRule

netstat -nao | find /i '":22"'