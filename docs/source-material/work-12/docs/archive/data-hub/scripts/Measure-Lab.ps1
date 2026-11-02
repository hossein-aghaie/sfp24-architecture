param([int]$LoadMinutes=2)
$ErrorActionPreference='Stop'
Set-Location -LiteralPath (Split-Path $PSScriptRoot -Parent)
$lab = Get-Content private/processes.json -Raw | ConvertFrom-Json
$output = 'private/logs/resource-samples.jsonl'
function Take-Sample([string]$phase) {
  $hub = Get-Process -Id $lab.hub
  $sim = Get-Process -Id $lab.simulator
  $row = @{at=(Get-Date).ToUniversalTime().ToString('o');phase=$phase;hubMiB=[math]::Round($hub.WorkingSet64/1MB,1);simulatorMiB=[math]::Round($sim.WorkingSet64/1MB,1);hubCpuSeconds=$hub.CPU;simulatorCpuSeconds=$sim.CPU;logicalProcessors=[Environment]::ProcessorCount}
  $row | ConvertTo-Json -Compress | Add-Content -LiteralPath $output
}
Invoke-RestMethod http://127.0.0.1:5223/api/control -Method Post -ContentType application/json -Body '{"action":"stop"}' | Out-Null
Take-Sample 'idle-start'
Start-Sleep -Seconds 60
Take-Sample 'idle-1min'
Invoke-RestMethod http://127.0.0.1:5223/api/control -Method Post -ContentType application/json -Body '{"action":"interval","seconds":5}' | Out-Null
Invoke-RestMethod http://127.0.0.1:5223/api/control -Method Post -ContentType application/json -Body '{"action":"start"}' | Out-Null
for($minuteIndex=1;$minuteIndex -le $LoadMinutes;$minuteIndex++){Start-Sleep -Seconds 60;Take-Sample "load-$($minuteIndex)min"}
Invoke-RestMethod http://127.0.0.1:5223/api/control -Method Post -ContentType application/json -Body '{"action":"stop"}' | Out-Null
Write-Host "Minute samples: $output"
