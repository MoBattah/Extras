param(
[string]$copysource,
[string]$copydest,
#[string]$environment
)

$jsonpath = $copydest + "\Json\TenantsList.json"

#if the TenantsList json file exists,it excludes it from the copy operation. 
if (Test-Path $jsonpath) 
{Get-ChildItem -Path $copysource |
  % {
  Copy-Item $_.fullname $copydest -Recurse -Force -Exclude @("TenantsList.json", "Json", "Web*config") 
}} 
Else 
{Copy-Item -Path $copysource* -Recurse -Destination $copydest -Force}
