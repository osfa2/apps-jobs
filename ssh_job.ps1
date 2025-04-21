$folderPath = "C:\ProgramData\ssh\logs"
# $user = 'OSFA-APPS2\Administrator'

$user = 'OSFA-APPS2\Administrator'
Write-Output "--------------------------------------------"
Get-ACL -Path $folderPath | Format-Table -Wrap
Write-Output "--------------------------------------------"

$path = Get-ACL -Path $folderPath
$acl = New-Object -TypeName System.Security.AccessControl.FileSystemAccessRule($user, 'FullControl', 'ContainerInherit, ObjectInherit', 'None', 'Allow')
$path.removeaccessrule($acl)
# $path.SetAccessRule($acl)

Set-Acl -Path $folderPath -AclObject $path

Write-Output "--------------------------------------------"
Get-ACL -Path $folderPath | Format-Table -Wrap
Write-Output "--------------------------------------------"