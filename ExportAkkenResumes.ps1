$baseurl = "https://appserver.akken.com/BSOS/Admin/Data_Mngmt/Candidates/getresume.php?fsno="  #enter in baseurl
$count = 1 #where would you like to start the export

While ($count -lt 52103){ #where would you like to end the export
$fullurl = $baseurl + $count
Write-Host $fullurl
Start-Process "chrome.exe" $fullurl #throw in your favorite browser
Start-Sleep -s 2 #sleep to not trigger loading issues
$count = $count + 1
}
