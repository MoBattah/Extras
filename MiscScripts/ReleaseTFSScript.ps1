param(
[string]$copysource, #source of copy
[string]$copydest, #destination of copy
[string]$webconfigfile #config file to be deployed
)

$dirlist = Get-ChildItem -Path $copysource
$jsonpath = $copydest + "\Json\TenantsList.json"
$webconfigpath = $copysource + $webconfigfile
$webconfigdest = $copydest + "\Web.config"

#if the TenantsList json file exists,it excludes it from the copy operation. 
if (Test-Path $jsonpath) 
{$dirlist |
  % {
  Copy-Item $_.fullname $copydest -Recurse -Force -Exclude @("TenantsList.json", "Json", "Web*config") 
}} 
Else 
{Copy-Item -Path $copysource* -Recurse -Destination $copydest -Force -Exclude @("Web*config")} #refactor beginning of this

if (Test-Path -Path $webconfigpath) {
    Copy-Item -Path $webconfigpath -Destination $webconfigdest -Force
    Write-Host $webconfigdest "copied"
  }
  else {
  Write-Host "Web.config not replaced"
  }
