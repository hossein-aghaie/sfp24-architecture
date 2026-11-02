$ErrorActionPreference='Stop'
Set-Location -LiteralPath (Split-Path $PSScriptRoot -Parent)
$lab=Get-Content private/processes.json -Raw | ConvertFrom-Json
$startedAt=(Get-Date).ToUniversalTime().ToString('o')
Start-Sleep -Seconds 30
$hub=Get-Process -Id $lab.hub
$sim=Get-Process -Id $lab.simulator
@{at=(Get-Date).ToUniversalTime().ToString('o');monitorStarted=$startedAt;window='first approximately 30 seconds after readiness, simulator stopped';hubPeakWorkingSetMiB=[math]::Round($hub.PeakWorkingSet64/1MB,1);simulatorPeakWorkingSetMiB=[math]::Round($sim.PeakWorkingSet64/1MB,1);hubWorkingSetMiB=[math]::Round($hub.WorkingSet64/1MB,1);simulatorWorkingSetMiB=[math]::Round($sim.WorkingSet64/1MB,1)} | ConvertTo-Json | Set-Content private/logs/startup-memory.json
