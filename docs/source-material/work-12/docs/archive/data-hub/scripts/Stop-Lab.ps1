$ErrorActionPreference='Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
$pidFile = Join-Path $projectRoot 'private/processes.json'
if (-not (Test-Path -LiteralPath $pidFile)) { Write-Host 'No recorded lab processes.'; return }
$lab = Get-Content -LiteralPath $pidFile -Raw | ConvertFrom-Json
if ([IO.Path]::GetFullPath($lab.root) -ne [IO.Path]::GetFullPath($projectRoot)) { throw 'Process record belongs to another directory.' }
foreach ($entry in @(@{id=$lab.simulator;script='dist-server/server/simulator.js'},@{id=$lab.hub;script='dist-server/server/index.js'})) {
  if ([int]$entry.id -le 0) { continue }
  $process = Get-CimInstance Win32_Process -Filter "ProcessId=$([int]$entry.id)" -ErrorAction SilentlyContinue
  if (-not $process) { continue }
  # Refuse to stop a recycled PID or a different Node application.
  $expectedScript = Join-Path $projectRoot $entry.script
  if ($process.Name -ne 'node.exe' -or -not $process.CommandLine.Contains($expectedScript)) { throw "PID $($entry.id) no longer matches this lab. Nothing else will be stopped." }
  Stop-Process -Id ([int]$entry.id) -ErrorAction Stop
}
Write-Host 'Recorded lab processes stopped. Data retained in private/.'
